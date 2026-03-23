# wifi_manager.py
import wifi
import config
import time

def connect():
    """Attempt to connect once, return True on success."""
    try:
        if not getattr(wifi.radio, "connected", False):
            print("Connecting to WiFi: {}...".format(config.WIFI_SSID))
            wifi.radio.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

        if getattr(wifi.radio, "connected", False):
            print("WiFi connected. IP:", wifi.radio.ipv4_address)
            return True
        else:
            print("WiFi connection failed.")
            return False
    except Exception as e:
        print("WiFi error:", e)
        return False

def is_connected():
    """Checks connection state."""
    return getattr(wifi.radio, "connected", False)

def ensure_connection(max_total_wait=60):
    """
    Ensure connectivity, with exponential backoff, return True when connected.
    max_total_wait seconds is a safety to allow caller to decide on reset path.
    """
    total_wait = 0
    backoff = 1
    while not is_connected():
        print("WiFi disconnected. Attempting to reconnect...")
        if connect():
            return True

        time.sleep(backoff)
        total_wait += backoff
        backoff = min(backoff * 2, 20)  # cap backoff
        if max_total_wait and total_wait >= max_total_wait:
            print("ensure_connection timeout after", total_wait, "s")
            return False

    return True