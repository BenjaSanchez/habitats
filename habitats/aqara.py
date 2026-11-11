import hashlib
import json
import os
import secrets
import time
import urllib.request


AQARA_API_URL = "https://open-ger.aqara.com/v3.0/open/api"
SENSOR_MODEL = "lumi.sensor_ht.agl02"


def aqara_request(intent, data):
    """Send a signed request to the Aqara API."""
    app_id = os.environ["AQARA_APP_ID"]
    key_id = os.environ["AQARA_KEY_ID"]
    app_key = os.environ["AQARA_APP_KEY"]
    access_token = os.environ["AQARA_ACCESS_TOKEN"]

    nonce = secrets.token_hex(8)
    timestamp = str(int(time.time() * 1000))

    sign_string = (
        f"Accesstoken={access_token}&"
        f"Appid={app_id}&"
        f"Keyid={key_id}&"
        f"Nonce={nonce}&"
        f"Time={timestamp}{app_key}"
    ).lower()

    signature = hashlib.md5(sign_string.encode("utf-8")).hexdigest()

    headers = {
        "Accesstoken": access_token,
        "Appid": app_id,
        "Keyid": key_id,
        "Nonce": nonce,
        "Time": timestamp,
        "Sign": signature,
        "Lang": "en",
        "Content-Type": "application/json",
    }

    payload = json.dumps({
        "intent": intent,
        "data": data,
    }).encode("utf-8")

    request = urllib.request.Request(
        AQARA_API_URL,
        data=payload,
        headers=headers,
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.loads(response.read().decode("utf-8"))

    if result.get("code") != 0:
        raise RuntimeError(f"Aqara API error: {result}")

    return result.get("result", {})


def get_devices():
    """Retrieve devices registered in the Aqara account."""
    result = aqara_request(
        "query.device.info",
        {
            "positionId": "",
            "pageNum": 1,
            "pageSize": 100,
        },
    )

    devices = result.get("data")

    if not isinstance(devices, list):
        raise RuntimeError(
            f"Unexpected Aqara device response: {result}"
        )

    return devices


def get_sensors():
    """Return registered temperature and humidity sensors."""
    devices = get_devices()

    sensors = [
        {
            "device_id": device["did"],
            "name": device["deviceName"],
        }
        for device in devices
        if device.get("model") == SENSOR_MODEL
    ]

    if any(not sensor["name"] for sensor in sensors):
        raise RuntimeError("An Aqara sensor has no device name.")

    return sensors
