import streamlit as st

from mledger.config import Config
from mledger.db import Connection
from mledger.transaction import TransactionView
from mledger.locales import get_langs, get_lang


@st.cache_resource
def get_conn(config: Config) -> Connection:
    return Connection(config)


def main() -> None:
    st.set_page_config(
        page_title="MLedger",
        page_icon="ML",
        layout="wide",
        initial_sidebar_state="auto",
    )
    config: Config = Config()
    conn: Connection = get_conn(config)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("MLedger")
    with col2:
        lang: str = st.selectbox(
            ".",
            options=get_langs(),
            index=0,
            label_visibility="hidden",
            filter_mode=None,
        )

    tview: TransactionView = TransactionView(conn, lang=get_lang("transaction", lang))
    select_page = st.Page(tview.select, title="Transactions", default=True)
    insert_page = st.Page(tview.insert, title="Create Transaction")
    tview.insert_page = insert_page
    tview.select_page = select_page

    pg = st.navigation([select_page, insert_page])
    pg.run()


if __name__ == "__main__":
    main()
