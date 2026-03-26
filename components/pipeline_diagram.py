"""SVG data pipeline schematic."""

import streamlit as st


def pipeline_diagram() -> None:
    """Render an SVG showing the data pipeline flow."""
    svg = """
    <div style="overflow-x:auto; padding:16px 0;">
    <svg width="720" height="80" viewBox="0 0 720 80" xmlns="http://www.w3.org/2000/svg"
         style="font-family:-apple-system,'SF Pro Text',sans-serif;">

      <!-- Step 1: Web / Kaggle -->
      <rect x="10" y="20" width="140" height="40" rx="8" fill="#F5F5F7" stroke="#D2D2D7" stroke-width="1.5"/>
      <text x="80" y="36" text-anchor="middle" fill="#1D1D1F" font-size="12" font-weight="600">Kaggle Dataset</text>
      <text x="80" y="52" text-anchor="middle" fill="#6E6E73" font-size="11">ks-projects-201801.csv</text>

      <!-- Arrow 1 -->
      <line x1="150" y1="40" x2="190" y2="40" stroke="#D2D2D7" stroke-width="1.5" marker-end="url(#arrow)"/>

      <!-- Step 2: CSV Files -->
      <rect x="190" y="20" width="140" height="40" rx="8" fill="#F5F5F7" stroke="#D2D2D7" stroke-width="1.5"/>
      <text x="260" y="36" text-anchor="middle" fill="#1D1D1F" font-size="12" font-weight="600">CSV Files</text>
      <text x="260" y="52" text-anchor="middle" fill="#6E6E73" font-size="11">~378K raw rows</text>

      <!-- Arrow 2 -->
      <line x1="330" y1="40" x2="370" y2="40" stroke="#D2D2D7" stroke-width="1.5" marker-end="url(#arrow)"/>

      <!-- Step 3: SQLite DB -->
      <rect x="370" y="20" width="140" height="40" rx="8" fill="#EBF4FF" stroke="#007AFF" stroke-width="1.5"/>
      <text x="440" y="36" text-anchor="middle" fill="#007AFF" font-size="12" font-weight="600">SQLite Database</text>
      <text x="440" y="52" text-anchor="middle" fill="#5856D6" font-size="11">5 normalized tables</text>

      <!-- Arrow 3 -->
      <line x1="510" y1="40" x2="550" y2="40" stroke="#D2D2D7" stroke-width="1.5" marker-end="url(#arrow)"/>

      <!-- Step 4: Streamlit -->
      <rect x="550" y="20" width="155" height="40" rx="8" fill="#F0FFF4" stroke="#34C759" stroke-width="1.5"/>
      <text x="627" y="36" text-anchor="middle" fill="#1D1D1F" font-size="12" font-weight="600">Python / Streamlit</text>
      <text x="627" y="52" text-anchor="middle" fill="#6E6E73" font-size="11">pandas · plotly · SQL</text>

      <!-- Arrow marker definition -->
      <defs>
        <marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
          <path d="M0,0 L0,6 L8,3 z" fill="#D2D2D7"/>
        </marker>
      </defs>
    </svg>
    </div>
    """
    st.markdown(svg, unsafe_allow_html=True)
