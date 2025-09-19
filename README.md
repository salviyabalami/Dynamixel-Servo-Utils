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
  Pings a servo by ID and reads basic control table values such as present position, velocity, and torque state. Useful for verifying communication with individual servos.

- **`discover_and_read.py`**  
  Scans all IDs at the selected baud and prints live Present Position values for each detected servo. Useful for monitoring many servos simultaneously.

---

## ⚙️ Requirements

- Python **3.9+**
- [dynamixel-sdk](https://github.com/ROBOTIS-GIT/DynamixelSDK) (`pip install dynamixel-sdk`)
- U2D2 or compatible USB-to-serial adapter
- USB serial drivers (FTDI, CP210x, etc. depending on your OS)

---

## 🔧 Installation & Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/dynamixel-utils.git
cd dynamixel-utils

# (Optional) Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt
