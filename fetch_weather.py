#usr/bin/env python3
'''
 Fetch Current Weather Data and Update README.md
'''

import os
import requests
from datetime import datetime, timezone, timedelta

# Configurations
API_KEY = os.environ.get('OPENWEATHER_API_KEY')  
LAT = 6.76
LON = 81.80
UNITS = 'metric'

# Get Current Date according to time zone for Colombo, Sri Lanka (UTC+5:30)
colombo_tz = timezone(timedelta(hours=5, minutes=30))
current_time = datetime.now(colombo_tz)
year = current_time.year
month = current_time.month
date = current_time.day
hour = current_time.hour
minute = current_time.minute
second = current_time.second


# Fetch Weather Data
url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&units={UNITS}&appid={API_KEY}"
response = requests.get(url)
weather_data = response.json()

if response.status_code == 200:
    # Extract Weather Information
    temp = weather_data ['main']['temp']
    feels_like = weather_data['main']['feels_like']
    description = weather_data['weather'][0]['description']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    pressure = weather_data['main']['pressure']
    icon_code = weather_data['weather'][0]['icon']

    # Get emoji based on weather condition
    weather_emoji = {
        "01d": "☀️", "01n": "🌙",
        "02d": "⛅", "02n": "☁️",
        "03d": "☁️", "03n": "☁️",
        "04d": "☁️", "04n": "☁️",
        "09d": "🌧️", "09n": "🌧️",
        "10d": "🌦️", "10n": "🌧️",
        "11d": "⛈️", "11n": "⛈️",
        "13d": "🌨️", "13n": "🌨️",
        "50d": "🌫️", "50n": "🌫️"
    }

    emoji = weather_emoji.get(icon_code, "🌈")
    temp_unit = "°C" if UNITS == 'metric' else "°F"

    # Create Weather String
    weather_string = f"{emoji} {description.capitalize()}, {temp}{temp_unit} (Feels like {feels_like}{temp_unit}) | Humidity: {humidity}% | Wind Speed: {wind_speed} m/s"
    last_updated_string = f'<img src="https://img.shields.io/badge/Last%20Updated-{year}--{month:02d}--{date:02d} {hour:02d}:{minute:02d}:{second:02d}-000000?style=flat-square" alt="Last Updated" />'

    # Read current README.md content
    with open('README.md', 'r') as file:
        readme_content = file.read()

    # Update Weather section
    weather_start_marker = "<!-- WEATHER_START -->"
    weather_end_marker = "<!-- WEATHER_END -->"
    date_start_marker = "<!-- DATE_START -->"
    date_end_marker = "<!-- DATE_END -->"
    weather_section = f"{weather_start_marker}{weather_string}{weather_end_marker}"
    date_section = f"{date_start_marker}{last_updated_string}{date_end_marker}"


    if weather_start_marker in readme_content and weather_end_marker in readme_content:
        # Replace existing weather section
        weather_updated_content = readme_content.split(weather_start_marker)[0] + weather_section + readme_content.split(weather_end_marker)[1]

    # Update Date section
    if date_start_marker in readme_content and date_end_marker in readme_content:
        date_updated_content = weather_updated_content.split(date_start_marker)[0] + date_section + weather_updated_content.split(date_end_marker)[1]

    # Write updated README.md 
    with open('README.md', 'w') as file:
        file.write(date_updated_content)

    print("Last updated date and Weather data updated successfully in README.md")
else:
    print(f"Failed to fetch weather data: {weather_data.get('message', 'Unknown error')}")
    exit(1)
    
