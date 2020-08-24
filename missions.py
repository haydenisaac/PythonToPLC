# Mission manipulation

def get_mission_id(plc, mission_list):
    mission_num = plc.get_mission()
    mission_id = {"mission_id": mission_list[mission_num]["guid"]}
    return mission_id

