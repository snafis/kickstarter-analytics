import sqlite3
from datetime import date
from pathlib import Path

import streamlit as st

DB_PATH = Path(__file__).parent.parent / "data" / "kickstarter.db"


@st.cache_resource
def get_connection() -> sqlite3.Connection:
    if not DB_PATH.exists():
        st.error(
            f"Database not found at `{DB_PATH}`. "
            "Run `uv run python data/setup.py` to create it."
        )
        st.stop()

    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row

    # Register DATEDIFF(a, b) → days between a and b
    def datediff(a: str, b: str) -> int:
        try:
            return (date.fromisoformat(b[:10]) - date.fromisoformat(a[:10])).days
        except Exception:
            return 0

    conn.create_function("DATEDIFF", 2, datediff)
    return conn
