COLORS = {
    "primary": "#007AFF",
    "success": "#34C759",
    "danger": "#FF3B30",
    "indigo": "#5856D6",
    "orange": "#FF9500",
    "text": "#1D1D1F",
    "secondary_text": "#6E6E73",
    "surface": "#F5F5F7",
    "border": "#D2D2D7",
    "border_light": "#E5E5EA",
}

PLOTLY_LAYOUT = dict(
    font_family="-apple-system, 'SF Pro Text', sans-serif",
    font_color="#1D1D1F",
    paper_bgcolor="white",
    plot_bgcolor="white",
    xaxis=dict(showgrid=False, linecolor="#E5E5EA", linewidth=1),
    yaxis=dict(showgrid=True, gridcolor="#F5F5F7", linecolor="#E5E5EA"),
    margin=dict(l=40, r=20, t=60, b=40),
    hoverlabel=dict(
        bgcolor="white",
        bordercolor="#E5E5EA",
        font_family="-apple-system, 'SF Pro Text', sans-serif",
        font_size=13,
    ),
)
