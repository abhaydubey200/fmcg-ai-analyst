import json
from src.ai_engine.gemini_client import ask_gemini

def detect_kpis_ai(df):
    prompt = f"""
Detect FMCG KPIs from dataset columns:
{list(df.columns)}

Return JSON:
[
 {"name":"Total Sales","formula":"sum(sales)"},
 {"name":"Avg Order Value","formula":"mean(sales)"}
]
"""
    return json.loads(ask_gemini(prompt))

def execute_kpis(df, kpis):
    results = {}
    for kpi in kpis:
        if "sum" in kpi["formula"]:
            col = kpi["formula"].split("(")[1].replace(")", "")
            results[kpi["name"]] = df[col].sum()
        elif "mean" in kpi["formula"]:
            col = kpi["formula"].split("(")[1].replace(")", "")
            results[kpi["name"]] = df[col].mean()
    return results
