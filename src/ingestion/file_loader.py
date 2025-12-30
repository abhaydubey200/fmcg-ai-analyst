import pandas as pd

def load_file(uploaded_file):
    """
    Load CSV or Excel safely.
    Handles missing openpyxl gracefully.
    """

    file_name = uploaded_file.name.lower()

    try:
        if file_name.endswith(".csv"):
            return pd.read_csv(uploaded_file)

        elif file_name.endswith((".xlsx", ".xls")):
            try:
                return pd.read_excel(uploaded_file, engine="openpyxl")
            except ImportError:
                raise ImportError(
                    "Excel file detected but 'openpyxl' is not installed. "
                    "Add openpyxl to requirements.txt or upload CSV."
                )

        else:
            raise ValueError("Unsupported file format. Upload CSV or Excel.")

    except Exception as e:
        raise RuntimeError(f"File loading failed: {str(e)}")
