"""Tab 3 — Data Analysis: six business questions with editable SQL cells."""

import streamlit as st

from components.sql_cell import sql_cell
import db.queries as Q


def render() -> None:
    st.markdown('<div class="tab-heading">Data Analysis</div>', unsafe_allow_html=True)
    st.markdown(
        "Six business questions, each answered with an editable SQL query. "
        "Modify any query and click **▶ Run Query** to explore the data yourself."
    )

    st.markdown("---")

    # ── Q1 ────────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Q1 — Are funding goals different between successful and failed campaigns?</div>', unsafe_allow_html=True)
    sql_cell(
        "tab3_q1",
        "Average goals, pledged, and backers by outcome",
        Q.Q1_OUTCOME_AVERAGES,
        description="Compare key averages between successful and failed campaigns.",
        insight=(
            "<strong>Finding:</strong> Successful campaigns set goals ~10× lower than failed ones "
            "($9,750 vs $97,425 on average). Lower, achievable goals attract more backers and build momentum. "
            "Standard deviation is high in both groups — the median is a better guide than the mean."
        ),
        editable=True,
        auto_run=True,
    )

    st.markdown("---")

    # ── Q2 ────────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Q2 — Which categories attract the most (and fewest) backers?</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        sql_cell(
            "tab3_q2_top_cat",
            "Top 3 categories by backers",
            Q.Q2_TOP_CATEGORIES_BACKERS,
            editable=True,
            auto_run=True,
        )
    with col_b:
        sql_cell(
            "tab3_q2_bot_cat",
            "Bottom 3 categories by backers",
            Q.Q2_BOTTOM_CATEGORIES_BACKERS,
            editable=True,
            auto_run=True,
        )

    col_c, col_d = st.columns(2)
    with col_c:
        sql_cell(
            "tab3_q2_top_sub",
            "Top 3 subcategories by backers",
            Q.Q2_TOP_SUBCATEGORIES_BACKERS,
            editable=True,
            auto_run=True,
        )
    with col_d:
        sql_cell(
            "tab3_q2_bot_sub",
            "Bottom 3 subcategories by backers",
            Q.Q2_BOTTOM_SUBCATEGORIES_BACKERS,
            editable=True,
            auto_run=True,
            insight=(
                "<strong>Finding:</strong> Games dominates backer counts, with Tabletop Games and Video Games "
                "leading subcategories. Crafts, Journalism, and Dance attract the fewest backers — likely due "
                "to niche audiences and lower digital virality."
            ),
        )

    st.markdown("---")

    # ── Q3 ────────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Q3 — Which categories raise the most money?</div>', unsafe_allow_html=True)

    col_e, col_f = st.columns(2)
    with col_e:
        sql_cell(
            "tab3_q3_top_cat",
            "Top 3 categories by money raised",
            Q.Q3_TOP_CATEGORIES_MONEY,
            editable=True,
            auto_run=True,
        )
    with col_f:
        sql_cell(
            "tab3_q3_bot_cat",
            "Bottom 3 categories by money raised",
            Q.Q3_BOTTOM_CATEGORIES_MONEY,
            editable=True,
            auto_run=True,
        )

    col_g, col_h = st.columns(2)
    with col_g:
        sql_cell(
            "tab3_q3_top_sub",
            "Top 3 subcategories by money raised",
            Q.Q3_TOP_SUBCATEGORIES_MONEY,
            editable=True,
            auto_run=True,
        )
    with col_h:
        sql_cell(
            "tab3_q3_bot_sub",
            "Bottom 3 subcategories by money raised",
            Q.Q3_BOTTOM_SUBCATEGORIES_MONEY,
            editable=True,
            auto_run=True,
            insight=(
                "<strong>Finding:</strong> The same top-3 categories (Games, Technology, Design) lead both "
                "backers <em>and</em> money raised — strong correlation between audience size and funding. "
                "Product Design and Tabletop Games lead subcategories for money raised."
            ),
        )

    st.markdown("---")

    # ── Q4 ────────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Q4 — What was the most successful tabletop game campaign?</div>', unsafe_allow_html=True)
    sql_cell(
        "tab3_q4",
        "Best tabletop game campaign",
        Q.Q4_BEST_TABLETOP_GAME,
        description="Find the highest-pledged successful campaign in the Tabletop Games subcategory.",
        insight=(
            "<strong>Finding:</strong> Kingdom Death: Monster 1.5 raised <strong>~$12.4M</strong> on a $100K goal "
            "with ~19,264 backers — a 124× overachievement. A known IP with a rabid fanbase, "
            "it shows what's possible when audience, product quality, and platform trust align."
        ),
        editable=True,
        auto_run=True,
    )

    st.markdown("---")

    # ── Q5 ────────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Q5 — Which countries raise the most money?</div>', unsafe_allow_html=True)
    sql_cell(
        "tab3_q5",
        "Top 3 countries by total pledged (successful campaigns)",
        Q.Q5_TOP_COUNTRIES,
        description="Rank countries by total USD pledged across all successful campaigns.",
        insight=(
            "<strong>Finding:</strong> The US dominates with an overwhelming majority of campaigns and pledged dollars. "
            "Great Britain and Canada are distant 2nd and 3rd — Kickstarter's US-centric origins explain the geographic skew."
        ),
        editable=True,
        auto_run=True,
    )

    st.markdown("---")

    # ── Q6 ────────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Q6 — Do longer campaigns raise more money?</div>', unsafe_allow_html=True)
    sql_cell(
        "tab3_q6",
        "Average raised by campaign duration",
        Q.Q6_DURATION_IMPACT,
        description="Group campaigns by duration in days and compare average amount raised.",
        insight=(
            "<strong>Finding:</strong> Campaigns in the <strong>31–61 day</strong> range tend to raise the most. "
            "Very short campaigns (&lt;15 days) underperform — not enough time to build momentum. "
            "Campaigns longer than 61 days show 'backer fatigue': most pledges happen at launch and in the final days, "
            "so a long dead zone in the middle hurts total raised."
        ),
        editable=True,
        auto_run=True,
    )
