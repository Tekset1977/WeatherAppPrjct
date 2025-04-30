from fastapi import FastAPI
from weather_utils import get_location_by_ip, get_weather, get_weekly_weather, get_hourly_weather
from ai_utils import get_clothing_suggestion
from datetime import datetime, timedelta
from collections import defaultdict
from dotenv import load_dotenv
import pytz
import os

load_dotenv()

app = FastAPI()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

@app.get("/weather")
def fetch_weather():
    lat, lon, city, timezone = get_location_by_ip()  # ✅ must match new return
    if not lat or not lon:
        return {"error": "Failed to get location"}

    weather_data = get_weather(lat, lon, OPENWEATHER_API_KEY)
    if not weather_data or "main" not in weather_data:
        return {"error": "Weather data unavailable"}

    temp = weather_data["main"]["temp"]
    desc = weather_data["weather"][0]["description"]
    icon = weather_data["weather"][0]["icon"]

    suggestion = get_clothing_suggestion(temp, desc, GEMINI_API_KEY)

    return {
        "city": city,
        "temperature": temp,
        "description": desc,
        "icon": icon,
        "suggestion": suggestion
    }

@app.get("/weekly")
def fetch_weekly_weather():
    try:
        lat, lon, city, timezone = get_location_by_ip()
        print(f"📍 Location: {lat}, {lon}, {city}, {timezone}")

        data = get_weekly_weather(lat, lon, OPENWEATHER_API_KEY)
        print(f"🌦️ Raw forecast data:", data)

        if not data or "list" not in data:
            print("❌ Forecast data missing 'list'")
            return {"error": "Weather data unavailable"}

        # Group forecasts by day
        daily_data = defaultdict(list)

        for entry in data["list"]:
            dt = datetime.utcfromtimestamp(entry["dt"])
            day_key = dt.date().isoformat()
            daily_data[day_key].append(entry)

        result = []
        for i, (day, entries) in enumerate(daily_data.items()):
            avg_temp = sum(e["main"]["temp"] for e in entries) / len(entries)
            description = entries[0]["weather"][0]["description"]
            icon = entries[0]["weather"][0]["icon"]

            result.append({
                "day": day,
                "temp": round(avg_temp, 1),
                "description": description,
                "icon": icon
            })

            if i == 6:
                break

        return {
            "city": city,
            "daily": result
        }
    except Exception as e:
        print("💥 Exception inside /weekly:", e)
        return {"error": str(e)}

@app.get("/hourly")
def fetch_hourly_weather():
    lat, lon, city, timezone = get_location_by_ip()
    if not lat or not lon:
        return {"error": "Failed to get location"}

    data = get_hourly_weather(lat, lon, OPENWEATHER_API_KEY)
    if not data or "list" not in data:
        return {"error": "Weather data unavailable"}

    now_utc = datetime.utcnow()
    tz = pytz.timezone(timezone)
    now_local = now_utc.astimezone(tz)
    end_local = now_local + timedelta(hours=24)

    today_forecasts = []

    for item in data["list"]:
        forecast_utc = datetime.utcfromtimestamp(item["dt"])
        forecast_local = forecast_utc.astimezone(tz)

        if now_local <= forecast_local <= end_local:
            today_forecasts.append({
                "time": forecast_local.strftime("%H:%M"),
                "temp": item["main"]["temp"],
                "description": item["weather"][0]["description"],
                "icon": item["weather"][0]["icon"]
            })

    return {
        "city": city,
        "timezone": timezone,
        "hourly": today_forecasts
    }