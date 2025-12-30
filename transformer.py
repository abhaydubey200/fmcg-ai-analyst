import pandas as pd

def apply_cleaning_rules(df, rules):
    if rules.get("remove_duplicates"):
        df = df.drop_duplicates()

    for col, strat in rules.get("missing_value_strategy", {}).items():
        if col in df.columns:
            if strat == "mean":
                df[col].fillna(df[col].mean(), inplace=True)
            elif strat == "median":
                df[col].fillna(df[col].median(), inplace=True)
            elif strat == "mode":
                df[col].fillna(df[col].mode()[0], inplace=True)
            elif strat == "drop":
                df.dropna(subset=[col], inplace=True)

    for col in rules.get("date_standardization", []):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df
