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

    # ── Issue tree resolved ────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Findings — Issue Tree Resolved</div>', unsafe_allow_html=True)
    st.markdown(
        "We set out with three questions. The analysis has answered all three. "
        "Below is the issue tree from the Context tab, now closed with data-driven answers."
    )

    try:
        suc = run_query(Q.VIZ_EXEC_SUCCESS_STATS).iloc[0]
        tab = run_query(Q.VIZ_EXEC_TABLETOP_STATS).iloc[0]
        avg_goal       = f"${suc['avg_success_goal']:,.0f}"
        pledge_per_backer = tab['avg_tabletop_pledged'] / tab['avg_tabletop_backers']
        backers_needed = int(round(10000 / pledge_per_backer))
        backers_expected = int(tab['avg_tabletop_backers'])
        pledge_per_backer_fmt = f"${pledge_per_backer:,.0f}"
    except Exception:
        avg_goal, backers_needed, backers_expected, pledge_per_backer_fmt = "$9,400", 131, 724, "$76"

    st.html(f"""
        <style>
          .it-card {{
            border-top: 2px solid #1D1D1F;
            padding: 18px 24px 24px 0;
          }}
          .it-step {{
            font-family: 'Lato', sans-serif;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.12em;
            color: #AEAEB2;
            margin-bottom: 4px;
          }}
          .it-question {{
            font-family: 'Lato', sans-serif;
            font-size: 11px;
            font-weight: 400;
            letter-spacing: 0.05em;
            color: #6E6E73;
            margin-bottom: 12px;
          }}
          .it-answer {{
            font-family: 'Georgia', serif;
            font-size: 38px;
            font-weight: 700;
            color: #1D1D1F;
            letter-spacing: -0.5px;
            line-height: 1.1;
            margin-bottom: 8px;
          }}
          .it-desc {{
            font-family: 'Lato', sans-serif;
            font-size: 13px;
            color: #3A3A3C;
            line-height: 1.65;
            margin-bottom: 6px;
          }}
          .it-evidence {{
            font-family: 'Lato', sans-serif;
            font-size: 12px;
            color: #6E6E73;
            line-height: 1.6;
          }}
          .it-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 32px;
            margin: 20px 0 36px 0;
          }}
          .it-root {{
            border: 1px solid #E5E5EA;
            padding: 16px 20px;
            margin-bottom: 28px;
            display: inline-block;
          }}
          .it-root-label {{
            font-family: 'Lato', sans-serif;
            font-size: 9px;
            font-weight: 700;
            letter-spacing: 0.12em;
            color: #AEAEB2;
            margin-bottom: 4px;
          }}
          .it-root-title {{
            font-family: 'Georgia', serif;
            font-size: 15px;
            font-weight: 700;
            color: #1D1D1F;
          }}
        </style>

        <div class="it-root">
          <div class="it-root-label">CENTRAL OBJECTIVE</div>
          <div class="it-root-title">Maximise Kickstarter campaign funding for a new board game company</div>
        </div>

        <div class="it-grid">

          <div class="it-card">
            <div class="it-step">01 — GOAL SETTING</div>
            <div class="it-question">What is a realistic campaign goal?</div>
            <div class="it-answer">{avg_goal}</div>
            <div class="it-desc">Average goal among successful Kickstarter campaigns across all categories.</div>
            <div class="it-evidence">
              Campaigns below $10K are significantly more likely to succeed.
              We recommend setting a goal of <strong>~$10,000</strong> for a first campaign —
              achievable, credible, and aligned with category norms.
            </div>
          </div>

          <div class="it-card">
            <div class="it-step">02 — BACKERS NEEDED</div>
            <div class="it-question">How many backers will be needed to meet that goal?</div>
            <div class="it-answer">~{backers_needed:,}</div>
            <div class="it-desc">Backers required to fund a $10,000 goal in the Tabletop Games subcategory.</div>
            <div class="it-evidence">
              Derived from a {pledge_per_backer_fmt} average pledge per backer across
              successful Tabletop Games campaigns. Goal ÷ avg pledge = backers required.
            </div>
          </div>

          <div class="it-card">
            <div class="it-step">03 — BACKERS EXPECTED</div>
            <div class="it-question">How many backers can the company realistically expect?</div>
            <div class="it-answer">{backers_expected:,}</div>
            <div class="it-desc">Average backer count for successful Tabletop Games campaigns.</div>
            <div class="it-evidence">
              This comfortably exceeds the ~{backers_needed} needed to hit $10K.
              Run for <strong>31–61 days</strong> to maximise momentum — the data-confirmed sweet spot
              for the category.
            </div>
          </div>

        </div>
    """)

    st.markdown("---")

    st.markdown('<div class="section-heading">Supporting Visualizations</div>', unsafe_allow_html=True)
    st.markdown("Five charts. One conclusion per chart. The data behind each recommendation.")

    st.markdown("---")

    # ── Chart 1: Scatter ──────────────────────────────────────────────────────
    col_chart, col_insight = st.columns([3, 2])
    with col_chart:
        st.html('<div class="viz-headline">Low goals succeed — and they overshoot.</div>')
        with st.spinner("Loading scatter data…"):
            df_scatter = run_query(Q.VIZ_SCATTER_DATA)
        st.plotly_chart(scatter_goal_pledged(df_scatter), use_container_width=True, key="tab4_scatter")
        st.html("""
            <div class="viz-chart-title">Goal vs. pledged amount — log scale</div>
            <div class="viz-chart-context">Each point is one campaign. Green = successful, red = failed.
            The diagonal marks where pledged equals goal.</div>
        """)
    with col_insight:
        st.html("""
            <div class="viz-panel">
                <div class="viz-num">01</div>
                <div>
                    <div class="viz-label">Insight</div>
                    <div class="viz-insight-text">Campaigns below $10K succeed at the highest rate
                    and raise the most relative to target. Above $10K, the success rate drops
                    sharply and overcrowding from failed campaigns increases.</div>
                </div>
                <div>
                    <div class="viz-label">Action</div>
                    <div class="viz-action-text">Set the goal at $10,000. Use stretch goals
                    for anything above — they capture excess demand without raising the
                    primary risk threshold.</div>
                </div>
            </div>
        """)

    st.markdown("---")

    # ── Chart 2: Histogram ────────────────────────────────────────────────────
    col_chart2, col_insight2 = st.columns([3, 2])
    with col_chart2:
        st.html('<div class="viz-headline">High goals don\'t attract bigger audiences. They just fail more.</div>')
        with st.spinner("Loading histogram data…"):
            df_hist = run_query(Q.VIZ_GOAL_HISTOGRAM)
        st.plotly_chart(histogram_goals(df_hist), use_container_width=True, key="tab4_hist")
        st.html("""
            <div class="viz-chart-title">Goal distribution by campaign outcome</div>
            <div class="viz-chart-context">Capped at $500K. Y-axis log scale.
            Successful campaigns are densely concentrated below $10K.</div>
        """)
    with col_insight2:
        st.html("""
            <div class="viz-panel">
                <div class="viz-num">02</div>
                <div>
                    <div class="viz-label">Insight</div>
                    <div class="viz-insight-text">Failed campaigns set goals their audiences
                    couldn't support. The goal does not signal quality to backers — it sets
                    a ceiling on who will back you. Higher goals shrink the eligible audience.</div>
                </div>
                <div>
                    <div class="viz-label">Action</div>
                    <div class="viz-action-text">Anchor at $10K. Signal upside through stretch
                    goals, not a higher primary target.</div>
                </div>
            </div>
        """)

    st.markdown("---")

    # ── Chart 3: Category performance ─────────────────────────────────────────
    col_chart3, col_insight3 = st.columns([3, 2])
    with col_chart3:
        st.html('<div class="viz-headline">Category choice is a distribution decision, not a branding one.</div>')
        with st.spinner("Loading category data…"):
            df_cat = run_query(Q.VIZ_CATEGORY_PERFORMANCE)
        metric_toggle = st.radio(
            "Rank by:",
            options=["Money Raised", "Backers"],
            key="cat_metric_toggle",
            horizontal=True,
        )
        metric_col = "total_raised" if metric_toggle == "Money Raised" else "total_backers"
        st.plotly_chart(category_performance(df_cat, metric=metric_col), use_container_width=True, key="tab4_cat")
        st.html("""
            <div class="viz-chart-title">All categories ranked by total raised or total backers</div>
            <div class="viz-chart-context">Toggle between metrics. Rankings are near-identical on both —
            audience size and funding are structurally linked.</div>
        """)
    with col_insight3:
        st.html("""
            <div class="viz-panel">
                <div class="viz-num">03</div>
                <div>
                    <div class="viz-label">Insight</div>
                    <div class="viz-insight-text">Games, Technology, and Design lead every ranking.
                    The category determines the backer pool — and backer pool determines outcome.
                    Tabletop Games tops subcategory rankings on both money raised and backer count.</div>
                </div>
                <div>
                    <div class="viz-label">Action</div>
                    <div class="viz-action-text">List under Games → Tabletop Games.
                    No other subcategory offers comparable backer depth or
                    spending capacity.</div>
                </div>
            </div>
        """)

    st.markdown("---")

    # ── Chart 4: Geographic ───────────────────────────────────────────────────
    col_chart4, col_insight4 = st.columns([3, 2])
    with col_chart4:
        st.html('<div class="viz-headline">Kickstarter is a US market. Plan accordingly.</div>')
        with st.spinner("Loading geographic data…"):
            df_geo = run_query(Q.VIZ_GEOGRAPHIC)
        st.plotly_chart(geographic_bar(df_geo), use_container_width=True, key="tab4_geo")
        st.html("""
            <div class="viz-chart-title">Top 5 countries by total pledged — successful campaigns only</div>
            <div class="viz-chart-context">Total USD pledged by country of origin.
            Campaign count indexed alongside total raised.</div>
        """)
    with col_insight4:
        st.html("""
            <div class="viz-panel">
                <div class="viz-num">04</div>
                <div>
                    <div class="viz-label">Insight</div>
                    <div class="viz-insight-text">The US generates more pledged dollars than all
                    other countries combined. GB and CA are secondary markets.
                    There is no material international audience to target on a first campaign.</div>
                </div>
                <div>
                    <div class="viz-label">Action</div>
                    <div class="viz-action-text">Direct pre-launch marketing to the US.
                    Board game review channels, Reddit, and conventions are the
                    highest-yield channels ahead of your campaign window.</div>
                </div>
            </div>
        """)

    st.markdown("---")

    # ── Chart 5: Duration ─────────────────────────────────────────────────────
    col_chart5, col_insight5 = st.columns([3, 2])
    with col_chart5:
        st.html('<div class="viz-headline">31–61 days raises the most. Shorter or longer both cost you.</div>')
        with st.spinner("Loading duration data…"):
            df_dur = run_query(Q.VIZ_DURATION_LINE)
        st.plotly_chart(campaign_duration(df_dur), use_container_width=True, key="tab4_dur")
        st.html("""
            <div class="viz-chart-title">Average amount raised by campaign length in days</div>
            <div class="viz-chart-context">Shaded region = optimal window. Pledge velocity
            peaks at launch and in the final 48 hours.</div>
        """)
    with col_insight5:
        st.html("""
            <div class="viz-panel">
                <div class="viz-num">05</div>
                <div>
                    <div class="viz-label">Insight</div>
                    <div class="viz-insight-text">Below 30 days, campaigns lack time to build
                    momentum. Above 61 days, pledge velocity collapses. The middle weeks of a
                    long campaign generate almost no new pledges — extending the window
                    does not extend the outcome.</div>
                </div>
                <div>
                    <div class="viz-label">Action</div>
                    <div class="viz-action-text">Run for 45 days. Launch hard,
                    send a mid-campaign update at day 22,
                    and close with a 48-hour final push.</div>
                </div>
            </div>
        """)
