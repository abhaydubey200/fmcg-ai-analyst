import pandas as pd
import numpy as np

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    # Convert dates
    if 'ORDER_DATE' in df.columns:
        df['ORDER_DATE'] = pd.to_datetime(df['ORDER_DATE'], errors='coerce')
    if 'OUTLET_CREATED_DATE' in df.columns:
        df['OUTLET_CREATED_DATE'] = pd.to_datetime(df['OUTLET_CREATED_DATE'], errors='coerce')

    # Time spent conversion
    if 'TIME_SPENT_AT_OUTLET' in df.columns:
        df['TIME_SPENT_SEC'] = pd.to_timedelta(df['TIME_SPENT_AT_OUTLET'], errors='coerce').dt.total_seconds()

    # Phone numbers as strings
    for col in ['PHONE_NO', 'MOBILE_NO']:
        if col in df.columns:
            df[col] = df[col].astype(str).replace('nan', 'UNKNOWN')

    return df

def kpi_summary(df: pd.DataFrame):
    """Return dict of basic KPIs."""
    summary = {}
    if 'AMOUNT' in df.columns:
        summary['Total Sales'] = df['AMOUNT'].sum()
        summary['Average Order Value'] = df['AMOUNT'].mean()
    if 'TOTAL_QUANTITY' in df.columns:
        summary['Total Quantity'] = df['TOTAL_QUANTITY'].sum()
    if 'ORDER_ID' in df.columns:
        summary['Total Orders'] = df['ORDER_ID'].nunique()
    return summary
