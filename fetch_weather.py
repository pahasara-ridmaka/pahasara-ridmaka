#usr/bin/env python3
'''
 Fetch Current Weather Data and Update README.md
'''


import os
# import json
import requests
# from datetime import datetime


# Configurations
API_KEY = os.environ.get('OPENWEATHER_API_KEY')  # Get API Key from OPEANWEATHER_API_KEY environment variable
CITY = 'Panama'
COUNTRY_CODE = 'LK'
UNITS = 'metric'  # Use 'imperial' for Fahrenheit

# Fetch Weather Data
url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY},{COUNTRY_CODE}&units={UNITS}&appid={API_KEY}"
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
    weather_string = f"{emoji} {description.capitalize()}, {temp}{temp_unit} (Feels like {feels_like}{temp_unit}) \| Humidity: {humidity}% \| Wind Speed: {wind_speed} m/s

    # Read current README.md content
    with open('README.md', 'r') as file:
        readme_content = file.read()

    # Update Weather section
    start_marker = "<!-- WEATHER_START -->"
    end_marker = "<!-- WEATHER_END -->"
    weather_section = f"{start_marker}\n{weather_string}\n{end_marker}"


    if start_marker in readme_content and end_marker in readme_content:
        # Replace existing weather section
        updated_content = readme_content.split(start_marker)[0] + weather_section + readme_content.split(end_marker)[1]

    # Write updated README.md 
    with open('README.md', 'w') as file:
        file.write(updated_content)

    print("Weather data updated successfully in README.md")
else:
    print(f"Failed to fetch weather data: {weather_data.get('message', 'Unknown error')}")
    exit(1)
    
