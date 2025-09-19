from dynamixel_sdk import *
PORT="/dev/cu.usbserial-FTAAMOEC"; BAUD=57600; PROTO=2.0
IDS=[4,7]  # <-- focus on the problem servos

ADDR_ERR=70; ADDR_VOLT=144; ADDR_TEMP=146
ADDR_POS=132; ADDR_MOV=122
ADDR_PROF_ACC=108; ADDR_PROF_VEL=112
ADDR_VEL_LIMIT=44; ADDR_PWM_LIMIT=36; ADDR_CUR_LIMIT=38
ADDR_MIN_POS=52; ADDR_MAX_POS=48

pkt=PacketHandler(PROTO); port=PortHandler(PORT)
assert port.openPort() and port.setBaudRate(BAUD)

def r1(i,a): return pkt.read1ByteTxRx(port,i,a)[0]
def r2(i,a): return pkt.read2ByteTxRx(port,i,a)[0]
def r4(i,a): return pkt.read4ByteTxRx(port,i,a)[0]

for i in IDS:
    err  = r1(i,ADDR_ERR)
    volt = r2(i,ADDR_VOLT)/10.0
    temp = r1(i,ADDR_TEMP)
    pos  = r4(i,ADDR_POS)
    mov  = r1(i,ADDR_MOV)
    pacc = r4(i,ADDR_PROF_ACC)
    pvel = r4(i,ADDR_PROF_VEL)
    vlim = r4(i,ADDR_VEL_LIMIT)
    plim = r2(i,ADDR_PWM_LIMIT)
    clim = r2(i,ADDR_CUR_LIMIT)
    minp = r4(i,ADDR_MIN_POS)
    maxp = r4(i,ADDR_MAX_POS)
    print(f"\nID {i}: ERR=0b{err:08b}  V={volt:.1f}V  T={temp}°C  pos={pos}  moving={mov}")
    print(f"   profile(acc,vel)=({pacc},{pvel})  vel_limit={vlim}  pwm_limit={plim}  cur_limit={clim}")
    print(f"   pos_limits=[{minp},{maxp}]")

port.closePort()
