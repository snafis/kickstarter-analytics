import plotly.graph_objects as go
import pandas as pd

from styles.theme import COLORS, PLOTLY_LAYOUT


def campaign_duration(df: pd.DataFrame) -> go.Figure:
    """Line chart: average raised vs campaign duration with sweet-spot shading."""
    fig = go.Figure()

    # Sweet-spot shaded region (31–61 days)
    fig.add_vrect(
        x0=31, x1=61,
        fillcolor=COLORS["accent_bg"],
        opacity=1.0,
        line_width=0,
        layer="below",
        annotation_text="Sweet spot",
        annotation_position="top left",
        annotation=dict(font_size=11, font_color=COLORS["accent_mid"]),
    )

    # Main line
    fig.add_trace(go.Scatter(
        x=df["duration"],
        y=df["avg_raised"],
        mode="lines+markers",
        name="Avg raised (USD)",
        line=dict(color=COLORS["primary"], width=2.5),
        marker=dict(size=4, color=COLORS["primary"]),
        hovertemplate="Duration: %{x}d<br>Avg Raised: $%{y:,.0f}<extra></extra>",
    ))

    layout = dict(PLOTLY_LAYOUT)
    layout.update(
        title="Campaign Duration vs Average Amount Raised",
        xaxis=dict(title="Campaign Duration (days)", **PLOTLY_LAYOUT["xaxis"]),
        yaxis=dict(title="Avg Raised (USD)", tickformat="$,.0f", **PLOTLY_LAYOUT["yaxis"]),
        showlegend=False,
    )
    fig.update_layout(**layout)
    return fig
