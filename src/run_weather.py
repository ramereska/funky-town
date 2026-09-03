import argparse
import os

from src.weather_api import (
    get_coordinates,
    get_current_weather,
    transform_weather,
)


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--city",
        required=True,
        help="City to retrieve weather for",
    )

    parser.add_argument(
        "--country-code",
        required=False,
        help="ISO country code, for example SK or AT",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        raise ValueError("OPENWEATHER_API_KEY is not set")

    location = get_coordinates(
        city=args.city,
        country_code=args.country_code,
        api_key=api_key,
    )

    raw_weather = get_current_weather(
        latitude=location["latitude"],
        longitude=location["longitude"],
        api_key=api_key,
    )

    weather = transform_weather(raw_weather)

    print(weather)


if __name__ == "__main__":
    main()
