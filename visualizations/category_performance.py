import plotly.graph_objects as go
import pandas as pd
import numpy as np

from styles.theme import COLORS, PLOTLY_LAYOUT


def category_performance(df: pd.DataFrame, metric: str = "total_raised") -> go.Figure:
    """Horizontal bar chart: categories ranked by total_raised or total_backers."""
    col = metric
    label = "Total Raised (USD)" if metric == "total_raised" else "Total Backers"
    title = f"Category Performance — {label}"

    df_sorted = df.sort_values(col, ascending=True)

    # Top 3 by rank get accent; remainder get muted tint (Tufte accent principle)
    top3 = set(df_sorted.nlargest(3, col)["category"])
    bar_colors = [
        COLORS["primary"] if cat in top3 else COLORS["accent_muted"]
        for cat in df_sorted["category"]
    ]

    fig = go.Figure(go.Bar(
        x=df_sorted[col],
        y=df_sorted["category"],
        orientation="h",
        marker=dict(color=bar_colors),
        hovertemplate=f"%{{y}}<br>{label}: %{{x:,.0f}}<extra></extra>",
    ))

    layout = dict(PLOTLY_LAYOUT)
    layout.update(
        title=title,
        xaxis=dict(title=label, tickformat=",.0f", **PLOTLY_LAYOUT["xaxis"]),
        yaxis=dict(title="", **PLOTLY_LAYOUT["yaxis"]),
        height=420,
    )
    fig.update_layout(**layout)
    return fig
