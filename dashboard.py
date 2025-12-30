import streamlit as st
from src.visualization.chart_renderer import render_chart

def show_kpis(kpis):
    cols = st.columns(len(kpis))
    for col, (k, v) in zip(cols, kpis.items()):
        col.metric(k, round(v, 2))

def show_charts(df, charts):
    for chart in charts:
        render_chart(df, chart)
