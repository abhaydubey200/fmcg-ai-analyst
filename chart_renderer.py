import plotly.express as px
import streamlit as st

def render_chart(df, chart):
    if chart["chart_type"] == "bar":
        fig = px.bar(df, x=chart["x_axis"], y=chart["y_axis"], title=chart["title"])
    elif chart["chart_type"] == "line":
        fig = px.line(df, x=chart["x_axis"], y=chart["y_axis"], title=chart["title"])
    else:
        return
    st.plotly_chart(fig, use_container_width=True)
    st.caption(chart["business_reason"])
