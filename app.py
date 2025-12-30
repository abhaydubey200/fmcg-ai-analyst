import streamlit as st

# Ingestion
from src.ingestion.file_loader import load_file

# Preprocessing (ROOT-LEVEL FILES)
from data_profiler import profile_data
from auto_cleaner import get_cleaning_rules
from transformer import apply_cleaning_rules
from feature_engineering import add_features

# Analysis
from kpi_engine import detect_kpis_ai, execute_kpis

# Visualization
from chart_selector_ai import detect_charts_ai
from dashboard import show_kpis, show_charts

# AI Insights
from insight_generator import generate_insights


# ---------------- STREAMLIT CONFIG ----------------
st.set_page_config(
    page_title="FMCG AI Analyst",
    layout="wide"
)

st.title("🤖 FMCG AI Data Analyst Platform")
st.caption("AI-powered automatic data cleaning, KPI detection & chart generation")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload FMCG CSV or Excel file",
    type=["csv", "xlsx"]
)

# ---------------- MAIN PIPELINE ----------------
if uploaded_file:
    try:
        # Load
        df = load_file(uploaded_file)
        st.success("✅ File loaded successfully")

        # Profile
        profile = profile_data(df)

        # AI Cleaning Rules
        with st.spinner("🧹 AI generating data cleaning rules..."):
            cleaning_rules = get_cleaning_rules(profile)

        with st.expander("🔍 AI Cleaning Rules"):
            st.json(cleaning_rules)

        # Apply Cleaning
        df = apply_cleaning_rules(df, cleaning_rules)

        # Feature Engineering
        df = add_features(df)

        # KPI Detection
        with st.spinner("📊 AI detecting KPIs..."):
            kpis = detect_kpis_ai(df)

        kpi_results = execute_kpis(df, kpis)

        st.subheader("📌 Key Business KPIs")
        show_kpis(kpi_results)

        # AI Chart Selection
        with st.spinner("📈 AI selecting best charts..."):
            charts = detect_charts_ai(df, kpi_results)

        st.subheader("📊 AI-Selected Charts")
        show_charts(df, charts)

        # AI Insights
        st.subheader("🧠 Executive Insights")
        insights = generate_insights(kpi_results)
        st.write(insights)

    except Exception as e:
        st.error("❌ Something went wrong")
        st.exception(e)
