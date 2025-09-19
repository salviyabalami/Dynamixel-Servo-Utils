# scan_servos.py
# Scans all possible IDs at several baud rates to discover connected Dynamixel servos.

from dynamixel_sdk import *   # Import Dynamixel SDK
import time

PORT = "/dev/cu.usbserial-FTAAMOEC"   # macOS: use cu.* device for serial
BAUDS = [57600, 115200, 1000000, 2000000]  # Common stable baud rates
ID_RANGE = range(0, 253)               # Valid Dynamixel IDs (0–252)
PROTO = 2.0                            # Protocol version (most servos use 2.0)
RETRIES = 2                            # Retry each ping this many times
DELAY = 0.01                           # Small delay between retries

def main():
    # Initialize port (USB/serial) and packet handler (protocol)
    port = PortHandler(PORT)
    packet = PacketHandler(PROTO)

    # Try to open the serial port
    if not port.openPort():
        print(f" Could not open {PORT}")
        return

    found = []  # store discovered servos

    # Try each baud rate
    for b in BAUDS:
        try:
            if not port.setBaudRate(b):
                print(f" Driver rejected baud {b}")
                continue
        except Exception as e:
            print(f" Could not set baud {b}: {e}")
            continue

        print(f"\n Scanning at {b}...")

        # Ping every possible ID
        for dxl_id in ID_RANGE:
            ok = False
            for _ in range(RETRIES):
                model, res, err = packet.ping(port, dxl_id)
                if res == COMM_SUCCESS and err == 0:
                    # Found a servo → print its info
                    print(f" ID={dxl_id:<3}  BAUD={b:<7}  MODEL={model}")
                    found.append((dxl_id, b, model))
                    ok = True
                    break
                time.sleep(DELAY)  # wait a moment before retrying

    # Close the port after scanning
    port.closePort()

    # If nothing found, print message
    if not found:
        print("\n No servos found.")

if __name__ == "__main__":
    main()
