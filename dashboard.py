import streamlit as st
from chart_renderer import render_chart


def show_kpis(kpis: dict):
    if not kpis:
        st.warning("No KPIs detected")
        return

    cols = st.columns(len(kpis))
    for col, (name, value) in zip(cols, kpis.items()):
        col.metric(name, round(value, 2) if isinstance(value, (int, float)) else value)


def show_charts(df, charts: list):
    if not charts:
        st.warning("No charts selected by AI")
        return

    for chart in charts:
        render_chart(df, chart)
