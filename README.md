# Dynamixel Servo Utilities

A collection of Python scripts for working with **Dynamixel servos** (tested on XL330 series with U2D2, Protocol 2.0).  
Includes utilities for scanning connected servos, changing IDs, recovering misconfigured servos, health checks, ping/read diagnostics, and monitoring.

---

## 📂 Included Scripts

- **`scan_servos.py`**  
  Scans a given serial port and lists all detected servos, reporting ID, position, voltage, temperature, and status.

- **`change_id.py`**  
  Safely changes the ID of a single connected servo.  
  ⚠️ *Important: Only power one servo at a time when running this script to avoid conflicts.*

- **`recover.py`**  
  Attempts to find and recover a misconfigured servo by scanning across common baud rates.

- **`health_check.py`**  
  Performs a quick diagnostic on each detected servo (temperature, voltage, error flags, etc.) to verify that it is operating within safe ranges.

- **`ping_and_read.py`**  
  Scans all IDs at the selected baud and prints live Present Position values for each detected servo. Useful for monitoring many servos simultaneously.

---

## ⚙️ Requirements

- Python **3.9+**
- [dynamixel-sdk](https://github.com/ROBOTIS-GIT/DynamixelSDK) (`pip install dynamixel-sdk`)
- U2D2 or compatible USB-to-serial adapter
- USB serial drivers (FTDI, CP210x, etc., depending on your OS)

---

## 🔧 Installation & Setup

### 1) Clone and install Python deps
```bash
# Clone the repository
git clone https://github.com/yourusername/dynamixel-utils.git
cd dynamixel-utils

# (Optional) Create a virtual environment
python3 -m venv venv
# macOS/Linux:
source venv/bin/activate
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```
### 2) Hardware hookup (in this order)

1. **Connect the servo to the U2D2** with the proper TTL cable (be sure the orientation matches the connector key).  
2. **Connect external power to the U2D2** (barrel jack/terminal block) with a supply that matches your servo’s voltage spec.  
   - ⚠️ Use the correct voltage and polarity per the servo datasheet.  
3. **Connect the U2D2 to your computer** via USB.  

---

### 3) Determine which serial port the U2D2 is using

Use your terminal to find the device name:

- **macOS**
  ```bash
  ls /dev/tty.usb* /dev/cu.usb* 2>/dev/null
  # Example result: /dev/cu.usbserial-FTAAMOEC
  ```
- **Linux**
 ```bash
- ls /dev/ttyUSB*
# Example result: /dev/ttyUSB0
```
- **Windows**
  Open Device Manager → Expand Ports (COM & LPT) → look for USB Serial Port (COM3) or similar.

### 4) Update the PORT value in the scripts
Open the Python script you plan to run (e.g., scan_servos.py) and set the PORT constant to the device you found in step 3.
```bash
# macOS example:
PORT = "/dev/cu.usbserial-FTAAMOEC"

# Linux example:
PORT = "/dev/ttyUSB0"

# Windows example:
PORT = "COM3"
```
