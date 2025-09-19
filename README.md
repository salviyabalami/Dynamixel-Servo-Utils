# Dynamixel Servo Utilities

A collection of Python scripts for working with **Dynamixel servos** (tested on XL330 series with U2D2, Protocol 2.0).  
Includes utilities for scanning connected servos, changing IDs, and recovering misconfigured or “lost” servos.  

---

## 📂 Included Scripts

- **`scan_servos.py`**  
  Scans a given serial port and lists all detected servos, reporting ID, position, voltage, temperature, and status.

- **`change_id.py`**  
  Safely changes the ID of a single connected servo.  
  ⚠️ *Important: Only power one servo at a time when running this script to avoid conflicts.*

- **`recover.py`**  
  Attempts to find and recover a misconfigured servo by scanning across common baud rates.

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
