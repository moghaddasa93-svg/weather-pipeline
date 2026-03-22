from __future__ import annotations

import os
import requests

from config import GROQ_MODEL


def generate_poem(records: list[dict]) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "Missing GROQ_API_KEY. Add it locally in .env or in GitHub Secrets."
        )

    weather_lines = []
    for r in records:
        weather_lines.append(
            f"{r['location_name']} ({r['location_label']}): "
            f"date={r['forecast_date']}, "
            f"max temp={r['temperature_max']}°C, "
            f"precipitation={r['precipitation_sum']} mm, "
            f"wind={r['wind_speed_max']} km/h"
        )

    weather_summary = "\n".join(weather_lines)

    prompt = f"""
Write a short creative poem in two languages: English and Persian.

Use tomorrow's weather for these three locations:
{weather_summary}

Requirements:
- Compare the weather in the three places
- Mention the differences in temperature, rain, or wind
- Say where it would be nicest to be tomorrow
- Keep it short, elegant, and clear
- First write the English version
- Then write the Persian version
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.8,
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=60,
    )
    response.raise_for_status()

    data = response.json()
    return data["choices"][0]["message"]["content"]


if __name__ == "__main__":
    sample = [
        {
            "location_name": "Tehran",
            "location_label": "Birthplace / Previous residence",
            "forecast_date": "2026-03-23",
            "temperature_max": 18,
            "precipitation_sum": 0,
            "wind_speed_max": 10,
        },
        {
            "location_name": "Aalborg",
            "location_label": "Current city",
            "forecast_date": "2026-03-23",
            "temperature_max": 7,
            "precipitation_sum": 2.1,
            "wind_speed_max": 24,
        },
        {
            "location_name": "Copenhagen",
            "location_label": "Comparison city",
            "forecast_date": "2026-03-23",
            "temperature_max": 9,
            "precipitation_sum": 1.2,
            "wind_speed_max": 18,
        },
    ]

    print(generate_poem(sample))