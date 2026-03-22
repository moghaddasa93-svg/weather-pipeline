from __future__ import annotations

from pathlib import Path

from config import DOCS_DIR


def build_site(records: list[dict], poem: str) -> None:
    rows_html = ""

    for r in records:
        rows_html += f"""
        <tr>
            <td>{r['location_name']}</td>
            <td>{r['location_label']}</td>
            <td>{r['forecast_date']}</td>
            <td>{r['temperature_max']} °C</td>
            <td>{r['precipitation_sum']} mm</td>
            <td>{r['wind_speed_max']} km/h</td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Automated Weather Pipeline</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            line-height: 1.6;
            background: #fafafa;
        }}
        h1, h2 {{
            color: #222;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: white;
        }}
        th, td {{
            border: 1px solid #ccc;
            padding: 10px;
            text-align: left;
        }}
        th {{
            background: #f0f0f0;
        }}
        pre {{
            background: white;
            border: 1px solid #ddd;
            padding: 16px;
            white-space: pre-wrap;
            font-family: inherit;
        }}
        .note {{
            color: #555;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <h1>Automated Weather Pipeline</h1>
    <p class="note">This page is updated automatically by GitHub Actions.</p>

    <h2>Weather Poem</h2>
    <pre>{poem}</pre>

    <h2>Tomorrow's Forecast</h2>
    <table>
        <thead>
            <tr>
                <th>Location</th>
                <th>Role</th>
                <th>Date</th>
                <th>Max Temperature</th>
                <th>Precipitation</th>
                <th>Wind Speed</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
</body>
</html>
"""

    output_path = Path(DOCS_DIR) / "index.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)