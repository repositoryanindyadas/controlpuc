# config.py
# Loads values from secrets.py and exposes them as constants.

from secrets import secrets

WIFI_SSID = secrets["wifi_ssid"]
WIFI_PASSWORD = secrets["wifi_password"]

DEVICE_ID = secrets["device_id"]
API_KEY = secrets["api_key"]

SERVER_ADDRESS = secrets["server_address"]

POLL_INTERVAL = secrets.get("poll_interval", 5)