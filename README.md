# Servo-Scripts
A collection of Python scripts for working with Dynamixel servos (tested on XL330 series with U2D2, Protocol 2.0). Includes utilities for scanning connected servos, changing IDs, and recovering misconfigured or “lost” servos. Provides clear CLI options and setup instructions for macOS, Linux, and Windows.
This repo contains small, focused Python scripts to scan, configure, diagnose, and move DYNAMIXEL servos (Protocol 2.0) using a U2D2 on macOS.

Works great with XL330-M077-T and companions. If one unit reports a different model (e.g., MODEL=1190), it’s still supported—just confirm its Operating Mode and limits first.

🚀 Quick Start
1) Requirements

macOS (USB-C is fine; use a direct USB-C ↔ micro-USB cable if possible)

U2D2 + Power Hub (TTL 3-pin)

7–12 V DC, center-positive power supply (for 6–7 servos, use 12 V / 3–5 A)

Python 3.9+ and VS Code (recommended)

Python packages:

python3 -m pip install --upgrade dynamixel-sdk pyserial

2) Recommended connections

U2D2 USB → Mac

DC supply → U2D2 Power Hub → switch ON

Servo → TTL 3-pin (not RS-485). Orientation: GND(Black) – V+(Red) – DATA(Yellow/White); signal toward the “DYNAMIXEL” text on U2D2.

3) Port name (macOS)

List serial ports:

python3 -m serial.tools.list_ports


Use the /dev/cu.* device (e.g., /dev/cu.usbserial-FTAAMOEC) in each script’s PORT variable.

📁 Scripts Overview

All scripts are small and single-purpose—easy to run and to explain.
Edit the config block at the top (PORT, BAUD, IDS, etc.) to match your setup.

Discovery & IDs

scan_servos.py – scan common baudrates & all IDs; prints (ID, BAUD, MODEL).

change_id_simple.py – safely change a servo’s ID (torque-off → write → reboot → verify).
Run one servo at a time to avoid ID collisions.

Health & Diagnostics

dxl_diagnostics.py – read Operating Mode, Torque, HW Error, Present Position, Profiles.

diag_ids.py – print key status for a list of IDs (error flags, voltage, temp, limits).

Reading positions

discover_and_read.py – scan once at a chosen baud, then GroupSyncRead all Present Positions.

Motion (safe examples)

move_one.py – enable torque, move to a target, read back, torque off.

oscillate_one.py – single-servo 0° ↔ 180° oscillation (with gentle profiles).

oscillate_all_sync.py – GroupSyncWrite all IDs in sync 0° ↔ 180°; prints live angles.

oscillate_safe_subset.py – like above, but safer: smaller range, lower profiles, stagger starts.

Emergency

e_stop.py – torque-off for a list of IDs (your “big red button”).

🧩 Configuration (what to edit in each file)

At the top of each script you’ll see a config block like:

PORT = "/dev/cu.usbserial-FTAAMOEC"  # macOS: use the cu.* device
BAUD = 57600                         # pick one baud and standardize your chain
IDS  = [2, 3, 4, 5, 6, 7]            # IDs you want to act on


PORT: set to your /dev/cu.*.

BAUD: keep consistent across all servos you intend to read/write together (e.g., 57600 or 1,000,000).

IDS: list only the IDs you mean to move. Exclude outliers (e.g., a different model) until verified.

🛠️ Typical Workflows
A) Initial bring-up (one servo)

Wire power + TTL, switch ON.

python3 scan_servos.py → confirm you see ID=1 @ 57600 (MODEL=1200) (or similar).

(Optional) python3 change_id_simple.py → set new ID (e.g., 2).

B) Assign unique IDs (many servos)

Do one servo at a time:

Connect one servo → scan_servos.py to find it.

change_id_simple.py → change 1 → 2, next servo 1 → 3, etc.

Daisy-chain all; scan_servos.py should show [2..N] at the same baud.

C) Live monitor all

Set all to the same BAUD.

python3 discover_and_read.py → auto-discovers IDs at that baud and prints Present Positions.

D) Move everything together

Start with a small group (e.g., 2 servos):
python3 oscillate_safe_subset.py

If stable, use the full set:
python3 oscillate_all_sync.py
