import plotly.graph_objects as go
import pandas as pd

from styles.theme import COLORS, PLOTLY_LAYOUT


def geographic_bar(df: pd.DataFrame) -> go.Figure:
    """Grouped bar: top countries by total pledged and campaign count."""
    fig = go.Figure()

    # US gets accent; all other countries get muted tint (Tufte accent principle)
    pledged_colors = [
        COLORS["primary"] if c == "US" else COLORS["accent_muted"]
        for c in df["country"]
    ]
    count_colors = [
        COLORS["primary"] if c == "US" else COLORS["accent_bg"]
        for c in df["country"]
    ]

    fig.add_trace(go.Bar(
        name="Total Pledged (USD)",
        x=df["country"],
        y=df["total_pledged"],
        marker_color=pledged_colors,
        yaxis="y",
        hovertemplate="%{x}<br>Pledged: $%{y:,.0f}<extra></extra>",
    ))

    fig.add_trace(go.Bar(
        name="Campaign Count",
        x=df["country"],
        y=df["campaign_count"],
        marker_color=count_colors,
        yaxis="y2",
        hovertemplate="%{x}<br>Campaigns: %{y:,}<extra></extra>",
    ))

    layout = dict(PLOTLY_LAYOUT)
    layout.update(
        title="Top Countries — Total Pledged vs Campaign Count",
        barmode="group",
        xaxis=dict(title="Country", **PLOTLY_LAYOUT["xaxis"]),
        yaxis=dict(title="Total Pledged (USD)", tickformat="$,.0f", **PLOTLY_LAYOUT["yaxis"]),
        yaxis2=dict(
            title="Campaign Count",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        legend=dict(orientation="h", y=1.1, x=0),
    )
    fig.update_layout(**layout)
    return fig
