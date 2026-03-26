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

    # Rank-based opacity
    n = len(df_sorted)
    opacities = [0.4 + 0.6 * (i / max(n - 1, 1)) for i in range(n)]

    fig = go.Figure(go.Bar(
        x=df_sorted[col],
        y=df_sorted["category"],
        orientation="h",
        marker=dict(
            color=[COLORS["primary"]] * n,
            opacity=opacities,
        ),
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
