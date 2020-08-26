import time
import updates


def mission_begin(plc, fleet, id_dict, robot=None):
    time.sleep(1)
    plc.mission(plc.mission_received)
    mission_list = fleet.get_mission_list()
    plc.status_code(mission_list.status_code)
    try:
        mission = plc.get_mission_id(mission_list.json())
        mission_id = fleet.post_mission(mission, robot)  # Can have a specific robot in mind
        plc.status_code(mission_id.status_code)
        try:
            identity = mission_id.json()['id']
            guid = mission_id.json()['mission_id']
            robot_id = mission_id.json()['robot_id']
            return mission_id, (identity, guid, id_dict[robot_id])
        except KeyError:
            print("Mission Failed")
            return mission_id, 0
    except TypeError:
        print("Type Error mission failed")
        return mission_list, 0


def change_state(plc, robot, byte_value):
    state = plc.check_state_type(byte_value)
    status = robot.change_state(state)
    if status:
        print(status.json())
        print("All Good")
    else:
        pass
        '''
        Charging Mission Here!
        '''


def accepted(plc, fleet, info):
    updates.mission(plc, fleet, info)
    time.sleep(1)
    plc.mission(plc.mission_accepted)
    time.sleep(1)
    plc.mission(plc.mission_end)


def end(plc):
    time.sleep(1)
    plc.mission(plc.mission_end)
