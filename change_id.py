# change_id_simple.py
# Purpose: change a DYNAMIXEL (Protocol 2.0) servo ID safely.

from dynamixel_sdk import *
import time

PORT = "/dev/cu.usbserial-FTAAMOEC"      # macOS: use cu.* device
SAFE_BAUDS = [57600, 115200, 1000000]    # bauds we’ll try
PROTO = 2.0

ADDR_TORQUE_ENABLE = 64   # 0=off, 1=on
ADDR_ID            = 7    # EEPROM (write new ID here)

def find_baud_for_id(port, packet, dxl_id):
    """Ping the ID at common bauds; return (baud, model) if found."""
    for b in SAFE_BAUDS:
        if port.setBaudRate(b):
            model, res, err = packet.ping(port, dxl_id)
            if res == COMM_SUCCESS and err == 0:
                return b, model
    return None, None

def main():
    # ask user which ID to change 
    old_id = int(input("Current ID: ").strip())
    new_id = int(input("New ID: ").strip())
    if old_id == new_id:
        print("Old and new ID are the same. Nothing to do."); return

    #open port 
    port   = PortHandler(PORT)
    packet = PacketHandler(PROTO)
    if not port.openPort():
        print(f"Could not open {PORT}"); return

    #find the servo at some baud 
    baud, model = find_baud_for_id(port, packet, old_id)
    if baud is None:
        print(f"ID {old_id} not found at {SAFE_BAUDS}"); port.closePort(); return
    print(f"Found ID {old_id} at {baud} baud (model {model})")

    # torque off before EEPROM write
    packet.write1ByteTxRx(port, old_id, ADDR_TORQUE_ENABLE, 0)

    #write new ID
    print(f"Writing new ID {new_id} …")
    res, err = packet.write1ByteTxRx(port, old_id, ADDR_ID, new_id)
    if res != COMM_SUCCESS or err != 0:
        print("Write failed:", packet.getTxRxResult(res), packet.getRxPacketError(err))
        port.closePort(); return

    # reboot so new ID takes effect
    packet.reboot(port, new_id)
    time.sleep(0.3)              # small delay after reboot
    port.setBaudRate(baud)       # restore baud

    # verify new ID responds 
    model2, res, err = packet.ping(port, new_id)
    if res == COMM_SUCCESS and err == 0:
        print(f"Success! {old_id} → {new_id} (model {model2})")
    else:
        print("New ID did not respond. Power-cycle and rescan.")

    port.closePort()

if __name__ == "__main__":
    main()
