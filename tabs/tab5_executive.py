"""Tab 5 — Executive Summary: headline recommendation, KPI cards, action items."""

import streamlit as st

from components.metric_card import metric_card
from db.executor import run_query
import db.queries as Q
from visualizations.campaign_duration import campaign_duration
from visualizations.category_performance import category_performance


def render() -> None:
    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="hero-container" style="text-align:center;">
            <div class="hero-title" style="font-size:32px;">
                Set a $10K goal. Run for 45 days. Aim for 190 backers.
            </div>
            <div class="hero-subtitle" style="text-align:center;margin-top:12px;">
                Three numbers distilled from 378,000+ campaigns.
                The data is clear on what drives Kickstarter success.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── KPI cards ─────────────────────────────────────────────────────────────
    try:
        suc = run_query(Q.VIZ_EXEC_SUCCESS_STATS).iloc[0]
        tab = run_query(Q.VIZ_EXEC_TABLETOP_STATS).iloc[0]
        avg_goal = f"${suc['avg_success_goal']:,.0f}"
        avg_backers = f"{int(suc['avg_backers']):,}"
        tab_pledged = f"${tab['avg_tabletop_pledged']:,.0f}"
        tab_backers = f"{int(tab['avg_tabletop_backers']):,}"
    except Exception:
        avg_goal = avg_backers = tab_pledged = tab_backers = "–"

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card(avg_goal, "Avg Successful Goal", color="#34C759")
    with c2:
        metric_card(avg_backers, "Avg Backers to Succeed", color="#007AFF")
    with c3:
        metric_card(tab_pledged, "Tabletop Avg Pledged", color="#5856D6")
    with c4:
        metric_card("31–61 days", "Sweet Spot Duration", color="#FF9500")

    st.markdown("---")

    # ── Evidence charts ────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Supporting Evidence</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("**Category performance (money raised)**")
        df_cat = run_query(Q.VIZ_CATEGORY_PERFORMANCE)
        st.plotly_chart(
            category_performance(df_cat, metric="total_raised"),
            use_container_width=True,
        )
    with col_right:
        st.markdown("**Duration sweet spot**")
        df_dur = run_query(Q.VIZ_DURATION_LINE)
        st.plotly_chart(campaign_duration(df_dur), use_container_width=True)

    st.markdown("---")

    # ── Recommendations ────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Action Recommendations</div>', unsafe_allow_html=True)

    recs = [
        (
            "1. Keep your goal modest and achievable",
            "Successful campaigns average ~$10K — not $100K. "
            "A smaller goal is easier to hit, triggers 'funded' momentum, "
            "and stretch goals can capture any overflow. "
            "The data shows that most failed campaigns set goals that were simply too high for their audience size.",
        ),
        (
            "2. Target the Games or Technology category",
            "These two categories account for a disproportionate share of both backers and dollars raised. "
            "If your product fits either space, you benefit from an existing community of engaged Kickstarter backers. "
            "Tabletop Games in particular shows very high average pledge per backer (~$98), "
            "indicating a premium-price-tolerant audience.",
        ),
        (
            "3. Run your campaign for 31–61 days",
            "The duration sweet spot is clear in the data. "
            "Campaigns shorter than 30 days don't build enough momentum; "
            "campaigns longer than 61 days experience backer fatigue. "
            "Plan your launch around a 45-day window with a strong Day 1 push and a final-48-hours reminder campaign.",
        ),
    ]

    for title, body in recs:
        st.markdown(
            f"""
            <div class="insight-callout" style="margin-bottom:16px;">
                <strong>{title}</strong><br>
                <span style="font-size:14px;color:#1D1D1F;">{body}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown(
        '<p style="color:#6E6E73;font-size:12px;text-align:center;">Analysis based on 378,000+ Kickstarter campaigns (2009–2018) · Dataset: Kaggle / kemical · Currency conversion: xe.com 11/06/2022</p>',
        unsafe_allow_html=True,
    )
