"""Tab 2 — Data Collection & Prep: pipeline, normalisation, exploration, validation."""

import streamlit as st
from datetime import datetime

from components.metric_card import metric_card
from components.pipeline_diagram import pipeline_diagram
from components.sql_cell import sql_cell
from db.executor import run_query
import db.queries as Q


def render() -> None:
    st.markdown('<div class="tab-heading">Data Collection & Preparation</div>', unsafe_allow_html=True)
    st.markdown(
        "Before any analysis can begin, raw data must be scraped, normalised for storage, "
        "inspected for quality issues, and finally assembled into a clean analytical table "
        "that serves as the foundation for every query in this report."
    )

    st.markdown(
        """
        <div style="overflow-x:auto; padding:20px 0 28px 0;">
        <svg width="760" height="130" viewBox="0 0 760 130" xmlns="http://www.w3.org/2000/svg"
             style="font-family:'Lato',sans-serif;">
          <defs>
            <marker id="flow-arr" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
              <path d="M0,0 L0,6 L8,3 z" fill="#1D1D1F"/>
            </marker>
          </defs>

          <rect x="0" y="10" width="160" height="110" rx="0" fill="#FFFFFF" stroke="#C8C8CC" stroke-width="1"/>
          <text x="80" y="27" text-anchor="middle" fill="#AEAEB2" font-size="9" letter-spacing="1">01</text>
          <line x1="14" y1="33" x2="146" y2="33" stroke="#E5E5EA" stroke-width="1"/>
          <text x="80" y="48" text-anchor="middle" fill="#1D1D1F" font-size="9" font-weight="700" letter-spacing="2">COLLECTION</text>
          <text x="80" y="65" text-anchor="middle" fill="#6E6E73" font-size="10">Web scraping</text>
          <text x="80" y="79" text-anchor="middle" fill="#6E6E73" font-size="10">Kaggle Dataset</text>
          <text x="80" y="93" text-anchor="middle" fill="#AEAEB2" font-size="9">378,661 campaigns</text>

          <line x1="160" y1="65" x2="193" y2="65" stroke="#1D1D1F" stroke-width="1" marker-end="url(#flow-arr)"/>

          <rect x="200" y="10" width="160" height="110" rx="0" fill="#FFFFFF" stroke="#C8C8CC" stroke-width="1"/>
          <text x="280" y="27" text-anchor="middle" fill="#AEAEB2" font-size="9" letter-spacing="1">02</text>
          <line x1="214" y1="33" x2="346" y2="33" stroke="#E5E5EA" stroke-width="1"/>
          <text x="280" y="48" text-anchor="middle" fill="#1D1D1F" font-size="9" font-weight="700" letter-spacing="2">NORMALISATION</text>
          <text x="280" y="65" text-anchor="middle" fill="#6E6E73" font-size="10">Flat CSV → 5 tables</text>
          <text x="280" y="79" text-anchor="middle" fill="#6E6E73" font-size="10">Foreign key refs</text>
          <text x="280" y="93" text-anchor="middle" fill="#AEAEB2" font-size="9">Storage efficiency</text>

          <line x1="360" y1="65" x2="393" y2="65" stroke="#1D1D1F" stroke-width="1" marker-end="url(#flow-arr)"/>

          <rect x="400" y="10" width="160" height="110" rx="0" fill="#FFFFFF" stroke="#C8C8CC" stroke-width="1"/>
          <text x="480" y="27" text-anchor="middle" fill="#AEAEB2" font-size="9" letter-spacing="1">03</text>
          <line x1="414" y1="33" x2="546" y2="33" stroke="#E5E5EA" stroke-width="1"/>
          <text x="480" y="48" text-anchor="middle" fill="#1D1D1F" font-size="9" font-weight="700" letter-spacing="2">INSPECTION</text>
          <text x="480" y="65" text-anchor="middle" fill="#6E6E73" font-size="10">Explore each table</text>
          <text x="480" y="79" text-anchor="middle" fill="#6E6E73" font-size="10">4 issues identified</text>
          <text x="480" y="93" text-anchor="middle" fill="#AEAEB2" font-size="9">Quality fixes applied</text>

          <line x1="560" y1="65" x2="593" y2="65" stroke="#1D1D1F" stroke-width="1" marker-end="url(#flow-arr)"/>

          <rect x="600" y="10" width="160" height="110" rx="0" fill="#FFFFFF" stroke="#1D1D1F" stroke-width="1.5"/>
          <text x="680" y="27" text-anchor="middle" fill="#AEAEB2" font-size="9" letter-spacing="1">04</text>
          <line x1="614" y1="33" x2="746" y2="33" stroke="#E5E5EA" stroke-width="1"/>
          <text x="680" y="48" text-anchor="middle" fill="#1D1D1F" font-size="9" font-weight="700" letter-spacing="1.5">ANALYTICAL TABLE</text>
          <text x="680" y="65" text-anchor="middle" fill="#6E6E73" font-size="10">v_condensed</text>
          <text x="680" y="79" text-anchor="middle" fill="#6E6E73" font-size="10">USD · duration · clean</text>
          <text x="680" y="93" text-anchor="middle" fill="#AEAEB2" font-size="9">Base for all analysis</text>

        </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── 1. Data Collection Pipeline ────────────────────────────────────────────
    st.markdown('<div class="section-heading">1 — Data Collection</div>', unsafe_allow_html=True)
    st.markdown(
        "Campaign data is scraped from kickstarter.com and made available as a structured CSV "
        "via Kaggle. The raw file is ingested into a relational database, which the analytics "
        "workbench then queries to produce the visualisations in this report."
    )
    pipeline_diagram()

    st.markdown("---")

    # ── 2. Database Normalisation ──────────────────────────────────────────────
    st.markdown('<div class="section-heading">2 — Normalisation</div>', unsafe_allow_html=True)
    st.markdown(
        "The raw CSV arrives as a single flat file with repeated strings for category, country, "
        "and currency on every row. Normalising into five tables removes that redundancy, "
        "reduces storage, and lets us update lookup values in one place."
    )

    st.markdown(
        """
        <div style="overflow-x:auto;padding:16px 0 24px 0;">
        <svg width="760" height="200" viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg"
             style="font-family:'Lato',sans-serif;">

          <line x1="210" y1="48" x2="290" y2="90" stroke="#C8C8CC" stroke-width="1" stroke-dasharray="4,3"/>
          <line x1="210" y1="133" x2="290" y2="120" stroke="#C8C8CC" stroke-width="1" stroke-dasharray="4,3"/>
          <line x1="550" y1="43" x2="470" y2="90" stroke="#C8C8CC" stroke-width="1" stroke-dasharray="4,3"/>
          <line x1="550" y1="133" x2="470" y2="120" stroke="#C8C8CC" stroke-width="1" stroke-dasharray="4,3"/>

          <rect x="290" y="55" width="180" height="95" rx="0" fill="#FFFFFF" stroke="#1D1D1F" stroke-width="1.5"/>
          <text x="380" y="76" text-anchor="middle" fill="#1D1D1F" font-size="11" font-weight="700" letter-spacing="0.08em">CAMPAIGN</text>
          <line x1="306" y1="82" x2="454" y2="82" stroke="#E5E5EA" stroke-width="1"/>
          <text x="380" y="97"  text-anchor="middle" fill="#6E6E73" font-size="10">id · name · goal · pledged</text>
          <text x="380" y="111" text-anchor="middle" fill="#6E6E73" font-size="10">backers · outcome</text>
          <text x="380" y="125" text-anchor="middle" fill="#6E6E73" font-size="10">launched · deadline</text>
          <text x="380" y="140" text-anchor="middle" fill="#AEAEB2" font-size="9">sub_category_id · country_id · currency_id</text>

          <rect x="55" y="18" width="155" height="52" rx="0" fill="#FFFFFF" stroke="#C8C8CC" stroke-width="1"/>
          <text x="133" y="37" text-anchor="middle" fill="#1D1D1F" font-size="11" font-weight="700" letter-spacing="0.06em">SUB_CATEGORY</text>
          <line x1="69" y1="43" x2="196" y2="43" stroke="#E5E5EA" stroke-width="1"/>
          <text x="133" y="57" text-anchor="middle" fill="#6E6E73" font-size="10">id · name · category_id</text>

          <rect x="55" y="108" width="155" height="46" rx="0" fill="#FFFFFF" stroke="#C8C8CC" stroke-width="1"/>
          <text x="133" y="127" text-anchor="middle" fill="#1D1D1F" font-size="11" font-weight="700" letter-spacing="0.06em">CATEGORY</text>
          <line x1="69" y1="133" x2="196" y2="133" stroke="#E5E5EA" stroke-width="1"/>
          <text x="133" y="146" text-anchor="middle" fill="#6E6E73" font-size="10">id · name</text>

          <rect x="550" y="18" width="155" height="46" rx="0" fill="#FFFFFF" stroke="#C8C8CC" stroke-width="1"/>
          <text x="628" y="37" text-anchor="middle" fill="#1D1D1F" font-size="11" font-weight="700" letter-spacing="0.06em">COUNTRY</text>
          <line x1="564" y1="43" x2="691" y2="43" stroke="#E5E5EA" stroke-width="1"/>
          <text x="628" y="56" text-anchor="middle" fill="#6E6E73" font-size="10">id · name</text>

          <rect x="550" y="108" width="155" height="46" rx="0" fill="#FFFFFF" stroke="#C8C8CC" stroke-width="1"/>
          <text x="628" y="127" text-anchor="middle" fill="#1D1D1F" font-size="11" font-weight="700" letter-spacing="0.06em">CURRENCY</text>
          <line x1="564" y1="133" x2="691" y2="133" stroke="#E5E5EA" stroke-width="1"/>
          <text x="628" y="146" text-anchor="middle" fill="#6E6E73" font-size="10">id · name</text>

        </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        total = run_query("SELECT COUNT(*) AS n FROM campaign").iloc[0]["n"]
        cats = run_query("SELECT COUNT(*) AS n FROM category").iloc[0]["n"]
        countries = run_query("SELECT COUNT(*) AS n FROM country").iloc[0]["n"]
        dates = run_query(
            "SELECT MIN(launched) AS start, MAX(launched) AS end FROM campaign"
            " WHERE launched >= '2009-01-01'"
        ).iloc[0]
        fmt = lambda s: datetime.strptime(str(s)[:7], "%Y-%m").strftime("%b %Y")
        date_range = f"{fmt(dates['start'])} – {fmt(dates['end'])}"
    except Exception:
        total, cats, countries, date_range = "–", "–", "–", "–"

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card(f"{total:,}" if isinstance(total, int) else total, "Total Campaigns")
    with c2:
        metric_card(date_range, "Date Range")
    with c3:
        metric_card(str(cats), "Categories")
    with c4:
        metric_card(str(countries), "Countries")

    st.markdown("---")

    # ── 3. Table Inspection ────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">3 — Table Inspection</div>', unsafe_allow_html=True)
    st.markdown(
        "With the data loaded, we inspect each table in turn. This surfaces the shape of the "
        "data and flags any quality concerns that will need to be resolved before analysis."
    )

    sql_cell(
        "tab2_outcomes",
        "Campaign outcomes",
        Q.QC_ALL_OUTCOMES,
        description="What states can a campaign be in?",
        editable=False,
        auto_run=True,
    )

    sql_cell(
        "tab2_categories",
        "Categories & subcategories",
        Q.QC_ALL_CATEGORIES,
        description="Main categories with subcategory counts and campaign totals.",
        editable=False,
        auto_run=True,
    )

    sql_cell(
        "tab2_currencies",
        "Currency breakdown",
        Q.QC_EXPLORE_CURRENCIES,
        description="Which currencies appear and how frequently?",
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

    sql_cell(
        "tab2_sample",
        "Sample campaign rows",
        Q.QC_SAMPLE_CAMPAIGNS,
        description="50 rows showing all joined columns.",
        editable=False,
        auto_run=True,
    )

    st.markdown("---")

    # ── 4. Quality Fixes & Analytical Table ───────────────────────────────────
    st.markdown('<div class="section-heading">4 — Quality Fixes & Analytical Table</div>', unsafe_allow_html=True)
    st.markdown(
        "Inspection revealed four data quality issues. Each is resolved in a base view "
        "<code>v_campaign_info</code>. A second view, <code>v_condensed</code>, builds on top "
        "of it — adding campaign duration in days and USD-normalised monetary values — to produce "
        "the clean analytical table used by every query in this report.",
        unsafe_allow_html=True,
    )

    # Issue 1 — backers=0 but pledged>0
    st.markdown(
        '<div class="quality-issue"><strong>Issue 1 — Backers = 0 but Pledged &gt; 0</strong><br>'
        'Logically impossible. These rows indicate corrupted or incomplete records.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="quality-fix"><strong>Fix:</strong> Exclude rows where <code>backers = 0 AND pledged &gt; 0</code> from all analysis views.</div>',
        unsafe_allow_html=True,
    )
    sql_cell(
        "tab2_qc1",
        "Verify — anomalous backer rows",
        Q.QC_ZERO_BACKERS_WITH_PLEDGED,
        description="How many campaigns have zero backers but positive pledged amounts?",
        editable=True,
        auto_run=True,
    )

    # Issue 2 — non-standard outcomes
    st.markdown(
        '<div class="quality-issue"><strong>Issue 2 — Non-standard outcomes</strong><br>'
        'Outcomes such as "live", "undefined", and "cancelled" add noise to success/failure analysis.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="quality-fix"><strong>Fix:</strong> Filter to <code>outcome IN (\'successful\', \'failed\')</code> in the base view.</div>',
        unsafe_allow_html=True,
    )
    sql_cell(
        "tab2_qc2",
        "Verify — outcome distribution after filter",
        """SELECT outcome, COUNT(*) AS n
FROM v_campaign_info
GROUP BY outcome
ORDER BY n DESC""",
        description="After filtering, only successful and failed should appear.",
        editable=True,
        auto_run=True,
    )

    # Issue 3 — currency magnitude
    st.markdown(
        '<div class="quality-issue"><strong>Issue 3 — Currency magnitudes are incomparable</strong><br>'
        'A $1 USD goal and a ¥1 JPY goal represent very different values.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="quality-fix"><strong>Fix:</strong> Convert all monetary values to USD using xe.com rates (11/06/2022) stored in the <code>currency_rate</code> table.</div>',
        unsafe_allow_html=True,
    )
    sql_cell(
        "tab2_qc3",
        "Verify — USD normalisation",
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
        '<div class="quality-issue"><strong>Issue 4 — Corrupted country code</strong><br>'
        'Country name <code>N,0&quot;</code> is an encoding artefact, not a real country.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="quality-fix"><strong>Fix:</strong> Exclude this country ID from the base view.</div>',
        unsafe_allow_html=True,
    )
    sql_cell(
        "tab2_qc4",
        "Verify — corrupted country excluded",
        """SELECT co.name AS country, COUNT(*) AS campaigns
FROM v_campaign_info v
JOIN country co ON v.country_id = co.id
WHERE co.name LIKE '%N,0%'""",
        description="Should return 0 rows after the fix is applied.",
        editable=True,
        auto_run=True,
    )

    # ── Analytical table ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        """
        <div class="insight-callout">
            <strong>Analytical table: <code>v_condensed</code></strong><br>
            All four fixes are applied, campaign duration is computed in days, and all monetary
            values are converted to USD. Every analysis in the subsequent tabs queries this view.
        </div>
        """,
        unsafe_allow_html=True,
    )
    sql_cell(
        "tab2_condensed",
        "v_condensed — the analytical base table",
        """SELECT v.id,
       v.name,
       cat.name   AS category,
       sc.name    AS sub_category,
       co.name    AS country,
       v.outcome,
       v.backers,
       v.days,
       v.usd_goal,
       v.usd_pledged,
       ROUND(v.usd_pledged / NULLIF(v.backers, 0), 2) AS usd_per_backer
FROM v_condensed v
JOIN sub_category sc  ON v.sub_category_id = sc.id
JOIN category cat     ON sc.category_id    = cat.id
JOIN country co       ON v.country_id      = co.id
ORDER BY v.usd_pledged DESC
LIMIT 50""",
        description="Clean analytical table: quality-filtered, duration in days, all amounts in USD.",
        editable=True,
        auto_run=True,
    )
