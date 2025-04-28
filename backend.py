from fastapi import FastAPI
from weather_utils import get_location_by_ip, get_weather, get_weekly_weather 
from ai_utils import get_clothing_suggestion
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

@app.get("/weather")
def fetch_weather():
    print("⏳ Received /weather request") 
    lat, lon, city = get_location_by_ip()
    print(f"📍 Location fetched: {lat}, {lon}, {city}")

    if not lat or not lon:
        return {"error": "Failed to get location"}

    weather_data = get_weather(lat, lon, OPENWEATHER_API_KEY)
    print(f"🌡️ Weather data: {weather_data}")

    temp = weather_data["main"]["temp"]
    desc = weather_data["weather"][0]["description"]
    icon = weather_data["weather"][0]["icon"]

    suggestion = get_clothing_suggestion(temp, desc, GEMINI_API_KEY) 

    return {
        "city": city,
        "temperature": weather_data["main"]["temp"],
        "description": weather_data["weather"][0]["description"],
        "icon": weather_data["weather"][0]["icon"], 
        "suggestion": suggestion
    }

@app.get("/weekly")
def fetch_weekly_weather():
    lat, lon, city = get_location_by_ip()
    if not lat or not lon:
        return {"error": "Location unavailable"}

    data = get_weekly_weather(lat, lon, OPENWEATHER_API_KEY) 
    print("📦 Raw API response:", data)

    if not data or "daily" not in data:
        return {"error": "Weather data unavailable"}

    # Return next 7 days
    return {
        "city": city,
        "daily": [
            {
                "day": i,
                "temp": d["temp"]["day"],
                "description": d["weather"][0]["description"],
                "icon": d["weather"][0]["icon"]
            }
            for i, d in enumerate(data["daily"][:7])
        ]
    }