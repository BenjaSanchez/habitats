import json
import os
import urllib.request


def d1_request(sql, params=None):
    """Execute a SQL statement against the Cloudflare D1 database."""
    account_id = os.environ["CLOUDFLARE_ACCOUNT_ID"]
    database_id = os.environ["CLOUDFLARE_DATABASE_ID"]
    api_token = os.environ["CLOUDFLARE_API_TOKEN"]

    url = (
        "https://api.cloudflare.com/client/v4/accounts/"
        f"{account_id}/d1/database/{database_id}/query"
    )

    payload = json.dumps({
        "sql": sql,
        "params": params or [],
    }).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.loads(response.read().decode("utf-8"))

    if not result.get("success"):
        raise RuntimeError(f"D1 API error: {result}")

    return result


def update_sensors(sensors):
    """Insert new sensors and update names of existing sensors."""
    if not sensors:
        raise RuntimeError("No Aqara temperature/humidity sensors found.")

    placeholders = ", ".join(["(?, ?, 1)"] * len(sensors))

    sql = f"""
        INSERT INTO sensors (device_id, name, active)
        VALUES {placeholders}
        ON CONFLICT(device_id) DO UPDATE SET
            name = excluded.name,
            active = 1
    """

    params = [
        value
        for sensor in sensors
        for value in (sensor["device_id"], sensor["name"])
    ]

    return d1_request(sql, params)


def get_active_sensors():
    """Retrieve active sensor IDs from D1."""
    response = d1_request(
        "SELECT device_id FROM sensors WHERE active = 1"
    )

    return [
        row["device_id"]
        for row in response["result"][0]["results"]
    ]


def insert_readings(readings):
    """Insert collected sensor readings into D1."""
    if not readings:
        raise RuntimeError("No readings to insert.")

    import time

    collected_at = int(time.time())

    placeholders = ", ".join(["(?, ?, ?, ?, ?, ?)"] * len(readings))

    sql = f"""
        INSERT OR IGNORE INTO readings (
            device_id,
            collected_at,
            temperature,
            temperature_timestamp,
            humidity,
            humidity_timestamp
        )
        VALUES {placeholders}
    """

    params = [
        value
        for reading in readings
        for value in (
            reading["device_id"],
            collected_at,
            reading["temperature"],
            reading["temperature_timestamp"],
            reading["humidity"],
            reading["humidity_timestamp"],
        )
    ]

    return d1_request(sql, params)
