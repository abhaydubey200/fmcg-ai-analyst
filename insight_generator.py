from src.ai_engine.gemini_client import ask_gemini

def generate_insights(kpis):
    prompt = f"""
Generate executive FMCG insights from KPIs:
{kpis}
"""
    return ask_gemini(prompt)
