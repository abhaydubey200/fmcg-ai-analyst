import streamlit as st
from src.ingestion.file_loader import load_file
from auto_cleaner import get_cleaning_rules
from data_profiler import profile_data

st.set_page_config(page_title="FMCG AI Analyst", layout="wide")

st.title("📊 FMCG AI Analyst")

uploaded_file = st.file_uploader(
    "Upload your FMCG dataset (CSV or Excel)",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file:
    try:
        df = load_file(uploaded_file)
        st.success("File loaded successfully!")
        st.dataframe(df.head())

        profile = profile_data(df)
        st.subheader("📋 Data Profile")
        st.json(profile)

        cleaning_rules = get_cleaning_rules(profile)
        st.subheader("🧹 AI Suggested Cleaning Rules")
        st.write(cleaning_rules)

    except Exception as e:
        st.error(str(e))
        st.stop()
