from src.ai_engine.gemini_client import ask_gemini

def get_cleaning_rules(profile: dict) -> str:
    """
    AI-driven cleaning with deterministic fallback.
    """

    prompt = f"""
    You are a senior data analyst.

    Dataset profile:
    {profile}

    Suggest:
    - Missing value handling
    - Data type fixes
    - Outlier handling
    - FMCG best practices
    """

    response = ask_gemini(prompt)

    if response.startswith("AI unavailable"):
        return (
            "Default Cleaning Rules Applied:\n"
            "- Drop duplicate rows\n"
            "- Fill numeric nulls with median\n"
            "- Fill categorical nulls with mode\n"
            "- Standardize column names\n"
            "- Convert date-like columns to datetime\n"
            "- Remove negative sales/quantity values"
        )

    return response
