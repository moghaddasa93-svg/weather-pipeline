from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from fetch import fetch_weather
from store_sql import init_db, store_weather, get_latest_forecasts
from generate_poem import generate_poem
from build_site import build_site
from config import OUTPUTS_DIR


def main() -> None:
    print("Starting weather pipeline...")

    # 1) Fetch weather
    records = fetch_weather()
    fetched_count = len(records)
    print(f"Fetched {fetched_count} forecast record(s)")

    if not records:
        print("No weather data fetched. Exiting.")
        return

    # 2) Store in SQLite
    conn = init_db()
    inserted = store_weather(conn, records)
    latest_records = get_latest_forecasts(conn)
    conn.close()

    print(f"Inserted {inserted} new row(s) into SQLite")

    # 3) Generate poem
    poem = generate_poem(latest_records)
    print("Poem generated successfully")

    # 4) Build GitHub Pages site
    build_site(latest_records, poem)
    print("docs/index.html updated")

    # 5) Save run summary
    summary = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "records_fetched": fetched_count,
        "rows_inserted_sql": inserted,
        "page_updated": True,
    }

    summary_path = Path(OUTPUTS_DIR) / "run_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)

    print("Run summary written to:", summary_path)
    print("Pipeline complete.")


if __name__ == "__main__":
    main()