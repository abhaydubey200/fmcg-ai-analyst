import json
from src.ai_engine.gemini_client import ask_gemini


def detect_kpis_ai(df):
    prompt = f"""
You are an FMCG analytics expert.

Dataset columns:
{list(df.columns)}

Detect important KPIs.

Return JSON:
[
  {{"name": "Total Sales", "formula": "sum(sales)"}},
  {{"name": "Average Sales", "formula": "mean(sales)"}}
]
"""
    response = ask_gemini(prompt)
    try:
        return json.loads(response)
    except Exception:
        return []


def execute_kpis(df, kpis):
    results = {}

    for kpi in kpis:
        formula = kpi.get("formula", "")
        name = kpi.get("name", "Unknown KPI")

        if "(" not in formula:
            continue

        col = formula.split("(")[1].replace(")", "")
        if col not in df.columns:
            continue

        if "sum" in formula:
            results[name] = df[col].sum()
        elif "mean" in formula:
            results[name] = df[col].mean()

    return results
