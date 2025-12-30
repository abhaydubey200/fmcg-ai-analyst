from src.ai_engine.gemini_client import ask_gemini

def get_cleaning_rules(profile: dict) -> str:
    """
    Generate AI-based cleaning rules safely.
    """

    prompt = f"""
    You are a data quality expert.

    Based on this dataset profile, suggest cleaning rules:
    {profile}

    Keep it concise and practical.
    """

    rules = ask_gemini(prompt)

    if "AI unavailable" in rules:
        return (
            "Standard cleaning applied:\n"
            "- Remove null values\n"
            "- Fix data types\n"
            "- Remove duplicates\n"
            "- Standardize column names"
        )

    return rules
