"""Interactive SQL cell component for educational query exploration."""

from __future__ import annotations

import streamlit as st

from db.executor import safe_run


def sql_cell(
    cell_id: str,
    label: str,
    sql: str,
    description: str = "",
    insight: str = "",
    editable: bool = True,   # kept for API compatibility; always editable now
    auto_run: bool = False,  # kept for API compatibility; ignored
) -> None:
    """
    Render an interactive SQL cell.

    Parameters
    ----------
    cell_id:     Unique key prefix for session state.
    label:       Section heading displayed above the editor.
    sql:         Default SQL text.
    description: Gray helper text shown below the heading.
    insight:     Optional callout text rendered after the result table.
    editable/auto_run: kept for backwards-compatibility, no longer used.
    """
    sql_key = f"sql_{cell_id}"
    result_key = f"result_{cell_id}"
    error_key = f"error_{cell_id}"

    if sql_key not in st.session_state:
        st.session_state[sql_key] = sql.strip()

    st.markdown(f"**{label}**")
    if description:
        st.markdown(
            f'<p style="color:#6E6E73;font-size:14px;margin-top:-8px">{description}</p>',
            unsafe_allow_html=True,
        )

    st.session_state[sql_key] = st.text_area(
        label="SQL",
        value=st.session_state[sql_key],
        key=f"area_{cell_id}",
        height=160,
        label_visibility="collapsed",
    )

    col_btn, col_info = st.columns([1, 5])
    run_clicked = col_btn.button("▶ Run Query", key=f"btn_{cell_id}")

    if run_clicked:
        df, err = safe_run(st.session_state[sql_key])
        if err:
            st.session_state[error_key] = err
            st.session_state.pop(result_key, None)
        else:
            st.session_state[result_key] = df
            st.session_state.pop(error_key, None)

    # Only render results after an explicit Run click
    if error_key in st.session_state:
        st.error(f"SQL Error: {st.session_state[error_key]}")
    elif result_key in st.session_state:
        df = st.session_state[result_key]
        col_info.markdown(
            f'<span style="color:#6E6E73;font-size:13px;line-height:2.2">{len(df):,} rows</span>',
            unsafe_allow_html=True,
        )
        st.dataframe(df, use_container_width=True)

        if insight:
            st.markdown(
                f'<div class="insight-callout">{insight}</div>',
                unsafe_allow_html=True,
            )
