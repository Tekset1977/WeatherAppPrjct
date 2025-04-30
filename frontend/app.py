import streamlit as st
import requests
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Live Weather", page_icon="⛅")
st.title("🌤️ Local Weather Forecast")

#backend_url = "http://localhost:8000/weather"
backend_url = os.getenv("BACKEND_URL", "http://localhost:8000") + "/weather"

try:
    with st.spinner("Fetching weather..."):
        response = requests.get(backend_url, timeout=5)
        st.write(f"Response status code: {response.status_code}")
        st.write(f"Raw response content: {response.text}")  # debug log
        data = response.json()

    st.subheader(f"Weather in {data['city']}")
    st.image(f"http://openweathermap.org/img/wn/{data['icon']}@2x.png")
    st.metric(label="Temperature (°C)", value=data["temperature"])
    st.write(f"Condition: **{data['description'].capitalize()}**") 
    st.markdown(f"**🧠 AI Suggestion:** {data['suggestion']}")

except Exception as e:
    st.error(f"Failed to load weather data: {e}")

st.header("🕑 Hourly Forecast (Today)")

hourly_response = requests.get(os.getenv("BACKEND_URL", "http://localhost:8000") + "/hourly", timeout=5).json()

response = requests.get(os.getenv("BACKEND_URL", "http://localhost:8000") + "/hourly", timeout=5)
st.write(f"Hourly API status code: {response.status_code}")
st.write(f"Hourly API raw content: {response.text}")  # debug output
hourly_response = response.json()


if "error" in hourly_response:
    st.warning(hourly_response["error"])
else:
    timezone_label = hourly_response.get("timezone", "UTC")
    times = [forecast["time"] for forecast in hourly_response["hourly"]]
    temps = [forecast["temp"] for forecast in hourly_response["hourly"]]

    st.subheader("🌡️ Temperature Forecast (3-hour intervals)")

    fig, ax = plt.subplots()
    ax.plot(times, temps, marker='o')
    ax.set_xlabel(f"Time ({timezone_label})")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Temperature over Today")
    ax.grid(True)
    st.pyplot(fig)

################

st.header("📅 7-Day Forecast")

backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
weekly = requests.get(backend_url + "/weekly", timeout=3).json()

if "error" in weekly:
    st.warning(weekly["error"])
else:
    cols = st.columns(7)
    for i, day in enumerate(weekly["daily"]):
        with cols[i]:
            st.image(f"http://openweathermap.org/img/wn/{day['icon']}@2x.png")
            st.metric(label=f"Day {i+1}", value=f"{day['temp']} °C")
            st.caption(day["description"].capitalize())
