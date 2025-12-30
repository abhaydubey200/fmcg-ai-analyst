import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from src.auto_cleaner import get_cleaning_rules

st.set_page_config(
    page_title="📊 FMCG AI Analyst",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📊 FMCG AI Analyst")
st.write("Upload your FMCG dataset (CSV or Excel)")

# --- File Upload ---
uploaded_file = st.file_uploader(
    "Drag and drop file here",
    type=["csv", "xlsx", "xls"],
    accept_multiple_files=False
)

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success(f"File loaded successfully! ({df.shape[0]} rows, {df.shape[1]} columns)")

        # --- DATA PROFILE ---
        st.header("📋 Data Profile")
        profile = {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "dtypes": df.dtypes.apply(lambda x: str(x)).to_dict(),
            "missing_percent": (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
            "sample": df.head(5).to_dict(orient="index")
        }

        st.json(profile)

        # --- AI Cleaning Rules ---
        st.header("🧹 AI Suggested Cleaning Rules")
        cleaning_rules = get_cleaning_rules(profile)
        st.markdown(cleaning_rules)

        # --- INTERACTIVE DASHBOARD ---
        st.header("📊 FMCG Analytics Dashboard")

        # Select columns for KPI display
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

        kpi_col1.metric("Total Orders", df['ORDER_ID'].nunique() if 'ORDER_ID' in df.columns else "N/A")
        kpi_col2.metric("Total Quantity", int(df['TOTAL_QUANTITY'].sum()) if 'TOTAL_QUANTITY' in df.columns else "N/A")
        kpi_col3.metric("Total Revenue", round(df['AMOUNT'].sum(),2) if 'AMOUNT' in df.columns else "N/A")

        # --- Filters ---
        st.sidebar.header("Filters")
        city_filter = st.sidebar.multiselect("Select City", options=df['CITY'].unique() if 'CITY' in df.columns else [])
        brand_filter = st.sidebar.multiselect("Select Brand", options=df['BRAND'].unique() if 'BRAND' in df.columns else [])

        filtered_df = df.copy()
        if city_filter:
            filtered_df = filtered_df[filtered_df['CITY'].isin(city_filter)]
        if brand_filter:
            filtered_df = filtered_df[filtered_df['BRAND'].isin(brand_filter)]

        # --- Charts ---
        st.subheader("Sales by City")
        if 'CITY' in filtered_df.columns and 'AMOUNT' in filtered_df.columns:
            fig_city = px.bar(
                filtered_df.groupby('CITY')['AMOUNT'].sum().reset_index(),
                x='CITY', y='AMOUNT',
                title="Revenue by City",
                text_auto=True
            )
            st.plotly_chart(fig_city, use_container_width=True)

        st.subheader("Top Brands by Sales")
        if 'BRAND' in filtered_df.columns and 'AMOUNT' in filtered_df.columns:
            top_brands = filtered_df.groupby('BRAND')['AMOUNT'].sum().sort_values(ascending=False).head(10).reset_index()
            fig_brand = px.bar(top_brands, x='BRAND', y='AMOUNT', text_auto=True)
            st.plotly_chart(fig_brand, use_container_width=True)

        st.subheader("Quantity Distribution")
        if 'TOTAL_QUANTITY' in filtered_df.columns:
            fig_qty = px.histogram(filtered_df, x='TOTAL_QUANTITY', nbins=50, title="Quantity Distribution")
            st.plotly_chart(fig_qty, use_container_width=True)

        st.subheader("Sample Data")
        st.dataframe(filtered_df.head(20))

    except Exception as e:
        st.error(f"Error loading file: {e}")
