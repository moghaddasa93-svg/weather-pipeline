from __future__ import annotations

from typing import Any

import requests

from config import DAILY_VARIABLES, LOCATIONS


BASE_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_weather() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    for location in LOCATIONS:
        params = {
            "latitude": location["lat"],
            "longitude": location["lon"],
            "daily": ",".join(DAILY_VARIABLES),
            "timezone": "auto",
            "forecast_days": 2,
        }

        response = requests.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        daily = data["daily"]

        records.append(
            {
                "location_name": location["name"],
                "location_label": location["label"],
                "forecast_date": daily["time"][1],
                "temperature_max": daily["temperature_2m_max"][1],
                "precipitation_sum": daily["precipitation_sum"][1],
                "wind_speed_max": daily["wind_speed_10m_max"][1],
            }
        )

    return records


if __name__ == "__main__":
    weather = fetch_weather()
    print(f"Fetched {len(weather)} forecast records")
    for row in weather:
        print(row)