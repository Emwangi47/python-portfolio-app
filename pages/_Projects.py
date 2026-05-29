# pyrefly: ignore [missing-import]
from importlib import readers
# pyrefly: ignore [missing-import]
import streamlit as st
import requests
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Projects", layout="wide", page_icon="💻")

# 1. HIDE STREAMLIT BRANDING (CSS Injection)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)  

st.title("My Projects")
st.write("This is a collection of projects I have worked on.")

st.divider() # Adds horizontal line to the page 

# ---- WEATHER APP SECTION ----

st.subheader("Live Weather App")
st.write("A python application built utilizing external API to display the current weather conditions of a requested city.  ")

# Expander to create a collapsible section to hide extra details
with st.expander("Launch Weather App", expanded=True): 

    # Set up the API variables
    API_KEY = st.secrets["WEATHER_API_KEY"] # OpenWeatherMap API Key    
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

    # Create user interface for the app
    city = st.text_input("Enter city name to check the weather:")

    if st.button("Get Weather"):
        if city:
            # Make the request to the API
            request_url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=imperial"
            response = requests.get(request_url)

            if response.status_code == 200:
                data = response.json()
            weather_desc = data["weather"][0]["description"].capitalize()
            temp = round(data["main"]["temp"])
            feels_like = round(data["main"]["feels_like"])
            humidity = data["main"]["humidity"]

            # Streamlit columns to display the weather data
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Temperature", value=f"{temp} °F")
            with col2:
                st.metric(label="Feels Like", value=f"{feels_like} °F")
            with col3:
                st.metric(label="Humidity", value=f"{humidity}%")
            
        else:
            st.error("City not found. Please check the spelling and try again")
    else:
        st.warning("Please enter a city name first")

st.divider()

# --- MARKET TRACKER CARD ---
st.subheader("📈 Market Tracker & Alert Automation")
st.write("A dual-component architecture featuring a live dashboard and a headless background daemon that sends automated HTML email alerts.")

with st.expander("Launch Market Tracker Dashboard", expanded=True):
    st.info("📊 **Live Dashboard Component:** Track your portfolio against the 7-day and 30-day Moving Average.")

    # We use regular columns here instead of the sidebar to keep the UI contained
    input_col1, input_col2 = st.columns([3, 1])
    
    with input_col1:
        ticker_input = st.text_input("Enter Stock Tickers (comma separated):", "AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA, META") 
    
    with input_col2:
        time_period = st.selectbox("Select Time Period:", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=2)

    # Clean up user input into a neat Python list 
    tickers = [ticker.strip().upper() for ticker in ticker_input.split(",") if ticker.strip()]

    if tickers:
        # Main Dashboard Loop
        for ticker in tickers:
            st.write(f"### 📊 {ticker}")

            # Fetch data
            stock = yf.Ticker(ticker)
            history = stock.history(period=time_period)

            if history.empty:
                st.warning(f"Could not fetch data for {ticker}. Please check the ticker symbol and try again.")
                continue

            # Calculate the moving averages
            history['7MA'] = history['Close'].rolling(window=7).mean()
            history['30MA'] = history['Close'].rolling(window=30).mean()

            # Get the latest data
            latest_price = history.iloc[-1]['Close']
            latest_ma = history.iloc[-1]['7MA']

            # Create columns for clean layout
            col1, col2, col3 = st.columns(3)

            # Display massive numbers (Metrics)
            col1.metric("Current Price", f"${latest_price:.2f}")
            col2.metric("7-Day MA", f"${latest_ma:.2f}")

            # Logic for Alert Status (Red or Green Boxes)
            if latest_price < latest_ma:
                col3.error("🚨 STATUS: BELOW AVERAGE")
            else:
                col3.success("✅ STATUS: ABOVE AVERAGE")

            # Plotting the Chart
            chart_data = history[['Close', '7MA', '30MA']]
            st.line_chart(chart_data)

            st.divider()

st.divider()

# Explain the backend script you built earlier!
st.subheader("⚙️ Backend Alert Daemon")
st.write("""
In addition to the UI dashboard above, I engineered a continuous background process (`daemon.py`) that monitors these assets automatically.
* **Continuous Polling:** Utilizes a `while True` loop with controlled sleep intervals to fetch API data.
* **State Management:** Implements memory dictionaries to ensure users only receive one alert per day, preventing spam.
* **Automated SMTP Routing:** Dynamically generates formatted HTML tables and routes them via Google's SMTP servers.
* **Persistent Logging:** Writes trigger events locally to a CSV file for historical auditing.
""")
    
          