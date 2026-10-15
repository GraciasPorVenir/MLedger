import streamlit as st
from mledger.db import Connection
from mledger.config import Config
from mledger.transaction import table_view


@st.cache_resource
def get_conn() -> Connection:
    return Connection(Config())


def main():
    conn: Connection = get_conn()
    table_view(conn)


if __name__ == "__main__":
    main()
