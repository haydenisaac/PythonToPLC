import snap7
import struct

class PLC:

	def __init__(self, ip):
		self.plc = snap7.client.Client()
		self.plc.connect(ip, 0, 1) ## Always 0, 1 for s1200/1500
		self.plc.get_connected()
		
	def disconnect(self):
		self.plc.disconnect()

	def isConnected(self, ip_panel):
		if self.plc.get_connected():
			print("Connected to PLC at " + ip_panel + "\n" + "-"*40)
			
		else:
			print("Not Connected\n")
			
	def getDB(self, dbNumber, start = 0, amount = 6):
		register = self.plc.db_read(dbNumber, start, amount)
		#print(register)
		return register
		
	def writeDB(self, dbNumber, data, start = 0):
		self.plc.db_write(dbNumber,start , data)
		
	def readUShort(self, dbNumber, byte):
		fromByte = self.getDB(dbNumber, byte, 2) ## Short is 2 bytes
		value = struct.unpack('>H', fromByte)[0]
		return value	
		
	def receivedMission(self):
		## Mission_Start is on byte 4 
		fromByte = self.getDB(311, 4, 1)
		## Check if first bit on
		if fromByte[0]%2 == 1:
			toByte = self.getDB(310, 4, 1)
			if toByte[0]%2 != 1:
				toByte[0] += 0x05
			self.writeDB(310, toByte, start = 4)
			return True
		else:
			
			return False
			
	def completedMission(self):
		toByte = self.getDB(310, 4, 1)
		if toByte[0] > 3: 
			toByte[0] += - 0x04
		if toByte[0] < 2:
			toByte[0] += 0x02
		self.writeDB(310, toByte, start = 4)
		pass;
		
	def getMission(self):
		value = self.readUShort(311, 2)
		if value < 5:
			return value
		else:
			return -1
			
	def getState(self):
		value = self.readUShort(311, 0)
		if value == 3 or value == 4:
			return value
		else:
			return value
			
	def setState(self, val):
		toByte = struct.pack('>H', val)
		self.writeDB(310, toByte)
		
	def setMission(self, val):
		toByte = struct.pack('>H', val)
		self.writeDB(310, toByte, start = 2)
		
		
		
		