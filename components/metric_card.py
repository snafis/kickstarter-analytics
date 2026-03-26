"""Apple-style KPI metric card rendered via st.markdown."""

import streamlit as st


def metric_card(value: str, label: str, color: str = "#1D1D1F") -> None:
    """Render a single metric card."""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-value" style="color:{color}">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
