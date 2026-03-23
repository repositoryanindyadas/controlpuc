---

# ControlPuc

**ControlPuc** is a hardware-centric automation and remote command execution tool. It utilizes the **Raspberry Pi Pico W** (or Pico 2 W) to act as a standalone, wireless **Human Interface Device (HID)**. By emulating a keyboard/mouse, it allows deterministic keystroke injection and remote control over a target PC without requiring administrative privileges or specialized software on the target machine..

---

## 🧠 Project Overview

ControlPuc is designed around a **hardware-first control philosophy**, where execution is performed outside the operating system's trust boundary. Instead of relying on software agents, it leverages USB HID emulation to interact directly with the system as if it were a human user.

This approach provides:
- High compatibility across systems
- Minimal software footprint
- Reduced dependency on OS-level permissions

---

## 🏗 Architecture

```
[ Host PC (Controller) ]
        │
        │  Wi-Fi (Hotspot / LAN)
        ▼
[ Raspberry Pi Pico W ]
        │
        │  USB HID (Keyboard/Mouse Emulation)
        ▼
[ Target Machine ]
```

### Components

- **Controller (PC Side):**
  - Sends commands over Wi-Fi
  - Provides UI/CLI for interaction

- **Pico W (Bridge Device):**
  - Maintains Wi-Fi connection
  - Parses incoming commands
  - Converts commands into HID actions

- **Target Machine:**
  - Receives input as a standard USB keyboard/mouse
  - Executes commands natively

---

## 🚀 Features

* **Wireless C2 Architecture:** Control the Pico W remotely via a Wi-Fi hotspot or local network.
* **HID Emulation:** Appears as a standard USB Keyboard/Mouse to the target PC.
* **Privilege Bypass:** No admin rights or installations required on the target system.
* **Self-Healing Connection:** Automatically reconnects on network interruptions.
* **Cross-Platform Compatibility:** Works with Windows, Linux, and macOS.
* **Low Footprint:** No persistent files or processes on the target machine.
* **Scriptable Payloads:** Easily extendable command execution logic.

---

## 🛠 Installation Guide

### 1. Setting up the Raspberry Pi Pico W / Pico 2 W (`/for pico`)

The Pico acts as the hardware execution bridge.

1. **Flash Firmware**
   - Install the latest **MicroPython UF2** firmware on the Pico.

2. **Configure Network**
   - Open files in `/for pico`
   - Set:
     ```python
     SSID = "your_hotspot_name"
     PASSWORD = "your_password"
     ```

3. **Upload Files**
   - Use **Thonny** or `ampy`
   - Upload all files to the Pico root directory

4. **Verify Libraries**
   - Ensure required HID libraries exist:
     - `adafruit_hid`
     - `usb_hid` (if used)

---

### 2. Setting up the Control Panel (`/for pc`)

1. **Install Python**
   - Python 3.8+ recommended

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Connect to Network**
   - Ensure PC and Pico are on the same Wi-Fi network

---

## 💻 Usage

### Step 1: Deploy Device
- Plug the Pico W into the target machine
- Wait for Wi-Fi connection (LED indicator)

### Step 2: Start Controller
```bash
python controlpannel.py
```

### Step 3: Send Commands
- Use the interface to:
  - Execute predefined scripts
  - Send raw keystrokes
  - Trigger automation flows

---

## 📜 Command Execution Model

ControlPuc operates on a simple command pipeline:

1. Controller sends instruction → Pico via Wi-Fi
2. Pico parses instruction
3. Instruction translated into HID events
4. HID events injected into target system

Example:
```
"open_cmd"
→ Win + R
→ type "cmd"
→ press Enter
```

---

## 📂 Project Structure

| Path | Description |
|------|------------|
| `for pc/` | PC-side control interface |
| `for pc/controlpannel.py` | Main controller script |
| `for pico/` | MicroPython firmware |
| `for pico/main.py` | Core logic for Pico |
| `lib/` | Required libraries for HID |
| `README.md` | Documentation |

---

## ⚙️ Configuration

### Network Parameters
Modify in Pico code:
```python
SSID = "your_ssid"
PASSWORD = "your_password"
```

### Timing Control
You may need to tune delays for reliability:
```python
time.sleep(0.1)
```

---

## 🔧 Extending the Project

You can expand ControlPuc by:

- Adding new payload scripts
- Implementing encrypted communication
- Building a web-based control dashboard
- Adding multi-device support
- Creating OS-specific payload modules

---

## 🐛 Troubleshooting

### Device Not Recognized
- Use a **USB data cable**
- Check USB port functionality

### Wi-Fi Not Connecting
- Verify SSID and password
- Ensure hotspot is active

### Commands Not Executing Properly
- Increase delay between keystrokes
- Check keyboard layout differences

---

## 🔒 Security Considerations

- Communication is not encrypted by default
- Network exposure should be controlled
- Avoid using on unsecured/public networks

---

## ⚠️ Disclaimer

This project is intended strictly for:

- Educational purposes  
- Authorized penetration testing  
- Security research  

Unauthorized use against systems without explicit permission is illegal. The author assumes no responsibility for misuse.

---

## 📌 Future Improvements

- Encrypted C2 channel
- Better GUI interface
- Plugin-based payload system
- Logging and telemetry
- OTA updates for Pico firmware

---

## 🤝 Contribution

Contributions are welcome.

1. Fork the repository  
2. Create a feature branch  
3. Submit a pull request  

---

## ⭐ Support

If you find this project useful, consider giving it a star.

---
