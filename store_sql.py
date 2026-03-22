from __future__ import annotations

import sqlite3
from pathlib import Path

from config import SQL_DB_PATH


def init_db() -> sqlite3.Connection:
    db_path = Path(SQL_DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS weather_forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_name TEXT NOT NULL,
            location_label TEXT,
            forecast_date TEXT NOT NULL,
            temperature_max REAL,
            precipitation_sum REAL,
            wind_speed_max REAL,
            UNIQUE(location_name, forecast_date)
        )
        """
    )

    conn.commit()
    return conn


def store_weather(conn: sqlite3.Connection, records: list[dict]) -> int:
    cursor = conn.cursor()
    inserted = 0

    sql = """
        INSERT OR IGNORE INTO weather_forecasts (
            location_name,
            location_label,
            forecast_date,
            temperature_max,
            precipitation_sum,
            wind_speed_max
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """

    for record in records:
        cursor.execute(
            sql,
            (
                record["location_name"],
                record["location_label"],
                record["forecast_date"],
                record["temperature_max"],
                record["precipitation_sum"],
                record["wind_speed_max"],
            ),
        )
        inserted += cursor.rowcount

    conn.commit()
    return inserted


def get_latest_forecasts(conn: sqlite3.Connection) -> list[dict]:
    cursor = conn.cursor()
    rows = cursor.execute(
        """
        SELECT location_name, location_label, forecast_date,
               temperature_max, precipitation_sum, wind_speed_max
        FROM weather_forecasts
        ORDER BY forecast_date DESC, location_name ASC
        LIMIT 3
        """
    ).fetchall()

    records = []
    for row in rows:
        records.append(
            {
                "location_name": row[0],
                "location_label": row[1],
                "forecast_date": row[2],
                "temperature_max": row[3],
                "precipitation_sum": row[4],
                "wind_speed_max": row[5],
            }
        )
    return records