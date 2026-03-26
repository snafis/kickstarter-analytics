COLORS = {
    # ── Single-hue accent (Tufte: one colour used purposefully against white) ──
    "primary":  "#1D3557",   # dark navy — primary data / success / positive end
    "accent_mid": "#6B98BC", # mid tint — secondary / paired series
    "accent_bg":    "#EAF2F8", # near-white tint — background highlights (sweet spot)
    "accent_muted": "#B8CEDF", # light tint — non-highlighted bars

    # ── Diverging negative end (failure only) ────────────────────────────────
    "danger":   "#C0392B",   # brick red — failure / negative end

    # ── Legacy aliases used by visualization files ────────────────────────────
    "success":  "#1D3557",   # same as primary — success dots in scatter/histogram
    "indigo":   "#6B98BC",   # same as accent_mid — geographic campaign count bars
    "orange":   "#1D3557",   # same as primary — duration sweet-spot annotation

    # ── Neutral / structural ─────────────────────────────────────────────────
    "text":           "#1D1D1F",
    "secondary_text": "#6E6E73",
    "surface":        "#F5F5F7",
    "border":         "#D2D2D7",
    "border_light":   "#E5E5EA",
}

PLOTLY_LAYOUT = dict(
    font_family="Lato, sans-serif",
    font_color="#1D1D1F",
    title_font_family="'Playfair Display', Georgia, serif",
    paper_bgcolor="white",
    plot_bgcolor="white",
    xaxis=dict(showgrid=False, linecolor="#E5E5EA", linewidth=1),
    yaxis=dict(showgrid=True, gridcolor="#F5F5F7", linecolor="#E5E5EA"),
    margin=dict(l=40, r=20, t=60, b=40),
    hoverlabel=dict(
        bgcolor="white",
        bordercolor="#E5E5EA",
        font_family="Georgia, serif",
        font_size=13,
    ),
)
