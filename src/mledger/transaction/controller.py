from decimal import Decimal
from pathlib import Path

import pandas as pd
from sqlite3 import Row, Error
from datetime import datetime

from .model import ViewTransaction
from ..db import Connection


class TransactionController:
    def __init__(self, conn: Connection) -> None:
        self.conn: Connection = conn

    def select_df(self, limit: int = 1000, page: int = 1) -> pd.DataFrame:
        page = max(1, page)
        sql: str = (
            "SELECT * FROM vw_transactions ORDER BY created_at DESC LIMIT ? OFFSET ?;"
        )
        params: tuple[int, ...] = (limit, limit * (page - 1))
        df: pd.DataFrame = pd.read_sql(
            sql, self.conn.conn, params=params, index_col="id"
        )
        if df.empty:
            return df
        df["amount"] = (df["cents"] / 100).map("{:0.2f}".format)
        df["is_income"] = df["is_income"].astype(bool)
        df["created_at"] = pd.to_datetime(df["created_at"])
        return df

    def get_currencies(self) -> list[str]:
        with open(Path(__file__).resolve().parent / "currencies.txt") as f:
            return f.readlines()

    def insert(
        self,
        cents: int,
        category: str,
        frequency: int = 0,
        reason: str | None = None,
        currency: str = "USD",
        is_income: int = 1,
        installments: int = 1,
        created_at: str = datetime.now().isoformat(sep=" ", timespec="seconds"),
    ) -> ViewTransaction:
        with self.conn.get_cursor() as cur:
            if currency not in self.get_currencies():
                raise Error("CUR_409")
            sql: str = "SELECT * FROM categories WHERE name = ?;"
            c: Row = cur.execute(sql, (category,)).fetchone()
            if c == None:
                raise Error("CAT_404")
            sql = "INSERT INTO metadata(category_id, frequency, reason) VALUES (?, ?, ?) RETURNING id;"
            m: Row = cur.execute(sql, (c["id"], frequency, reason)).fetchone()
            params = (m["id"], cents, currency, is_income, installments, created_at)
            sql = "INSERT INTO transactions(metadata_id, cents, currency, is_income, installments, created_at) VALUES (?, ?, ?, ?, ?, ?) RETURNING *"
            t: Row = cur.execute(sql, params).fetchone()
            return ViewTransaction(
                id=t["id"],
                metadata_id=t["metadata_id"],
                category_id=m["category_id"],
                cents=t["cents"],
                currency=t["currency"],
                is_income=t["is_income"],
                installments=t["installments"],
                created_at=t["created_at"],
                category=c["name"],
                frequency=m["frequency"],
                reason=m["reason"],
            )
