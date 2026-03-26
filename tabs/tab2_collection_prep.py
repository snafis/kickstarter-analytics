"""Tab 2 — Data Collection & Prep: pipeline, schema exploration, quality checks."""

import streamlit as st

from components.pipeline_diagram import pipeline_diagram
from components.sql_cell import sql_cell
import db.queries as Q


def render() -> None:
    st.markdown('<div class="tab-heading">Data Collection & Preparation</div>', unsafe_allow_html=True)
    st.markdown(
        "Before any analysis can happen, raw data must be collected, cleaned, and structured. "
        "This tab walks through each step — from ingestion to the quality fixes that make our queries trustworthy."
    )

    # ── Pipeline diagram ───────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Data Pipeline</div>', unsafe_allow_html=True)
    pipeline_diagram()

    st.markdown("---")

    # ── Schema exploration ─────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Schema Exploration</div>', unsafe_allow_html=True)
    st.markdown("These read-only queries let you inspect the raw database structure.")

    sql_cell(
        "tab2_outcomes",
        "All campaign outcomes",
        Q.QC_ALL_OUTCOMES,
        description="What states can a campaign be in?",
        editable=False,
        auto_run=True,
    )

    sql_cell(
        "tab2_currencies",
        "All currencies",
        Q.QC_EXPLORE_CURRENCIES,
        description="Which currencies appear and how frequently?",
        editable=False,
        auto_run=True,
    )

    sql_cell(
        "tab2_categories",
        "All categories",
        Q.QC_ALL_CATEGORIES,
        description="Main categories with subcategory counts and campaign totals.",
        editable=False,
        auto_run=True,
    )

    sql_cell(
        "tab2_sample",
        "Sample campaign rows",
        Q.QC_SAMPLE_CAMPAIGNS,
        description="50 rows showing all joined columns.",
        editable=False,
        auto_run=True,
    )

    sql_cell(
        "tab2_countries",
        "Country distribution",
        Q.QC_COUNTRY_ANOMALY,
        description="Countries ranked by campaign count — watch for anomalies.",
        editable=False,
        auto_run=True,
    )

    st.markdown("---")

    # ── Data quality ───────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Data Quality Issues & Fixes</div>', unsafe_allow_html=True)
    st.markdown("Each issue below was discovered during exploration. The editable queries let you verify the fix.")

    # Issue 1 — backers=0 but pledged>0
    st.markdown(
        '<div class="quality-issue">⚠️ <strong>Issue 1: Backers = 0 but Pledged &gt; 0</strong> — Logically impossible; these rows are corrupted.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="quality-fix">✅ <strong>Fix:</strong> Exclude rows where <code>backers = 0 AND pledged &gt; 0</code> from all analysis views.</div>',
        unsafe_allow_html=True,
    )
    sql_cell(
        "tab2_qc1",
        "Verify: count of anomalous rows",
        Q.QC_ZERO_BACKERS_WITH_PLEDGED,
        description="How many campaigns have zero backers but positive pledged amounts?",
        editable=True,
        auto_run=True,
    )

    # Issue 2 — non-standard outcomes
    st.markdown(
        '<div class="quality-issue">⚠️ <strong>Issue 2: Non-standard outcomes</strong> — Outcomes like "live", "undefined", and "cancelled" add noise to success/failure analysis.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="quality-fix">✅ <strong>Fix:</strong> Filter to <code>outcome IN (\'successful\', \'failed\')</code> in the base view.</div>',
        unsafe_allow_html=True,
    )
    sql_cell(
        "tab2_qc2",
        "Verify: non-standard outcomes excluded",
        """SELECT outcome, COUNT(*) AS n
FROM v_campaign_info
GROUP BY outcome
ORDER BY n DESC""",
        description="After filtering, only successful and failed should appear.",
        editable=True,
        auto_run=True,
    )

    # Issue 3 — currency magnitude problem
    st.markdown(
        '<div class="quality-issue">⚠️ <strong>Issue 3: Currency magnitudes are incomparable</strong> — A $1 USD goal and a ¥1 JPY goal are very different values.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="quality-fix">✅ <strong>Fix:</strong> Convert all monetary values to USD using xe.com rates (11/06/2022) stored in the <code>currency_rate</code> table.</div>',
        unsafe_allow_html=True,
    )
    sql_cell(
        "tab2_qc3",
        "Verify: USD normalisation",
        """SELECT cu.name AS currency, cr.usd_rate,
       COUNT(*) AS campaigns,
       ROUND(AVG(c.goal), 0) AS avg_raw_goal,
       ROUND(AVG(c.goal * cr.usd_rate), 0) AS avg_usd_goal
FROM campaign c
JOIN currency cu ON c.currency_id = cu.id
LEFT JOIN currency_rate cr ON c.currency_id = cr.currency_id
WHERE c.outcome IN ('successful','failed')
GROUP BY cu.name, cr.usd_rate
ORDER BY campaigns DESC""",
        description="Compare raw vs USD-normalised average goals per currency.",
        editable=True,
        auto_run=True,
    )

    # Issue 4 — corrupted country
    st.markdown(
        '<div class="quality-issue">⚠️ <strong>Issue 4: Corrupted country code</strong> — Country name <code>N,0&quot;</code> is clearly an encoding artefact, not a real country.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="quality-fix">✅ <strong>Fix:</strong> Exclude this country ID from the base view.</div>',
        unsafe_allow_html=True,
    )
    sql_cell(
        "tab2_qc4",
        "Verify: corrupted country excluded",
        """SELECT co.name AS country, COUNT(*) AS campaigns
FROM v_campaign_info v
JOIN country co ON v.country_id = co.id
WHERE co.name LIKE '%N,0%'""",
        description="Should return 0 rows after the fix is applied.",
        editable=True,
        auto_run=True,
    )
