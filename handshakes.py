import updates


def mission_begin(plc, fleet, id_dict, robot=None):
    plc.mission(plc.mission_received)
    mission_lists = fleet.get_mission_list()  # Change for 200 fix
    plc.status_code(mission_lists[0].status_code)
    try:
        mission_list = mission_lists[0].json() + mission_lists[1].json()
        print(mission_list)
        mission = plc.get_mission_id(mission_list)
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
        print("All Good")
    else:
        pass
        '''
        Charging Mission Here!
        '''


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
