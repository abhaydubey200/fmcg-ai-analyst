import pandas as pd

def get_cleaning_rules(profile):
    """
    Returns AI suggested cleaning rules based on data profile.
    Currently a placeholder. Can be extended with AI logic later.
    """
    rules = {
        "drop_columns": [
            "WAREHOUSE_CATEGORY", "BUSINESS_UNIT", "ASSET_SERIAL_NUMBER",
            "EX_FACT_UNIT_PRICE", "ASSET_OWNED", "HI_PO_OUTLET", "OUTLET_ERP_ID"
        ],
        "impute_columns": {
            "MOBILE_NO": "UNKNOWN",
            "EMPLOYEE_ID": "UNKNOWN",
            "CITY": "UNKNOWN",
            "STATE": "UNKNOWN"
        },
        "convert_datetime": ["ORDER_DATE", "ORDER_TIME", "OUTLET_CREATED_DATE"],
        "convert_timedelta": ["TIME_SPENT_AT_OUTLET"],
        "categorical_columns": [
            "SOURCE", "ORDERSTATE", "ORDERTYPE", "TYPE", "OUTLET_CATEGORY",
            "BEAT_NAME", "AREA", "WAREHOUSE", "ZONE", "SUBZONE", "STATE",
            "WAREHOUSE_CITY", "USER_NM", "USERNAME", "DESIGNATION_REPORT_TO",
            "DESIGNATION_MNGR_REPORTING_TO", "DESIGNATION", "REPORTING_TO",
            "MANAGER_REPORTING_TO", "CATEGORY", "SUBCATEGORIES", "BRAND",
            "SKU_CODE", "WAREHOUSE_GSTIN", "BUSS_CODE", "VERIFIED_OUTLET"
        ]
    }
    return rules

def clean_data(df, rules):
    """
    Apply cleaning rules to the dataframe.
    """
    # Drop columns
    df = df.drop(columns=rules["drop_columns"], errors="ignore")
    
    # Impute missing values
    for col, val in rules["impute_columns"].items():
        if col in df.columns:
            df[col] = df[col].fillna(val).astype(str)
    
    # Convert datetime
    for col in rules["convert_datetime"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    
    # Convert timedelta
    for col in rules.get("convert_timedelta", []):
        if col in df.columns:
            df[col] = pd.to_timedelta(df[col])
    
    # Convert categorical
    for col in rules["categorical_columns"]:
        if col in df.columns:
            df[col] = df[col].astype("category")
    
    return df
