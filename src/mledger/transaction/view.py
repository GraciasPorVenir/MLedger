import pandas as pd
import streamlit as st

from ..db import Connection
from .controller import TransactionController


def table_view(conn: Connection, limit: int = 1000, page: int = 1):
    controller: TransactionController = TransactionController(conn)
    df: pd.DataFrame = controller.select_df(limit, page)
    st.dataframe(
        df,
        column_config={
            "created_at": st.column_config.DatetimeColumn(format="YYY-MM-DD HH:mm"),
            "cents": None,
            "metadata_id": None,
            "category_id": None,
        },
        hide_index=True,
        width="stretch",
    )
