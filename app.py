"""
Kickstarter Analytics — Streamlit application entry point.

Run with:
    uv run streamlit run app.py
"""

from pathlib import Path

import streamlit as st

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kickstarter Analytics",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Inject custom CSS ──────────────────────────────────────────────────────────
css_path = Path(__file__).parent / "styles" / "custom.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# ── Tab scaffold ───────────────────────────────────────────────────────────────
from tabs import (
    tab1_context,
    tab2_collection_prep,
    tab3_analysis,
    tab4_synthesis,
    tab5_executive,
)

tab_labels = [
    "🌍 Context",
    "🔧 Data Collection & Prep",
    "🔍 Data Analysis",
    "📊 Synthesis & Visualization",
    "📋 Executive Summary",
]

tabs = st.tabs(tab_labels)

with tabs[0]:
    tab1_context.render()

with tabs[1]:
    tab2_collection_prep.render()

with tabs[2]:
    tab3_analysis.render()

with tabs[3]:
    tab4_synthesis.render()

with tabs[4]:
    tab5_executive.render()
