import updates


def mission_begin(plc, fleet, id_dict, robot=None):
    plc.mission(plc.mission_received)
    mission_list = fleet.get_mission_list()
    try:
        plc.status_code(mission_list.status_code)
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
        return 0, 0
    except AttributeError:
        print("Unable to connect to Fleet")
        return 0, 0


def change_state(plc, robot, byte_value):
    state = plc.check_state_type(byte_value)
    if robot.connect:
        status = robot.change_state(state)
        if status:
            print("All Good")
    else:
        print("Robot not connected")


def accepted(plc, fleet, info):
    updates.mission(plc, fleet, info)
    prev_value = plc.is_mission_acknowledged()
    plc.mission(plc.mission_accepted)
    while True:
        current_value = plc.is_mission_acknowledged()
        if prev_value < current_value:
            break
        prev_value = current_value

    plc.mission(plc.mission_end)


def end(plc):
    plc.mission(plc.mission_end)
    return 0
