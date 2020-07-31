import snap7

try: FILE = open('ip.txt', 'r+')
except: print("No Valid file to open")

ip = FILE.readlines()[0]

plc = snap7.client.Client()
 
try: plc.connect(ip, 0, 1)
except: print("Invalid IP")

reg = plc.db_read(2003, 0, 282) ## 282 is the entire register
print(reg)

input()
plc.disconnect()