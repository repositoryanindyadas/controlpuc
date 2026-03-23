# boot.py
import digitalio
import board
import time
import storage
import usb_hid

SAFETY_PIN = board.GP15

def check_safe_mode():
    pin = digitalio.DigitalInOut(SAFETY_PIN)
    pin.direction = digitalio.Direction.INPUT
    pin.pull = digitalio.Pull.UP
    time.sleep(0.05)
    if not pin.value:
        print("Safe mode activated. Halting boot sequence.")
        try:
            # hide the CIRCUITPY drive to avoid easy access to files
            storage.disable_usb_drive()
        except Exception as e:
            print("storage.disable_usb_drive failed:", e)
        # Optionally disable HID devices if supported
        try:
            usb_hid.disable()
        except Exception:
            pass
        # Block forever to prevent running code.py
        while True:
            time.sleep(1)

check_safe_mode()
print("Normal boot proceeding.")