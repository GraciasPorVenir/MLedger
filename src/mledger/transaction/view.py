import pandas as pd
import streamlit as st

from mledger.db import Connection
from mledger.transaction.controller import TransactionController


class TransactionView:
    def __init__(
        self,
        conn: Connection,
        lang: dict,
        insert_page: st.Page | None = None,
        select_page: st.Page | None = None,
    ) -> None:
        self.controller: TransactionController = TransactionController(conn)
        self.insert_page = insert_page
        self.select_page = select_page
        self.lang: dict = lang

    @st.cache_data
    def get_df(
        _self,
        filters: dict[str, list[int | str]],
        limit: int = 20,
        page: int = 1,
    ) -> pd.DataFrame:
        return _self.controller.select_df(limit=limit, page=page, filters=filters)

    def select(self) -> None:
        filters: dict[str, list[str | int]] = {}

        cA1, cA2, cA3 = st.columns([2, 1, 1])
        with cA1:
            filters["category"] = st.multiselect(
                self.lang["category"], self.controller.get_categories()
            )
        with cA2:
            filters["currency"] = st.multiselect(
                self.lang["currency"], self.controller.get_currencies()
            )
        with cA3:
            filters["frequency"] = st.multiselect(
                self.lang["frequency"], self.lang["frequencies"]
            )

        cB1, cB2 = st.columns([2, 1])
        with cB2:
            if self.insert_page and st.button(self.lang["new"]):
                st.switch_page(self.insert_page)
        with cB1:
            LIMIT: int = 20
            page: int = st.pagination(
                self.controller.get_pagination(filters=filters, limit=LIMIT)
            )

        df: pd.DataFrame = self.get_df(limit=LIMIT, page=page, filters=filters)
        column_order: list[str] = [
            "is_income",
            "amount",
            "currency",
            "frequency",
            "installments",
            "category",
            "created_at",
            "last_payment",
        ]
        column_config: dict = {
            "is_income": self.lang["is_income"],
            "amount": self.lang["amount"],
            "currency": self.lang["currency"],
            "installments": self.lang["installments"],
            "created_at": st.column_config.DatetimeColumn(
                format="HH:mm DD/MM/YYYY", label=self.lang["created_at"]
            ),
            "frequency": st.column_config.SelectboxColumn(
                label=self.lang["frequency"],
                options=list(range(len(self.lang["frequencies"]))),
                format_func=lambda x: self.lang["frequencies"][int(x)],
            ),
            "last_payment": st.column_config.DatetimeColumn(
                format="HH:mm DD/MM/YYYY", label=self.lang["last_payment"]
            ),
        }
        st.dataframe(
            df,
            column_config=column_config,
            column_order=column_order,
            hide_index=True,
            width="stretch",
        )

    def insert(self) -> None:
        frequencies: list[str] = self.lang["frequencies"]
        col1, col2 = st.columns([2, 1])
        with col1:
            st.title(self.lang["new"])
        with col2:
            if st.button(self.lang["back"]) and self.select_page:
                st.switch_page(self.select_page)
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            is_income: bool = st.checkbox(self.lang["is_income"])
        with col2:
            amount = st.number_input(self.lang["amount"], min_value=1.0, format="%.2f")
        with col3:
            currency: str = st.selectbox(
                self.lang["currency"],
                self.controller.get_currencies(),
                filter_mode=None,
            )
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            installments: int = st.number_input(
                self.lang["installments"], min_value=1, step=1, format="%d"
            )
        with col2:
            frequency: str = st.selectbox(
                self.lang["frequency"],
                frequencies,
                index=0,
                filter_mode=None,
            )
        with col3:
            category: str = st.selectbox(
                self.lang["category"],
                self.controller.get_categories(),
                filter_mode=None,
            )
        reason: str | None = st.text_input(self.lang["reason"])
        is_paid: bool = st.toggle(self.lang["partial_amount"])
        partial_amount = 0
        paid_at = None
        if is_paid:
            col1, col2 = st.columns([2, 1])
            with col1:
                partial_amount = st.number_input(
                    self.lang["amount"],
                    min_value=1.0,
                    format="%.2f",
                    value=amount / installments,
                )
            with col2:
                paid_at = st.datetime_input(self.lang["paid_at"])
        can_send = (
            amount > 0
            and installments > 0
            and (not is_paid or (is_paid and partial_amount > 0))
        )

        if st.button(self.lang["send"], disabled=not can_send):
            try:
                data = {
                    "cents": int(amount * 100),
                    "is_income": int(is_income),
                    "currency": currency,
                    "installments": installments,
                    "frequency": frequencies.index(frequency),
                    "category": category,
                    "reason": reason,
                }
                if is_paid:
                    data["partial_cents"] = int(partial_amount * 100)
                    data["paid_at"] = paid_at
                self.controller.insert(**data)
                st.success("Exito")
            except Exception as e:
                st.error(e)
