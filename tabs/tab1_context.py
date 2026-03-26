"""Tab 1 — Context: business narrative, dataset stats, schema, data preview."""

import streamlit as st

from components.metric_card import metric_card
from components.sql_cell import sql_cell
from db.executor import run_query


def render() -> None:
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-title">What makes a Kickstarter campaign succeed?</div>
            <div class="hero-subtitle">
                ~60% of Kickstarter campaigns fail to reach their funding goal.<br>
                This analysis examines 378,000+ campaigns to find the patterns that separate winners from losers —
                covering goals, categories, geography, and campaign duration.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Dataset stats ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Dataset at a Glance</div>', unsafe_allow_html=True)

    try:
        total = run_query("SELECT COUNT(*) AS n FROM campaign").iloc[0]["n"]
        cats = run_query("SELECT COUNT(*) AS n FROM category").iloc[0]["n"]
        countries = run_query("SELECT COUNT(*) AS n FROM country").iloc[0]["n"]
        dates = run_query(
            "SELECT MIN(launched) AS start, MAX(launched) AS end FROM campaign"
        ).iloc[0]
        date_range = f"{str(dates['start'])[:7]} – {str(dates['end'])[:7]}"
    except Exception:
        total, cats, countries, date_range = "–", "–", "–", "–"

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card(f"{total:,}" if isinstance(total, int) else total, "Total Campaigns")
    with c2:
        metric_card(date_range, "Date Range", color="#5856D6")
    with c3:
        metric_card(str(cats), "Categories", color="#34C759")
    with c4:
        metric_card(str(countries), "Countries", color="#FF9500")

    st.markdown("---")

    # ── Schema ─────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Database Schema</div>', unsafe_allow_html=True)
    st.markdown(
        "Five normalised tables enable clean, efficient queries without data duplication.",
        unsafe_allow_html=False,
    )

    schema_svg = """
    <div style="overflow-x:auto;padding:12px 0;">
    <svg width="760" height="200" viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg"
         style="font-family:-apple-system,'SF Pro Text',sans-serif;">

      <!-- campaign (centre) -->
      <rect x="290" y="60" width="180" height="90" rx="8" fill="#EBF4FF" stroke="#007AFF" stroke-width="1.5"/>
      <text x="380" y="80" text-anchor="middle" fill="#007AFF" font-size="13" font-weight="600">campaign</text>
      <text x="380" y="97"  text-anchor="middle" fill="#1D1D1F" font-size="11">id · name · goal · pledged</text>
      <text x="380" y="112" text-anchor="middle" fill="#1D1D1F" font-size="11">backers · outcome</text>
      <text x="380" y="127" text-anchor="middle" fill="#1D1D1F" font-size="11">launched · deadline</text>
      <text x="380" y="142" text-anchor="middle" fill="#6E6E73" font-size="10">sub_category_id · country_id · currency_id</text>

      <!-- sub_category -->
      <rect x="60" y="20" width="150" height="55" rx="8" fill="#F5F5F7" stroke="#D2D2D7" stroke-width="1.5"/>
      <text x="135" y="40" text-anchor="middle" fill="#1D1D1F" font-size="12" font-weight="600">sub_category</text>
      <text x="135" y="57" text-anchor="middle" fill="#6E6E73" font-size="11">id · name · category_id</text>
      <line x1="210" y1="48" x2="290" y2="90" stroke="#D2D2D7" stroke-width="1" stroke-dasharray="4,3"/>

      <!-- category -->
      <rect x="60" y="110" width="150" height="45" rx="8" fill="#F5F5F7" stroke="#D2D2D7" stroke-width="1.5"/>
      <text x="135" y="130" text-anchor="middle" fill="#1D1D1F" font-size="12" font-weight="600">category</text>
      <text x="135" y="147" text-anchor="middle" fill="#6E6E73" font-size="11">id · name</text>
      <line x1="210" y1="133" x2="290" y2="120" stroke="#D2D2D7" stroke-width="1" stroke-dasharray="4,3"/>

      <!-- country -->
      <rect x="550" y="20" width="150" height="45" rx="8" fill="#F5F5F7" stroke="#D2D2D7" stroke-width="1.5"/>
      <text x="625" y="40" text-anchor="middle" fill="#1D1D1F" font-size="12" font-weight="600">country</text>
      <text x="625" y="57" text-anchor="middle" fill="#6E6E73" font-size="11">id · name</text>
      <line x1="550" y1="43" x2="470" y2="90" stroke="#D2D2D7" stroke-width="1" stroke-dasharray="4,3"/>

      <!-- currency -->
      <rect x="550" y="110" width="150" height="45" rx="8" fill="#F5F5F7" stroke="#D2D2D7" stroke-width="1.5"/>
      <text x="625" y="130" text-anchor="middle" fill="#1D1D1F" font-size="12" font-weight="600">currency</text>
      <text x="625" y="147" text-anchor="middle" fill="#6E6E73" font-size="11">id · name</text>
      <line x1="550" y1="133" x2="470" y2="120" stroke="#D2D2D7" stroke-width="1" stroke-dasharray="4,3"/>

    </svg>
    </div>
    """
    st.markdown(schema_svg, unsafe_allow_html=True)

    st.markdown("---")

    # ── Data preview ───────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Data Preview</div>', unsafe_allow_html=True)
    sql_cell(
        cell_id="tab1_preview",
        label="Sample campaign rows",
        description="Explore the raw campaign data with all joined lookup columns.",
        sql="""SELECT c.id, c.name, c.outcome, c.goal, c.pledged, c.backers,
       s.name AS sub_category, cat.name AS category,
       co.name AS country, cu.name AS currency,
       c.launched, c.deadline
FROM campaign c
JOIN sub_category s ON c.sub_category_id = s.id
JOIN category cat ON s.category_id = cat.id
JOIN country co ON c.country_id = co.id
JOIN currency cu ON c.currency_id = cu.id
LIMIT 50""",
        editable=False,
        auto_run=True,
    )
