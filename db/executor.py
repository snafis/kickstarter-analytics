from __future__ import annotations

import pandas as pd
import streamlit as st

from db.connection import get_connection


@st.cache_data(ttl=3600)
def run_query(sql: str, params: tuple = ()) -> pd.DataFrame:
    conn = get_connection()
    return pd.read_sql_query(sql, conn, params=params)


def safe_run(sql: str, params: tuple = ()) -> tuple[pd.DataFrame | None, str | None]:
    try:
        conn = get_connection()
        df = pd.read_sql_query(sql, conn, params=params)
        return df, None
    except Exception as exc:
        return None, str(exc)
