import requests
from datetime import datetime


def get_location_by_ip():
    try:
        response = requests.get("https://ipinfo.io/json", timeout=2)
        data = response.json()
        lat, lon = map(float, data["loc"].split(","))
        city = data.get("city", "Unknown")
        timezone = data.get("timezone", "UTC")
        return lat, lon, city, timezone
    except Exception as e:
        print("⚠️ Failed IP geolocation:", e)
        return None, None, "Unknown", "UTC"





def get_weather(lat, lon, api_key):
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"lat={lat}&lon={lon}&appid={api_key}&units=metric"
        )
        response = requests.get(url, timeout=3)
        return response.json()
    except Exception as e:
        print("⚠️ Failed OpenWeather fetch:", e)
        return {"main": {"temp": "N/A"}, "weather": [{"description": "Error", "icon": "01d"}]}
 

def get_weekly_weather(lat, lon, api_key):
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/forecast?"
            f"lat={lat}&lon={lon}&appid={api_key}&units=metric"
        )
        response = requests.get(url, timeout=3)
        return response.json()
    except Exception as e:
        print("⚠️ Weekly weather fetch failed:", e)
        return None

def get_hourly_weather(lat, lon, api_key):
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/forecast?"
            f"lat={lat}&lon={lon}&appid={api_key}&units=metric"
        )
        response = requests.get(url, timeout=3)
        return response.json()
    except Exception as e:
        print("⚠️ Hourly weather fetch failed:", e)
        return None