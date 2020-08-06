import json, requests

class Robot:
	
	def __init__(self):
		FILE = open('address.txt', 'r+')
		self.ip, auth = FILE.readlines()
		self.ip = self.ip.rstrip('\n')
		FILE.close()
		self.setHost()
		self.headers = {}
		self.setHeaders(auth)
		
	def get(self, url):
		status = requests.get(self.host + url, headers = self.headers)
		self.statusCheck(status, url)
		return status
	
	def post(self, url, jsonVal):
		status = requests.post(self.host + url, json = jsonVal, headers = self.headers)
		self.statusCheck(status, url)
		return status
		
	def put(self, url, jsonVal):
		status = requests.put(self.host + url, json = jsonVal, headers = self.headers)
		self.statusCheck(status, url)
		return status
	
	def setHeaders(self, auth, content = "application/json"):
		self.headers["Content-Type"] = content
		self.headers["Authorization"] = auth
		
	def printIP(self):
		print("MiR ip address is: " + self.ip + "\n")
	
	def setHost(self, url = "/api/v2.0.0/"):
		self.host = "http://" + self.ip + url
		
	def getMissionList(self):
		missionList = self.get("mission_groups/75b83d4a-5f93-11ea-88ff-0001299216bf/missions")
		return missionList.json()
	
	def getMissionQueue(self):
		missionQueue = self.get("mission_queue")
		return missionQueue.json()

	def postMission(self, mission_id):
		self.post('mission_queue/', mission_id)
		
	def getStatus(self):
		status = requests.get(self.host + "status", headers = self.headers)
		for key in status.json():
			print(key,status.json()[key])
			print("--"*20)
			
		return status.json()
		
	def clearError(self):
		self.put("status", {"clear_error": True})
		self.put("status", {"state_id": 3})
		print("Cleared Error")
		
	def statusCheck(self, status, type):
		if status:
			print(status)
			#print("Sucessful connection to " + type +".\n\n")
		else:
			print(status)
			#print("Failed to connect to '" + type+"'.\n")
		

		
	
	