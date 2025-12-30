import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_processing import preprocess_data, kpi_summary
from gemini_client import ask_gemini

st.set_page_config(page_title="📊 FMCG AI Analyst", layout="wide")
st.title("📊 FMCG AI Analyst Dashboard")

# --- File Upload ---
uploaded_file = st.file_uploader("Upload CSV or Excel (Max 200MB)", type=["csv", "xlsx", "xls"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, engine='openpyxl')

    df = preprocess_data(df)
    st.success(f"File loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")

    # --- KPI Cards ---
    summary = kpi_summary(df)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Sales", f"{summary.get('Total Sales',0):,.2f}")
    col2.metric("📊 Avg Order Value", f"{summary.get('Average Order Value',0):,.2f}")
    col3.metric("🛒 Total Orders", f"{summary.get('Total Orders',0)}")
    col4.metric("📦 Total Quantity", f"{summary.get('Total Quantity',0)}")

    # --- Tabs ---
    tabs = st.tabs(["Overview", "Outlet & Employee", "Inventory", "AI Insights"])

    # --- Tab 1: Overview ---
    with tabs[0]:
        st.subheader("Monthly Sales Trend")
        df_monthly = df.groupby(df['ORDER_DATE'].dt.to_period("M"))['AMOUNT'].sum().reset_index()
        df_monthly['ORDER_DATE'] = df_monthly['ORDER_DATE'].dt.to_timestamp()
        fig = px.line(df_monthly, x='ORDER_DATE', y='AMOUNT', title="Monthly Sales")
        st.plotly_chart(fig, use_container_width=True)

    # --- Tab 2: Outlet & Employee ---
    with tabs[1]:
        st.subheader("Top Outlets")
        top_outlets = df.groupby('OUTLET_NAME')['AMOUNT'].sum().nlargest(20).reset_index()
        fig = px.bar(top_outlets, x='OUTLET_NAME', y='AMOUNT', title="Top 20 Outlets by Sales")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Top Employees")
        top_employees = df.groupby('USER_NM')['AMOUNT'].sum().nlargest(20).reset_index()
        fig = px.bar(top_employees, x='USER_NM', y='AMOUNT', title="Top 20 Employees by Sales")
        st.plotly_chart(fig, use_container_width=True)

    # --- Tab 3: Inventory ---
    with tabs[2]:
        st.subheader("Top SKUs")
        top_skus = df.groupby('SKU_ID')['TOTAL_QUANTITY'].sum().nlargest(20).reset_index()
        fig = px.bar(top_skus, x='SKU_ID', y='TOTAL_QUANTITY', title="Top 20 SKUs by Quantity Sold")
        st.plotly_chart(fig, use_container_width=True)

    # --- Tab 4: AI Insights ---
    with tabs[3]:
        st.subheader("AI Suggestions")
        profile = {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "dtypes": df.dtypes.astype(str).to_dict(),
            "missing_percent": (df.isna().sum() / df.shape[0] * 100).round(2).to_dict()
        }
        prompt = f"Analyze this FMCG dataset: {profile}.\nProvide cleaning rules, KPIs, trends, and future recommendations."
        insights = ask_gemini(prompt)
        st.text_area("AI Insights & Recommendations", insights, height=400)
