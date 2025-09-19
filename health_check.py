# health_check.py
from dynamixel_sdk import *
PORT="/dev/cu.usbserial-FTAAMOEC"; BAUD=57600; PROTO=2.0
ADDR_HW_ERR=70; ADDR_VOLT=144; ADDR_TEMP=146
def r1(pkt,port,i,a): v,res,err=pkt.read1ByteTxRx(port,i,a); return v,res,err
def r2(pkt,port,i,a): v,res,err=pkt.read2ByteTxRx(port,i,a); return v,res,err
ids=[1,2,3,4,5,6,7]  # put your IDs here

pkt=PacketHandler(PROTO); port=PortHandler(PORT)
assert port.openPort() and port.setBaudRate(BAUD)
for i in ids:
  e,_,_=r1(pkt,port,i,ADDR_HW_ERR); v,_,_=r2(pkt,port,i,ADDR_VOLT); t,_,_=r1(pkt,port,i,ADDR_TEMP)
  print(f"ID {i}: HW_ERR=0b{e:08b}  V={v/10:.1f}V  T={t}°C")
port.closePort()
