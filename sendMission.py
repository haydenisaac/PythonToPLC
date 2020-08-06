print("Importing Packages\n-------------------")
import time
from MiR import Robot


print("Initialising Robot")
mir_23 = Robot()
mir_23.printIP()
missionList = mir_23.getMissionList()

dic = {}
for i in range(len(missionList)):
	item = missionList[i]
	dic[item['name']] = i

print("--"*20)
for mission in dic:
	print(mission)
	print("--"*20)
	
missionChoice = "Load Wall Drop Off Wall"
mission_id = {"mission_id": missionList[dic[missionChoice]]['guid']}	

print(mir_23.getMissionQueue()[-1])
#print(mir_23.getStatus())
#print(mir_23.clearError())


while True:
	FILE = open('test.txt', 'r+')
	signal = FILE.read()
	FILE.close()
	if signal == 'Send':
		mir_23.postMission(mission_id)
		FILE = open('test.txt', 'w+')
		FILE.write('Sent')
		FILE.close()
	print(mir_23.getMissionQueue()[-1])
	time.sleep(.500)
