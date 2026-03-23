# hid_executor.py
import usb_hid
import time
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# Safe initialization
try:
    kbd = Keyboard(usb_hid.devices)
    layout = KeyboardLayoutUS(kbd)
except Exception as e:
    print("HID disabled or unavailable:", e)
    kbd = None
    layout = None

# Controls
MAX_STRING_LEN = 2048  # limit typed strings
TYPING_DELAY = 0.005   # seconds between characters, adjust if needed

def execute_command(command):
    if not isinstance(command, dict):
        print("Invalid command format.")
        return False

    cmd_type = command.get("type")
    try:
        if cmd_type == "keyboard_string":
            text = command.get("text", "")
            if not isinstance(text, str):
                return False
            if len(text) > MAX_STRING_LEN:
                print("String too long, aborting.")
                return False
            _type_string(text)
            return True

        elif cmd_type == "keyboard_shortcut":
            keys = command.get("keys", [])
            if not isinstance(keys, list):
                return False
            # keys should be simple strings like "CONTROL", "ALT", "F4", "A"
            _press_shortcut(keys)
            return True

        elif cmd_type == "delay":
            ms = command.get("ms", 500) # Default to 500 milliseconds
            print(f"HID DELAY: Waiting {ms}ms...")
            time.sleep(ms / 1000.0)
            return True

        else:
            print("Unsupported command type:", cmd_type)
            return False

    except Exception as e:
        print("HID execution error:", e)
        return False

def _type_string(text):
    if layout is None:
        print("Keyboard not initialized. Skipping typing.")
        return

    print("HID TYPE STRING (len={}):".format(len(text)), text[:200])  # show only head
    for ch in text:
        try:
            layout.write(ch)
            time.sleep(TYPING_DELAY)
        except Exception as e:
            print("Typing error on character:", ch, e)
            return

def _press_shortcut(keys):
    if kbd is None:
        print("Keyboard not initialized. Skipping shortcut.")
        return

    print("HID SHORTCUT:", keys)

    keycodes = []
    for k in keys:
        if not isinstance(k, str):
            print("Invalid key type:", k)
            return
        try:
            keycodes.append(getattr(Keycode, k.upper()))
        except AttributeError:
            print("Invalid key requested:", k)
            return

    # Press and release
    try:
        kbd.press(*keycodes)
        # small hold for safety, adjust as needed
        time.sleep(0.05)
        kbd.release_all()
    except Exception as e:
        print("Key press error:", e)
        try:
            kbd.release_all()
        except Exception:
            pass