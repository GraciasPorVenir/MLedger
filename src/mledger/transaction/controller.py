from pathlib import Path
from math import ceil

import pandas as pd
from sqlite3 import Row, Error
from datetime import datetime

from ..db import Connection


class TransactionController:
    def __init__(self, conn: Connection) -> None:
        self.conn: Connection = conn

    def check_filters(self, filters: dict[str, list[str | int]]) -> tuple[str, list]:
        where: list = []
        params: list = []
        for key, value in filters.items():
            if value:
                where.append(" OR ".join([f"{key} = ?"]))
                params.extend(value)
        return (f" WHERE {' AND '.join(where)}", params) if where else ("", [])

    def select_df(
        self,
        filters: dict[str, list[str | int]],
        limit: int = 15,
        page: int = 1,
    ) -> pd.DataFrame:
        page = max(1, int(page))
        where, params = self.check_filters(filters)
        params.extend([limit, limit * (page - 1)])
        sql: str = f"SELECT id, is_income, cents, currency, frequency, installments, category, created_at, last_payment FROM vw_transactions {where} LIMIT ? OFFSET ?;"
        df: pd.DataFrame = pd.read_sql(
            sql, self.conn.conn, params=params, index_col="id"
        )
        if df.empty:
            return df
        df["amount"] = df["cents"] / 100.0
        df["is_income"] = df["is_income"].astype(bool)
        df["created_at"] = pd.to_datetime(df["created_at"])
        df["last_payment"] = pd.to_datetime(df["last_payment"])
        return df

    def get_currencies(self) -> list[str]:
        with open(Path(__file__).resolve().parent / "currencies.txt") as f:
            return [line.strip() for line in f if line.strip()]

    def get_categories(self) -> list[str]:
        with self.conn.get_cursor() as cur:
            cat = cur.execute("SELECT name FROM categories;").fetchall()
            return [c[0] for c in cat]

    def get_pagination(
        self, filters: dict[str, list[str | int]], limit: int = 15
    ) -> int:
        with self.conn.get_cursor() as cur:
            where, params = self.check_filters(filters)
            count = cur.execute(
                f"SELECT COUNT(id) FROM transactions {where};", params
            ).fetchone()
            total_items = count[0] if count else 0
            if total_items == 0:
                return 1
            return ceil(total_items / limit)

    def insert(
        self,
        cents: int,
        category: str,
        frequency: int = 0,
        reason: str | None = None,
        currency: str = "USD",
        is_income: int = 1,
        installments: int = 1,
        partial_cents: int | None = None,
        paid_at: datetime | None = None,
    ) -> None:
        with self.conn.get_cursor() as cur:
            if currency not in self.get_currencies():
                raise Error("CUR_409")
            sql: str = "SELECT * FROM categories WHERE name = ?;"
            c: Row = cur.execute(sql, (category,)).fetchone()
            if c == None:
                raise Error("CAT_404")
            sql = "INSERT INTO metadata(category_id, frequency, reason) VALUES (?, ?, ?) ON CONFLICT(category_id, frequency, reason) DO UPDATE SET category_id = excluded.category_id RETURNING id;"
            m: Row = cur.execute(sql, (c["id"], frequency, reason)).fetchone()
            params = (m["id"], cents, currency, is_income, installments)
            sql = "INSERT INTO transactions(metadata_id, cents, currency, is_income, installments) VALUES (?, ?, ?, ?, ?) RETURNING *"
            t: Row = cur.execute(sql, params).fetchone()
            if partial_cents != None:
                sql: str = "INSERT INTO payments(cents, paid_at, transaction_id) VALUES (?, ?, ?);"
                cur.execute(sql, (partial_cents, paid_at, t["id"]))
