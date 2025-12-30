import json
from src.ai_engine.gemini_client import ask_gemini


def detect_charts_ai(df, kpis):
    prompt = f"""
You are an FMCG data visualization expert.

Columns: {list(df.columns)}
KPIs: {kpis}

Select best charts.

Return STRICT JSON:
[
  {{
    "chart_type": "bar | line",
    "x_axis": "column_name",
    "y_axis": "column_name",
    "title": "Chart Title",
    "business_reason": "Why this chart is useful"
  }}
]
"""
    response = ask_gemini(prompt)

    try:
        return json.loads(response)
    except Exception:
        return []
