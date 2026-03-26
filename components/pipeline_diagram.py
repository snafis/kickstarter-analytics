"""Three-system data architecture diagram: Source → Database → Analytics Workbench."""

import streamlit as st


def pipeline_diagram() -> None:
    """Render a three-system architecture diagram."""
    st.markdown(
        """
        <div style="overflow-x:auto; padding:16px 0 24px 0;">
        <svg width="720" height="140" viewBox="0 0 720 140" xmlns="http://www.w3.org/2000/svg"
             style="font-family:'Lato',sans-serif;">
          <defs>
            <marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
              <path d="M0,0 L0,6 L8,3 z" fill="#1D1D1F"/>
            </marker>
          </defs>

          <!-- Box 1: Source Data -->
          <rect x="0" y="10" width="200" height="115" rx="0" fill="#FFFFFF" stroke="#C8C8CC" stroke-width="1"/>
          <text x="100" y="30" text-anchor="middle" fill="#1D1D1F" font-size="9" font-weight="700" letter-spacing="2">SOURCE DATA</text>
          <line x1="14" y1="36" x2="186" y2="36" stroke="#E5E5EA" stroke-width="1"/>
          <text x="100" y="55" text-anchor="middle" fill="#6E6E73" font-size="10">kickstarter.com</text>
          <text x="100" y="70" text-anchor="middle" fill="#6E6E73" font-size="10">Kaggle Dataset</text>
          <text x="100" y="85" text-anchor="middle" fill="#AEAEB2" font-size="10">378,661 campaigns</text>
          <text x="100" y="114" text-anchor="middle" fill="#AEAEB2" font-size="9" letter-spacing="1">COLLECTION</text>

          <!-- Arrow 1 -->
          <line x1="200" y1="67" x2="253" y2="67" stroke="#1D1D1F" stroke-width="1" marker-end="url(#arr)"/>

          <!-- Box 2: Database (heavier border — central system) -->
          <rect x="260" y="10" width="200" height="115" rx="0" fill="#FFFFFF" stroke="#1D1D1F" stroke-width="1.5"/>
          <text x="360" y="30" text-anchor="middle" fill="#1D1D1F" font-size="9" font-weight="700" letter-spacing="2">DATABASE</text>
          <line x1="274" y1="36" x2="446" y2="36" stroke="#E5E5EA" stroke-width="1"/>
          <text x="360" y="55" text-anchor="middle" fill="#6E6E73" font-size="10">SQLite</text>
          <text x="360" y="70" text-anchor="middle" fill="#6E6E73" font-size="10">5 normalised tables</text>
          <text x="360" y="85" text-anchor="middle" fill="#AEAEB2" font-size="10">378,661 rows stored</text>
          <text x="360" y="114" text-anchor="middle" fill="#AEAEB2" font-size="9" letter-spacing="1">STORAGE</text>

          <!-- Arrow 2 -->
          <line x1="460" y1="67" x2="513" y2="67" stroke="#1D1D1F" stroke-width="1" marker-end="url(#arr)"/>

          <!-- Box 3: Analytics Workbench -->
          <rect x="520" y="10" width="200" height="115" rx="0" fill="#FFFFFF" stroke="#C8C8CC" stroke-width="1"/>
          <text x="620" y="30" text-anchor="middle" fill="#1D1D1F" font-size="9" font-weight="700" letter-spacing="1.5">ANALYTICS WORKBENCH</text>
          <line x1="534" y1="36" x2="706" y2="36" stroke="#E5E5EA" stroke-width="1"/>
          <text x="620" y="55" text-anchor="middle" fill="#6E6E73" font-size="10">Python / Streamlit</text>
          <text x="620" y="70" text-anchor="middle" fill="#6E6E73" font-size="10">SQL queries</text>
          <text x="620" y="85" text-anchor="middle" fill="#AEAEB2" font-size="10">pandas · plotly</text>
          <text x="620" y="114" text-anchor="middle" fill="#AEAEB2" font-size="9" letter-spacing="1">ANALYSIS</text>

        </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )
