import json
from src.ai_engine.gemini_client import ask_gemini


def get_cleaning_rules(profile: dict) -> dict:
    prompt = f"""
You are a senior data quality engineer.

Dataset profile:
{profile}

Suggest SAFE data cleaning rules.

Return STRICT JSON ONLY:
{{
  "missing_value_strategy": {{
    "column_name": "mean | median | mode | drop"
  }},
  "remove_duplicates": true,
  "date_standardization": ["date_column_name"]
}}
"""
    response = ask_gemini(prompt)

    try:
        return json.loads(response)
    except Exception:
        # Safe fallback (enterprise behavior)
        return {
            "missing_value_strategy": {},
            "remove_duplicates": True,
            "date_standardization": []
        }
