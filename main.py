print("\nImporting Packages\n"+"-"*40)
import time
from MiR import Robot
from PLC import PLC

def getMissionID(plc, missionList):
	missionNum = plc.getMission()
	if missionNum < 0:
		missionNum = 2 ## 2 = Wall to Wall
	missionID = {"mission_id": missionList[missionNum]["guid"]}
	plc.setMission(missionNum)
	return missionID
	
def configStates(plc, robot):
	plc.setState(robot.getState())
	robot.setState(plc.getState())

def main():
	## Creating PLC object
	print("Initialising PLC\n"+"-"*40)
	ip_panel = "192.168.1.204"
	plc_1 = PLC(ip_panel)
	plc_1.isConnected(ip_panel)
	
	
	## Creating robot object
	print("Initialising Robot\n"+"-"*40)
	#mir_23 = Robot()
	#mir_23.printIP()
	#missionList = mir_23.getMissionList()
	
	while True:
		print("PLC state: %d" %plc_1.getState())
		print("Writing robot state: %d" %5)
		plc_1.setState(5)
		
		#configStates(plc_1, mir_23)
		if plc_1.receivedMission():
			#missionID = getMissionID(plc_1, missionList)
			print("Mission Sent")
			#mir_23.postMission(missionID)
			
			
		if plc_1.getDB(311, start = 4, amount = 1)[0] == 2:
			plc_1.completedMission()
		
		time.sleep(.750)

	#input()
	plc_1.disconnect()




if __name__ == "__main__":
	main()
