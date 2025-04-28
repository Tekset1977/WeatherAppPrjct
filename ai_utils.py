import google.generativeai as genai

def get_clothing_suggestion(temp_c, description, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-2.0-flash")

    prompt = f"""
    It's {temp_c}°C outside with {description}. 
    Give a concise, 1-sentence clothing recommendation.
    Consider comfort, layers, and accessories if relevant.
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("❌ Gemini AI error:", e)
        return "No suggestion available" 