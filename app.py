import streamlit as st
import pandas as pd
import plotly.express as px
from src.auto_cleaner import get_cleaning_rules, clean_data

st.set_page_config(page_title="📊 FMCG AI Analyst", layout="wide")

st.title("📊 FMCG AI Analyst Dashboard")

# ----------------------
# File Upload
# ----------------------
uploaded_file = st.file_uploader(
    "Upload your FMCG dataset (CSV or Excel)",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file:
    # Load file
    try:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.success(f"✅ File `{uploaded_file.name}` loaded successfully!")
    except Exception as e:
        st.error(f"❌ Error loading file: {e}")
        st.stop()
    
    # ----------------------
    # Data Profile
    # ----------------------
    st.subheader("📋 Data Profile")
    profile = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "dtypes": df.dtypes.apply(lambda x: str(x)).to_dict(),
        "missing_percent": (df.isna().sum() / len(df) * 100).round(2).to_dict(),
        "sample": df.head(5).to_dict(orient="records")
    }
    st.json(profile)
    
    # ----------------------
    # AI Suggested Cleaning Rules
    # ----------------------
    st.subheader("🧹 AI Suggested Cleaning Rules")
    rules = get_cleaning_rules(profile)
    st.json(rules)
    
    # ----------------------
    # Clean Data Button
    # ----------------------
    if st.button("✨ Apply Cleaning Rules & Show Dashboard"):
        df_cleaned = clean_data(df, rules)
        
        st.success("✅ Data cleaned successfully!")
        
        # ----------------------
        # Dashboard
        # ----------------------
        st.subheader("📊 FMCG Dashboard")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Total Orders by STATE**")
            if "STATE" in df_cleaned.columns:
                fig = px.bar(df_cleaned.groupby("STATE").size().reset_index(name="Orders"),
                             x="STATE", y="Orders", text="Orders")
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Total Amount by CATEGORY**")
            if "CATEGORY" in df_cleaned.columns and "AMOUNT" in df_cleaned.columns:
                fig = px.pie(df_cleaned.groupby("CATEGORY")["AMOUNT"].sum().reset_index(),
                             names="CATEGORY", values="AMOUNT")
                st.plotly_chart(fig, use_container_width=True)
        
        # Additional KPIs
        st.markdown("**Key KPIs**")
        total_orders = len(df_cleaned)
        total_amount = df_cleaned["AMOUNT"].sum() if "AMOUNT" in df_cleaned.columns else 0
        avg_order_value = total_amount / total_orders if total_orders else 0
        
        st.metric("Total Orders", total_orders)
        st.metric("Total Amount", f"{total_amount:,.2f}")
        st.metric("Average Order Value", f"{avg_order_value:,.2f}")
