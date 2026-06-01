# pyrefly: ignore [missing-import]
from importlib import readers
# pyrefly: ignore [missing-import]
import streamlit as st
import requests


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




    
          
