import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def _get_valid_model():
    """
    Dynamically find a Gemini model that supports generateContent
    """
    try:
        models = genai.list_models()
        for m in models:
            if "generateContent" in m.supported_generation_methods:
                return m.name
    except Exception:
        pass
    return None


def ask_gemini(prompt: str) -> str:
    """
    Safe Gemini call.
    ZERO crash guarantee.
    """

    try:
        model_name = _get_valid_model()

        if not model_name:
            return "AI unavailable: No supported Gemini model found."

        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)

        if not response or not hasattr(response, "text"):
            return "AI returned empty response."

        return response.text.strip()

    except Exception as e:
        return f"AI unavailable: {str(e)}"
