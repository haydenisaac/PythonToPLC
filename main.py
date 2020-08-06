print("\nImporting Packages\n"+"-"*40)
import time
from MiR import Robot
from PLC import PLC

def getMissionID(plc, missionList):
	missionNum = plc.getMission()
	if missionNum < 0:
		missionNum = 2
	missionID = {"mission_id": missionList[missionNum]["guid"]}
	return missionID

def main():
	## Creating PLC object
	print("Initialising PLC\n"+"-"*40)
	ip_panel = "192.168.1.204"
	plc_1 = PLC(ip_panel)
	plc_1.isConnected(ip_panel)
	
	
	## Creating robot object
	print("Initialising Robot\n"+"-"*40)
	mir_23 = Robot()
	mir_23.printIP()
	missionList = mir_23.getMissionList()
	
	## Creating a dictionary of missions
	#dic = {}
	#for i in range(len(missionList)):
	#	item = missionList[i]
	#	dic[item['name']] = i
	
	print("Ready")
	while True:
		if plc_1.receivedMission():
			#missionID = getMissionID(plc_1, missionList)
			#mir_23.postMission(missionID)
			print(plc_1.getStatus())
			print(plc_1.getMission())
			plc_1.setStatus(plc_1.getStatus())
			plc_1.setMission(plc_1.getMission())
			
		if plc_1.getDB(311, start = 4, amount = 1)[0] == 2:
			plc_1.completedMission()
			
		#print(mir_23.getMissionQueue()[-1])
		time.sleep(.750)

	input()
	plc_1.disconnect()



if __name__ == "__main__":
	main()
