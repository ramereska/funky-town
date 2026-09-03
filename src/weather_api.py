from datetime import datetime, timezone
import os

import requests


def get_coordinates(city, api_key, country_code=None):
    url = "https://api.openweathermap.org/geo/1.0/direct"

    query = city

    if country_code:
        query = f"{city},{country_code}"

    params = {
        "q": query,
        "limit": 1,
        "appid": api_key,
    }

    response = requests.get(
        url,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    locations = response.json()

    if not locations:
        raise ValueError(f"City not found: {city}")

    return {
        "city": locations[0]["name"],
        "latitude": locations[0]["lat"],
        "longitude": locations[0]["lon"],
        "country": locations[0]["country"],
    }


def get_current_weather(latitude, longitude, api_key=None):
    api_key = api_key or os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        raise ValueError("OPENWEATHER_API_KEY is not set")

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": api_key,
        "units": "metric",
    }

    response = requests.get(
        url,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


def transform_weather(raw_weather):
    return {
        "city": raw_weather["name"],
        "latitude": raw_weather["coord"]["lat"],
        "longitude": raw_weather["coord"]["lon"],
        "temperature_c": raw_weather["main"]["temp"],
        "humidity_pct": raw_weather["main"]["humidity"],
        "pressure_hpa": raw_weather["main"]["pressure"],
        "wind_speed_mps": raw_weather["wind"]["speed"],
        "weather_condition": raw_weather["weather"][0]["main"],
        "observation_timestamp": datetime.fromtimestamp(
            raw_weather["dt"],
            tz=timezone.utc,
        ).isoformat(),
        "ingestion_timestamp": datetime.now(timezone.utc).isoformat(),
    }