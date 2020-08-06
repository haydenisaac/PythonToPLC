import snap7
import struct

try: FILE = open('ip.txt', 'r+')
except: print("No Valid file to open")

ip = FILE.readlines()[0]

plc = snap7.client.Client()
 
try: plc.connect(ip, 0, 1)
except: print("Invalid IP")

reg = plc.db_read(2003, 0, 282) ## 282 is the entire register
print(reg)
short = struct.unpack('H', reg)
#b1, b2, t1,t2,t3 , string, short,long, b3,b4 = struct.unpack('2?3L256shl2?',reg)
x = struct.pack('H', 0x6d60)
print(x)

#plc.db_write(2003,274,x)
input()
plc.disconnect()