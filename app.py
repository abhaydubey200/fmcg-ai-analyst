import streamlit as st
from src.ingestion.file_loader import load_file
from src.preprocessing.data_profiler import profile_data
from src.preprocessing.auto_cleaner import get_cleaning_rules
from src.preprocessing.transformer import apply_cleaning_rules
from src.preprocessing.feature_engineering import add_features
from src.analysis.kpi_engine import detect_kpis_ai, execute_kpis
from src.visualization.chart_selector_ai import detect_charts_ai
from src.visualization.dashboard import show_kpis, show_charts
from src.ai_engine.insight_generator import generate_insights

st.set_page_config("FMCG AI Analyst", layout="wide")
st.title("🤖 FMCG AI Data Analyst")

file = st.file_uploader("Upload FMCG Data")

if file:
    df = load_file(file)

    profile = profile_data(df)
    rules = get_cleaning_rules(profile)
    df = apply_cleaning_rules(df, rules)
    df = add_features(df)

    kpis = detect_kpis_ai(df)
    kpi_results = execute_kpis(df, kpis)

    show_kpis(kpi_results)

    charts = detect_charts_ai(df, kpi_results)
    show_charts(df, charts)

    st.subheader("🧠 AI Executive Insights")
    st.write(generate_insights(kpi_results))
