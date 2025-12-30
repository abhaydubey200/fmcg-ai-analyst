import pandas as pd


def load_file(file):
    try:
        if file.name.endswith(".csv"):
            return pd.read_csv(file)

        elif file.name.endswith(".xlsx"):
            return pd.read_excel(file, engine="openpyxl")

        else:
            raise ValueError("Unsupported file format. Upload CSV or XLSX.")

    except Exception as e:
        raise RuntimeError(f"File loading failed: {e}")
