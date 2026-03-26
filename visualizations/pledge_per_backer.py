import plotly.graph_objects as go
import pandas as pd

from styles.theme import COLORS, PLOTLY_LAYOUT

TOP_HIGHLIGHT = {"Games", "Technology", "Design"}


def pledge_per_backer(df: pd.DataFrame) -> go.Figure:
    """Horizontal bar: avg pledge per backer by category (successful campaigns)."""
    df = df.copy()
    df["avg_pledge"] = df["total_raised"] / df["total_backers"]
    df_sorted = df.sort_values("avg_pledge", ascending=True)

    bar_colors = [
        COLORS["primary"] if cat in TOP_HIGHLIGHT else COLORS["accent_muted"]
        for cat in df_sorted["category"]
    ]

    fig = go.Figure(go.Bar(
        x=df_sorted["avg_pledge"],
        y=df_sorted["category"],
        orientation="h",
        marker=dict(color=bar_colors),
        hovertemplate="%{y}<br>Avg pledge/backer: $%{x:,.0f}<extra></extra>",
    ))

    layout = dict(PLOTLY_LAYOUT)
    layout.update(
        title="Avg Pledge per Backer — by Category",
        xaxis=dict(title="Avg Pledge per Backer (USD)", tickformat="$,.0f", **PLOTLY_LAYOUT["xaxis"]),
        yaxis=dict(title="", **PLOTLY_LAYOUT["yaxis"]),
        height=420,
    )
    fig.update_layout(**layout)
    return fig
