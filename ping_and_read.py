# ping_and_read.py
# Scans once (current BAUD) to discover IDs, then reads all positions via GroupSyncRead.

from dynamixel_sdk import *   # Dynamixel SDK for servo communication
import time

PORT = "/dev/cu.usbserial-FTAAMOEC"  
BAUD = 57600                          # Baud rate (all servos must use same)
ID_RANGE = range(0, 253)              # Full ID range (0–252 for Dynamixel)

PROTO = 2.0                           # Dynamixel protocol version
ADDR_PRESENT_POSITION = 132           # Control table address for present position
LEN_PRESENT_POSITION  = 4             # Data length (bytes) for present position
STEP_TO_DEG = 360.0 / 4096.0          # Conversion: raw steps → degrees

def open_bus():
    """Open the serial port and initialize the packet handler."""
    port = PortHandler(PORT)
    pkt  = PacketHandler(PROTO)
    if not port.openPort():
        raise RuntimeError(f"Could not open {PORT}")
    if not port.setBaudRate(BAUD):
        raise RuntimeError(f"Could not set baud {BAUD}")
    return port, pkt

def quick_scan(port, pkt, id_range=ID_RANGE, retries=2, delay=0.005):
    """Ping each possible ID to find which servos respond."""
    found = []
    print(f"Scanning IDs at {BAUD} baud …")
    for dxl_id in id_range:
        ok = False
        for _ in range(retries):  # retry a couple times for reliability
            model, res, err = pkt.ping(port, dxl_id)
            if res == COMM_SUCCESS and err == 0:
                found.append(dxl_id)
                ok = True
                break
            time.sleep(delay)
    return sorted(found)

def main():
    port = None
    try:
        # 1. Open communication
        port, pkt = open_bus()

        # 2. Scan for connected servos
        ids = quick_scan(port, pkt)
        print("Found IDs:", ids)
        if not ids:
            print("No servos responded. Check power, wiring, and baud rate.")
            return

        # 3. Create a GroupSyncRead to read all positions at once
        group = GroupSyncRead(port, pkt, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
        for i in ids:
            if not group.addParam(i):  # Add each found ID
                print(f"⚠️ Could not add ID {i} to GroupSyncRead")

        print("\nReading Present Position for IDs:", ids)
        print("Press Ctrl+C to stop.\n")

        # 4. Loop: continuously read present positions
        while True:
            comm = group.txRxPacket()  # send/receive sync read
            if comm != COMM_SUCCESS:
                print("Comm error:", pkt.getTxRxResult(comm))
                time.sleep(0.1)
                continue

            line = []
            for i in ids:
                if group.isAvailable(i, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION):
                    raw = group.getData(i, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
                    deg = raw * STEP_TO_DEG
                    line.append(f"ID {i}: {deg:7.2f}° ({raw:4d})")
                else:
                    line.append(f"ID {i}: N/A")
            print(" | ".join(line))
            time.sleep(0.10)  # ~10Hz update rate

    except KeyboardInterrupt:
        # Allow user to exit cleanly with Ctrl+C
        pass
    finally:
        # Always close port on exit
        if port:
            port.closePort()
            print("Port closed.")

if __name__ == "__main__":
    main()
