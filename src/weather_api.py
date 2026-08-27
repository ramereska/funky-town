from datetime import datetime, timezone
import os
import requests

def get_current_weather(latitude, longitude):
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        raise ValueError("OPENWEATHER_API_KEY environment variable is not set")

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
            tz=timezone.utc
        ).isoformat(),
        "ingestion_timestamp": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    raw_weather = get_current_weather(
        latitude=48.1486,
        longitude=17.1077,
    )

    weather = transform_weather(raw_weather)

    print(weather)