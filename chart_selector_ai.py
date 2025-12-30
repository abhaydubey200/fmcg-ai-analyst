import json
from src.ai_engine.gemini_client import ask_gemini

def detect_charts_ai(df, kpis):
    prompt = f"""
Select best charts for FMCG dashboard.

Columns: {list(df.columns)}
KPIs: {kpis}

Return JSON:
[
 {{
  "chart_type":"bar",
  "x_axis":"product",
  "y_axis":"sales",
  "title":"Sales by Product",
  "business_reason":"Product performance"
 }}
]
"""
    return json.loads(ask_gemini(prompt))
