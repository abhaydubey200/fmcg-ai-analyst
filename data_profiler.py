def profile_data(df):
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_percent": (df.isnull().mean() * 100).to_dict(),
        "sample": df.head(5).to_dict(orient="records")
    }
