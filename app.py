import streamlit as st
import requests

st.set_page_config(page_title="Live Weather", page_icon="⛅")
st.title("🌤️ Local Weather Forecast")

backend_url = "http://localhost:8000/weather"

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

st.header("📅 7-Day Forecast")

weekly = requests.get("http://localhost:8000/weekly", timeout=3).json()

if "error" in weekly:
    st.warning(weekly["error"])
else:
    cols = st.columns(7)
    for i, day in enumerate(weekly["daily"]):
        with cols[i]:
            st.image(f"http://openweathermap.org/img/wn/{day['icon']}@2x.png")
            st.metric(label=f"Day {i+1}", value=f"{day['temp']} °C")
            st.caption(day["description"].capitalize())