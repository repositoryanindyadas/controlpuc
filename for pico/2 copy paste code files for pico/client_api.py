# client_api.py
import adafruit_requests
import adafruit_connection_manager
import wifi
import config
import gc
import time

requests_session = None
dynamic_server_url = None
is_registered = False 

def get_session(force_rebuild=False):
    global requests_session
    if force_rebuild:
        requests_session = None
        gc.collect()
    if requests_session is None:
        try:
            pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
            ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
            requests_session = adafruit_requests.Session(pool, ssl_context)
        except Exception:
            return None
    return requests_session

def discover_server():
    global dynamic_server_url
    if dynamic_server_url: return dynamic_server_url
    pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
    try:
        sock = pool.socket(pool.AF_INET, pool.SOCK_DGRAM)
        sock.settimeout(2.0)
        sock.sendto(b"DISCOVER_C2", ("255.255.255.255", 50000))
        buf = bytearray(32)
        size, addr = sock.recvfrom_into(buf)
        if b"C2_HERE" in buf:
            dynamic_server_url = f"http://{addr[0]}:8080"
            return dynamic_server_url
    except: pass
    finally:
        try: sock.close()
        except: pass
    return None

def _request_with_retries(method, endpoint, **kwargs):
    global dynamic_server_url, is_registered
    last_error = None
    
    for attempt in range(3):
        base_url = discover_server()
        if not base_url: continue
        
        session = get_session()
        try:
            url = base_url + endpoint
            if method == "post": return session.post(url, timeout=8, **kwargs)
            if method == "get": return session.get(url, timeout=8, **kwargs)
        except OSError as e:
            last_error = e
            # Only wipe URL/Registration if we've failed EVERY attempt
            if attempt == 2:
                dynamic_server_url = None
                is_registered = False 
            get_session(force_rebuild=True)
            time.sleep(1)
    return None

def register_device():
    global is_registered
    payload = {"device_id": config.DEVICE_ID, "api_key": config.API_KEY}
    resp = _request_with_retries("post", "/register", json=payload)
    if resp and resp.status_code in (200, 201):
        is_registered = True
        return True
    return False

def poll_commands():
    global is_registered
    endpoint = f"/poll?device_id={config.DEVICE_ID}&api_key={config.API_KEY}"
    resp = _request_with_retries("get", endpoint)
    
    if resp:
        if resp.status_code == 401: # Server explicitly forgot us
            is_registered = False
            return None
        if resp.status_code == 200:
            return resp.json()
    return None

def send_log(message):
    payload = {"device_id": config.DEVICE_ID, "api_key": config.API_KEY, "log": str(message)}
    _request_with_retries("post", "/log", json=payload)