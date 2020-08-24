import time
import missions as mn
import updates


# Static methods
def mission_begin(plc, fleet):
    plc.mission(mission_received)
    mission_list = fleet.get_mission_list()
    if mission_list:
        mission = mn.get_mission_id(plc, fleet.get_mission_list().json())
        mission_id = fleet.post_mission(mission, 2)
        if mission_id:
            identity = mission_id.json()['id']
            guid = mission_id.json()['mission_id']
            robot_id = mission_id.json()['robot_id']
            return mission_id, (identity, guid, robot_id)
        else:
            return mission_id, 0
    else:
        return mission_list, 0

def accepted(plc, fleet, info):
    time.sleep(0.75)
    updates.mission(plc, fleet, info)
    plc.mission(mission_accepted)
    plc.mission(mission_end)


def end(plc):
    plc.mission(mission_end)


def mission_end(byte_value):
    time.sleep(1)
    if byte_value & 4:
        byte_value -= 4
    if byte_value & 1:
        byte_value -= 1
    return byte_value


def mission_received(byte_value):
    if not byte_value & 4:
        byte_value += 4
    return byte_value


def mission_accepted(byte_value):
    if not byte_value & 1:
        byte_value += 1
    return byte_value
