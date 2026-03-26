import plotly.graph_objects as go
import pandas as pd
import numpy as np

from styles.theme import COLORS, PLOTLY_LAYOUT


def scatter_goal_pledged(df: pd.DataFrame) -> go.Figure:
    """Log-log scatter of USD goal vs USD pledged, coloured by outcome."""
    success = df[df["outcome"] == "successful"]
    failed = df[df["outcome"] == "failed"]

    fig = go.Figure()

    fig.add_trace(go.Scattergl(
        x=failed["USD_goal"],
        y=failed["USD_pledged"],
        mode="markers",
        name="Failed",
        marker=dict(color=COLORS["danger"], size=3, opacity=0.35),
        hovertemplate="Goal: $%{x:,.0f}<br>Pledged: $%{y:,.0f}<extra>Failed</extra>",
    ))

    fig.add_trace(go.Scattergl(
        x=success["USD_goal"],
        y=success["USD_pledged"],
        mode="markers",
        name="Successful",
        marker=dict(color=COLORS["success"], size=3, opacity=0.45),
        hovertemplate="Goal: $%{x:,.0f}<br>Pledged: $%{y:,.0f}<extra>Successful</extra>",
    ))

    # Reference diagonal (goal == pledged)
    axis_range = [1, 10_000_000]
    fig.add_trace(go.Scatter(
        x=axis_range,
        y=axis_range,
        mode="lines",
        name="Goal = Pledged",
        line=dict(color=COLORS["border"], dash="dash", width=1.5),
        hoverinfo="skip",
    ))

    layout = dict(PLOTLY_LAYOUT)
    layout.update(
        title="Goal vs Pledged (USD, log scale)",
        xaxis=dict(type="log", title="Goal (USD)", **PLOTLY_LAYOUT["xaxis"]),
        yaxis=dict(type="log", title="Pledged (USD)", **PLOTLY_LAYOUT["yaxis"]),
        legend=dict(orientation="h", y=1.08, x=0),
    )
    fig.update_layout(**layout)
    return fig
