import json
from src.ai_engine.gemini_client import ask_gemini

def get_cleaning_rules(profile):
    prompt = f"""
You are a senior data quality engineer.
Suggest data cleaning rules.

Profile:
{profile}

Return JSON:
{{
 "missing_value_strategy": {{"column":"mean|median|mode|drop"}},
 "remove_duplicates": true,
 "date_standardization": ["date"]
}}
"""
    return json.loads(ask_gemini(prompt))
