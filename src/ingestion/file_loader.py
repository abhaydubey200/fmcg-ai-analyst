import pandas as pd
import streamlit as st


def load_file(file):
    filename = file.name.lower()

    # CSV is always safe
    if filename.endswith(".csv"):
        return pd.read_csv(file)

    # Excel is OPTIONAL
    elif filename.endswith(".xlsx"):
        try:
            return pd.read_excel(file, engine="openpyxl")
        except ImportError:
            st.warning(
                "⚠️ Excel support not available on server. "
                "Please upload CSV instead."
            )
            raise RuntimeError("Excel dependency missing")

    else:
        raise ValueError("Unsupported file format. Upload CSV or XLSX.")
