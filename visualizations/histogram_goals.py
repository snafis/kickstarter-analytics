import plotly.graph_objects as go
import pandas as pd

from styles.theme import COLORS, PLOTLY_LAYOUT


def histogram_goals(df: pd.DataFrame) -> go.Figure:
    """Overlapping goal distribution histogram by outcome (log Y)."""
    success = df[df["outcome"] == "successful"]["usd_goal"]
    failed = df[df["outcome"] == "failed"]["usd_goal"]

    fig = go.Figure()

    # Failed rendered first (behind), muted — provides context
    fig.add_trace(go.Histogram(
        x=failed,
        name="Failed",
        marker_color=COLORS["accent_muted"],
        opacity=0.9,
        xbins=dict(start=0, end=500_000, size=10_000),
        hovertemplate="Goal range: $%{x:,.0f}<br>Count: %{y}<extra>Failed</extra>",
    ))

    # Successful rendered on top, accent — carries the argument
    fig.add_trace(go.Histogram(
        x=success,
        name="Successful",
        marker_color=COLORS["primary"],
        opacity=0.9,
        xbins=dict(start=0, end=500_000, size=10_000),
        hovertemplate="Goal range: $%{x:,.0f}<br>Count: %{y}<extra>Successful</extra>",
    ))

    layout = dict(PLOTLY_LAYOUT)
    layout.update(
        title="Campaign Goal Distribution by Outcome (capped $500K)",
        barmode="overlay",
        xaxis=dict(title="Goal (USD)", tickformat="$,.0f", **PLOTLY_LAYOUT["xaxis"]),
        yaxis=dict(type="log", title="Count (log scale)", **PLOTLY_LAYOUT["yaxis"]),
        legend=dict(orientation="h", y=1.08, x=0),
    )
    fig.update_layout(**layout)
    return fig
