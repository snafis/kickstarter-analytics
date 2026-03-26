"""Tab 4 — Synthesis & Visualization: five Plotly charts with narrative."""

import streamlit as st

from db.executor import run_query
import db.queries as Q
from visualizations.scatter_goal_pledged import scatter_goal_pledged
from visualizations.histogram_goals import histogram_goals
from visualizations.category_performance import category_performance
from visualizations.geographic import geographic_bar
from visualizations.campaign_duration import campaign_duration


def render() -> None:
    st.markdown('<div class="tab-heading">Synthesis & Visualization</div>', unsafe_allow_html=True)
    st.markdown(
        "The six analysis queries are powerful — but charts reveal patterns that tables can't. "
        "Each visualization below synthesises a key finding from the analysis."
    )

    st.markdown("---")

    # ── Chart 1: Scatter ──────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">1 — Goal vs Pledged</div>', unsafe_allow_html=True)
    col_txt, col_chart = st.columns([1, 2])
    with col_txt:
        st.markdown(
            """
            **What it shows:** Every campaign plotted on a log-log scale.
            The dashed diagonal marks where goal equals pledged.

            **Key insight:** Successful campaigns (green) cluster *above* the diagonal —
            they overshoot their goals. Failed campaigns (red) cluster *below* it.
            The separation is clearest at low goals, reinforcing that modest targets succeed more often.
            """
        )
    with col_chart:
        with st.spinner("Loading scatter data…"):
            df_scatter = run_query(Q.VIZ_SCATTER_DATA)
        st.plotly_chart(scatter_goal_pledged(df_scatter), use_container_width=True, key="tab4_scatter")

    st.markdown("---")

    # ── Chart 2: Histogram ────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">2 — Goal Distribution by Outcome</div>', unsafe_allow_html=True)
    col_txt2, col_chart2 = st.columns([1, 2])
    with col_txt2:
        st.markdown(
            """
            **What it shows:** How campaign goals are distributed for successful vs failed campaigns
            (capped at $500K to exclude extreme outliers; Y-axis is log scale).

            **Key insight:** Successful campaigns are heavily concentrated below $10K.
            The distribution of failed campaigns has a much longer tail toward higher goals —
            ambition without audience is the most common failure mode.
            """
        )
    with col_chart2:
        with st.spinner("Loading histogram data…"):
            df_hist = run_query(Q.VIZ_GOAL_HISTOGRAM)
        st.plotly_chart(histogram_goals(df_hist), use_container_width=True, key="tab4_hist")

    st.markdown("---")

    # ── Chart 3: Category performance ─────────────────────────────────────────
    st.markdown('<div class="section-heading">3 — Category Performance</div>', unsafe_allow_html=True)
    col_txt3, col_chart3 = st.columns([1, 2])
    with col_txt3:
        st.markdown(
            """
            **What it shows:** All categories ranked by total money raised or total backers.

            **Key insight:** Games, Technology, and Design dominate on both metrics.
            The same three categories top both lists — showing that audience size and
            funding are tightly correlated. Niche categories (Crafts, Dance, Journalism)
            consistently underperform.
            """
        )
        metric_toggle = st.radio(
            "Rank by:",
            options=["Money Raised", "Backers"],
            key="cat_metric_toggle",
            horizontal=True,
        )
    with col_chart3:
        with st.spinner("Loading category data…"):
            df_cat = run_query(Q.VIZ_CATEGORY_PERFORMANCE)
        metric_col = "total_raised" if metric_toggle == "Money Raised" else "total_backers"
        st.plotly_chart(category_performance(df_cat, metric=metric_col), use_container_width=True, key="tab4_cat")

    st.markdown("---")

    # ── Chart 4: Geographic ───────────────────────────────────────────────────
    st.markdown('<div class="section-heading">4 — Geographic Distribution</div>', unsafe_allow_html=True)
    col_txt4, col_chart4 = st.columns([1, 2])
    with col_txt4:
        st.markdown(
            """
            **What it shows:** Top 5 countries by total pledged and campaign count
            (successful campaigns only).

            **Key insight:** The US accounts for the vast majority of both campaigns and pledged dollars.
            GB and CA are meaningful but distant second and third.
            For campaigns targeting non-US audiences, the data suggests a real opportunity gap.
            """
        )
    with col_chart4:
        with st.spinner("Loading geographic data…"):
            df_geo = run_query(Q.VIZ_GEOGRAPHIC)
        st.plotly_chart(geographic_bar(df_geo), use_container_width=True, key="tab4_geo")

    st.markdown("---")

    # ── Chart 5: Duration ─────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">5 — Campaign Duration Impact</div>', unsafe_allow_html=True)
    col_txt5, col_chart5 = st.columns([1, 2])
    with col_txt5:
        st.markdown(
            """
            **What it shows:** Average amount raised for each campaign length in days
            (1–92 days). The orange-shaded region marks the "sweet spot."

            **Key insight:** Campaigns running **31–61 days** raise the most on average.
            Shorter campaigns lack time to build momentum; longer ones experience
            "backer fatigue" — most pledges happen in the first and last few days,
            leaving a dead zone in the middle that erodes total raised.
            """
        )
    with col_chart5:
        with st.spinner("Loading duration data…"):
            df_dur = run_query(Q.VIZ_DURATION_LINE)
        st.plotly_chart(campaign_duration(df_dur), use_container_width=True, key="tab4_dur")
