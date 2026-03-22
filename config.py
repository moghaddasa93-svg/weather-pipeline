from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUTS_DIR = BASE_DIR / "outputs"
DOCS_DIR = BASE_DIR / "docs"

DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)

SQL_DB_PATH = os.getenv("SQL_DB_PATH", str(DATA_DIR / "weather.db"))

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

LOCATIONS = [
    {"name": "Tehran", "label": "Birthplace / Previous residence", "lat": 35.6892, "lon": 51.3890},
    {"name": "Aalborg", "label": "Current city", "lat": 57.0488, "lon": 9.9217},
    {"name": "Copenhagen", "label": "Comparison city", "lat": 55.6761, "lon": 12.5683},
]

DAILY_VARIABLES = [
    "temperature_2m_max",
    "precipitation_sum",
    "wind_speed_10m_max",
]