"""Tab 1 — Context: problem framing, data understanding, field requirements."""

import streamlit as st


def render() -> None:
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-title">What makes a Kickstarter campaign successful?</div>
            <div class="hero-subtitle">
                It's a common misconception that most campaigns reach their funding goal, but in reality, only about 60% do.
                This analysis delves into over 378,000 campaigns to uncover the key patterns that distinguish successful ones from unsuccessful ones.
                We examine various factors including goals, categories, geography, and campaign duration.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── The Brief ──────────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">The Brief</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="border-left:2px solid #1D1D1F; padding-left:20px; margin:0 0 36px 0;">
            <p style="font-size:15px; line-height:1.8; color:#3A3A3C; margin:0;">
                We are the executive team of a small board game company setting up our first Kickstarter campaign.
                We have ambitions of expanding the business and would like to maximise our funding.
                We need data-driven recommendations to inform three critical decisions before we launch.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Three Questions ────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Three Questions</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="display:flex; flex-direction:column; gap:0; margin-bottom:36px;">

          <div style="display:flex; gap:28px; padding:20px 0; border-bottom:1px solid #E5E5EA; align-items:flex-start;">
            <div style="font-family:'Lato',sans-serif; font-size:10px; font-weight:700; letter-spacing:0.12em; color:#AEAEB2; padding-top:5px; min-width:20px;">01</div>
            <div>
              <div style="font-family:'Playfair Display',Georgia,serif; font-size:18px; font-weight:700; color:#1D1D1F; margin-bottom:5px;">What is a realistic campaign goal?</div>
              <div style="font-family:'Lato',sans-serif; font-size:14px; color:#6E6E73; line-height:1.65;">What dollar amount should the company aim to raise, based on what successful board game campaigns typically target?</div>
            </div>
          </div>

          <div style="display:flex; gap:28px; padding:20px 0; border-bottom:1px solid #E5E5EA; align-items:flex-start;">
            <div style="font-family:'Lato',sans-serif; font-size:10px; font-weight:700; letter-spacing:0.12em; color:#AEAEB2; padding-top:5px; min-width:20px;">02</div>
            <div>
              <div style="font-family:'Playfair Display',Georgia,serif; font-size:18px; font-weight:700; color:#1D1D1F; margin-bottom:5px;">How many backers will be needed to meet that goal?</div>
              <div style="font-family:'Lato',sans-serif; font-size:14px; color:#6E6E73; line-height:1.65;">Given the goal, how many backers are required — derived from average pledge-per-backer benchmarks in the tabletop games category?</div>
            </div>
          </div>

          <div style="display:flex; gap:28px; padding:20px 0; align-items:flex-start;">
            <div style="font-family:'Lato',sans-serif; font-size:10px; font-weight:700; letter-spacing:0.12em; color:#AEAEB2; padding-top:5px; min-width:20px;">03</div>
            <div>
              <div style="font-family:'Playfair Display',Georgia,serif; font-size:18px; font-weight:700; color:#1D1D1F; margin-bottom:5px;">How many backers can the company realistically expect?</div>
              <div style="font-family:'Lato',sans-serif; font-size:14px; color:#6E6E73; line-height:1.65;">Based on historical trends in the tabletop games category, what backer count is achievable for a first-time campaign?</div>
            </div>
          </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Analytical Framework (Issue Tree) ─────────────────────────────────────
    st.markdown('<div class="section-heading">Analytical Framework</div>', unsafe_allow_html=True)
    st.markdown(
        "An issue tree decomposes the central objective into the three measurable sub-questions "
        "and the data analyses required to answer each.",
    )
    st.markdown("""
        <div style="overflow-x:auto; padding:16px 0 28px 0;">
        <svg width="780" height="280" viewBox="0 0 780 280" xmlns="http://www.w3.org/2000/svg"
             style="font-family:'Lato',sans-serif;">

          <rect x="10" y="105" width="130" height="70" rx="0" fill="#FFFFFF" stroke="#1D1D1F" stroke-width="1.5"/>
          <text x="75" y="130" text-anchor="middle" fill="#1D1D1F" font-size="9" font-weight="700" letter-spacing="2">MAXIMISE</text>
          <text x="75" y="145" text-anchor="middle" fill="#1D1D1F" font-size="9" font-weight="700" letter-spacing="2">CAMPAIGN</text>
          <text x="75" y="160" text-anchor="middle" fill="#1D1D1F" font-size="9" font-weight="700" letter-spacing="2">FUNDING</text>

          <line x1="140" y1="140" x2="175" y2="140" stroke="#1D1D1F" stroke-width="1"/>
          <line x1="175" y1="50"  x2="175" y2="232" stroke="#1D1D1F" stroke-width="1"/>
          <line x1="175" y1="50"  x2="210" y2="50"  stroke="#1D1D1F" stroke-width="1"/>
          <line x1="175" y1="140" x2="210" y2="140" stroke="#1D1D1F" stroke-width="1"/>
          <line x1="175" y1="232" x2="210" y2="232" stroke="#1D1D1F" stroke-width="1"/>

          <rect x="210" y="25" width="160" height="50" rx="0" fill="#FFFFFF" stroke="#C8C8CC" stroke-width="1"/>
          <text x="290" y="43" text-anchor="middle" fill="#1D1D1F" font-size="9" font-weight="700" letter-spacing="1.5">01 — GOAL SETTING</text>
          <text x="290" y="58" text-anchor="middle" fill="#6E6E73" font-size="10">What goal to aim for?</text>
          <line x1="370" y1="50"  x2="405" y2="50"  stroke="#C8C8CC" stroke-width="1"/>
          <line x1="405" y1="35"  x2="405" y2="65"  stroke="#C8C8CC" stroke-width="1"/>
          <line x1="405" y1="35"  x2="420" y2="35"  stroke="#C8C8CC" stroke-width="1"/>
          <line x1="405" y1="65"  x2="420" y2="65"  stroke="#C8C8CC" stroke-width="1"/>
          <text x="426" y="39" fill="#3A3A3C" font-size="10">Goal distribution in board games</text>
          <text x="426" y="69" fill="#3A3A3C" font-size="10">Success rate by goal size bracket</text>

          <rect x="210" y="115" width="160" height="50" rx="0" fill="#FFFFFF" stroke="#C8C8CC" stroke-width="1"/>
          <text x="290" y="133" text-anchor="middle" fill="#1D1D1F" font-size="9" font-weight="700" letter-spacing="1.5">02 — BACKERS NEEDED</text>
          <text x="290" y="148" text-anchor="middle" fill="#6E6E73" font-size="10">How many required?</text>
          <line x1="370" y1="140" x2="405" y2="140" stroke="#C8C8CC" stroke-width="1"/>
          <line x1="405" y1="125" x2="405" y2="155" stroke="#C8C8CC" stroke-width="1"/>
          <line x1="405" y1="125" x2="420" y2="125" stroke="#C8C8CC" stroke-width="1"/>
          <line x1="405" y1="155" x2="420" y2="155" stroke="#C8C8CC" stroke-width="1"/>
          <text x="426" y="129" fill="#3A3A3C" font-size="10">Avg pledge per backer in category</text>
          <text x="426" y="159" fill="#3A3A3C" font-size="10">Goal ÷ avg pledge = backers required</text>

          <rect x="210" y="207" width="160" height="50" rx="0" fill="#FFFFFF" stroke="#C8C8CC" stroke-width="1"/>
          <text x="290" y="225" text-anchor="middle" fill="#1D1D1F" font-size="9" font-weight="700" letter-spacing="1.5">03 — BACKERS EXPECTED</text>
          <text x="290" y="240" text-anchor="middle" fill="#6E6E73" font-size="10">What's realistic?</text>
          <line x1="370" y1="232" x2="405" y2="232" stroke="#C8C8CC" stroke-width="1"/>
          <line x1="405" y1="217" x2="405" y2="247" stroke="#C8C8CC" stroke-width="1"/>
          <line x1="405" y1="217" x2="420" y2="217" stroke="#C8C8CC" stroke-width="1"/>
          <line x1="405" y1="247" x2="420" y2="247" stroke="#C8C8CC" stroke-width="1"/>
          <text x="426" y="221" fill="#3A3A3C" font-size="10">Historical backer counts in tabletop</text>
          <text x="426" y="251" fill="#3A3A3C" font-size="10">Campaign duration &amp; timing effects</text>

        </svg>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Data Understanding ─────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Data Understanding</div>', unsafe_allow_html=True)
    st.markdown(
        "Before collecting data we need to understand what a Kickstarter campaign page "
        "actually surfaces. Each campaign exposes a structured set of fields — goal, pledged amount, "
        "backer count, dates, category, and location — that map directly to our three questions."
    )

    # Annotated campaign page mockup — uses st.html() to avoid Streamlit's SVG sanitiser
    st.html("""
        <div style="overflow-x:auto; padding:16px 0 4px 0; font-family:'Lato',sans-serif;">
        <svg width="740" height="318" viewBox="0 0 740 318" xmlns="http://www.w3.org/2000/svg">

          <!-- Browser chrome -->
          <rect x="0" y="0" width="740" height="32" rx="4" fill="#F5F5F7" stroke="#E5E5EA" stroke-width="1"/>
          <circle cx="16" cy="16" r="4.5" fill="#D2D2D7"/>
          <circle cx="30" cy="16" r="4.5" fill="#D2D2D7"/>
          <circle cx="44" cy="16" r="4.5" fill="#D2D2D7"/>
          <rect x="62" y="7" width="616" height="18" rx="9" fill="#E5E5EA"/>
          <text x="370" y="20" text-anchor="middle" fill="#AEAEB2" font-size="10">kickstarter.com/projects/pawmination/pawmination-a-fun-new-tabletop-game</text>

          <!-- Page bg -->
          <rect x="0" y="32" width="740" height="286" fill="#FFFFFF" stroke="#E5E5EA" stroke-width="1"/>

          <!-- Campaign image placeholder -->
          <rect x="14" y="46" width="112" height="84" fill="#F5F5F7" stroke="#E5E5EA" stroke-width="1"/>
          <line x1="14" y1="46" x2="126" y2="130" stroke="#D2D2D7" stroke-width="0.8"/>
          <line x1="126" y1="46" x2="14"  y2="130" stroke="#D2D2D7" stroke-width="0.8"/>

          <!-- Title -->
          <text x="146" y="63"  fill="#1D1D1F" font-size="14" font-weight="700">PAWMINATION — a fun new tabletop game</text>
          <text x="146" y="76"  fill="#AEAEB2" font-size="9" letter-spacing="1">campaign.name</text>

          <!-- Category -->
          <text x="146" y="94"  fill="#6E6E73" font-size="11">Games · Tabletop Games</text>
          <text x="146" y="106" fill="#AEAEB2" font-size="9" letter-spacing="1">category.name · sub_category.name</text>

          <!-- Creator / location -->
          <text x="146" y="123" fill="#6E6E73" font-size="10">by Pawmination ·</text>
          <text x="243" y="123" fill="#1D1D1F" font-size="10" font-weight="600"> Bellevue, WA · United States</text>
          <text x="146" y="134" fill="#AEAEB2" font-size="9" letter-spacing="1">country.name · currency.name (GBP)</text>

          <!-- Progress bar ~45% funded (505/1122) -->
          <rect x="14" y="148" width="712" height="5" fill="#E5E5EA"/>
          <rect x="14" y="148" width="321" height="5" fill="#1D1D1F"/>

          <!-- Stats -->
          <text x="14"  y="169" fill="#1D1D1F" font-size="15" font-weight="700">£505</text>
          <text x="14"  y="182" fill="#6E6E73" font-size="10">pledged of £1,122 goal</text>
          <text x="14"  y="193" fill="#AEAEB2" font-size="9" letter-spacing="1">campaign.pledged</text>

          <text x="200" y="169" fill="#1D1D1F" font-size="15" font-weight="700">£1,122</text>
          <text x="200" y="182" fill="#6E6E73" font-size="10">goal</text>
          <text x="200" y="193" fill="#AEAEB2" font-size="9" letter-spacing="1">campaign.goal</text>

          <text x="340" y="169" fill="#1D1D1F" font-size="15" font-weight="700">14</text>
          <text x="340" y="182" fill="#6E6E73" font-size="10">backers</text>
          <text x="340" y="193" fill="#AEAEB2" font-size="9" letter-spacing="1">campaign.backers</text>

          <text x="440" y="169" fill="#1D1D1F" font-size="15" font-weight="700">51</text>
          <text x="440" y="182" fill="#6E6E73" font-size="10">days to go</text>
          <text x="440" y="193" fill="#AEAEB2" font-size="9" letter-spacing="1">deadline − launched</text>

          <!-- Divider -->
          <line x1="14" y1="206" x2="726" y2="206" stroke="#E5E5EA" stroke-width="1"/>

          <!-- Meta -->
          <text x="14"  y="223" fill="#6E6E73" font-size="10">Launched</text>
          <text x="76"  y="223" fill="#1D1D1F" font-size="10">Mar 26, 2026</text>
          <text x="190" y="223" fill="#AEAEB2" font-size="9" letter-spacing="1">campaign.launched</text>

          <text x="14"  y="239" fill="#6E6E73" font-size="10">Deadline</text>
          <text x="76"  y="239" fill="#1D1D1F" font-size="10">May 17, 2026  (51 days)</text>
          <text x="190" y="239" fill="#AEAEB2" font-size="9" letter-spacing="1">campaign.deadline</text>

          <!-- Outcome -->
          <rect x="14" y="254" width="52" height="20" rx="0" fill="#F5F5F7" stroke="#C8C8CC" stroke-width="1"/>
          <text x="40"  y="268" text-anchor="middle" fill="#1D1D1F" font-size="9" font-weight="700" letter-spacing="1">LIVE</text>
          <text x="74" y="268" fill="#AEAEB2" font-size="9" letter-spacing="1">campaign.outcome</text>

        </svg>
        </div>
        <p style="font-family:'Lato',sans-serif; font-size:11px; color:#AEAEB2; letter-spacing:0.05em; margin:4px 0 28px 0;">
            SOURCE — kickstarter.com/projects/pawmination/pawmination-a-fun-new-tabletop-game · fields map directly to dataset columns
        </p>
    """)

    # ── Data Requirements ──────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Data Requirements</div>', unsafe_allow_html=True)
    st.markdown(
        "Nine fields from the campaign page are sufficient to answer all three questions. "
        "They are stored across five normalised tables to eliminate redundancy."
    )

    rows = [
        ("campaign.goal",      "Target funding amount in local currency",            "Q1"),
        ("campaign.pledged",   "Total amount pledged at campaign close",              "Q1"),
        ("campaign.backers",   "Number of individual backers",                        "Q2, Q3"),
        ("campaign.outcome",   "Final status: successful, failed, cancelled, live",   "Q1, Q2, Q3"),
        ("campaign.launched",  "Campaign start date",                                 "Q3"),
        ("campaign.deadline",  "Campaign end date",                                   "Q3"),
        ("sub_category.name",  "Granular category (e.g. Tabletop Games)",             "Q3"),
        ("country.name",       "Creator's country",                                   "Context"),
        ("currency.name",      "Currency of the goal and pledged amounts",            "Q1"),
    ]

    table_rows = ""
    for i, (field, desc, answers) in enumerate(rows):
        border = "border-bottom:1px solid #F5F5F5;" if i < len(rows) - 1 else ""
        table_rows += f"""
        <div style="display:grid;grid-template-columns:220px 1fr 80px;padding:10px 0;{border}">
          <div style="font-family:'Courier New',monospace;font-size:12px;color:#1D1D1F;">{field}</div>
          <div style="font-family:'Lato',sans-serif;font-size:13px;color:#6E6E73;line-height:1.5;">{desc}</div>
          <div style="font-family:'Lato',sans-serif;font-size:11px;font-weight:700;letter-spacing:0.06em;color:#AEAEB2;">{answers}</div>
        </div>"""

    st.html(f"""
        <div style="font-family:'Lato',sans-serif;">
          <div style="display:grid;grid-template-columns:220px 1fr 80px;padding:0 0 8px 0;border-bottom:2px solid #1D1D1F;margin-bottom:2px;">
            <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#6E6E73;">FIELD</div>
            <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#6E6E73;">DESCRIPTION</div>
            <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#6E6E73;">ANSWERS</div>
          </div>
          {table_rows}
        </div>
    """)
