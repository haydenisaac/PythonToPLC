# State Dictionary
dic = {'Pending': 1, 'Executing': 2, 'Invalid': 3, 'Aborted': 4, 'Done': 5}


def mission(plc, fleet, info):
    (identity, guid, robot_id) = info
    plc.set_recent_mission_id(identity)
    plc.set_recent_mission(fleet.get_mission_number(guid))
    plc.set_recent_robot_id(robot_id)


def mission_queue(plc, fleet, id_dict):
    queue = fleet.get_mission_queue().json()[0:100]
    keys = ['id', 'state']
    nested_list = [[dictionary[key] for key in keys] for dictionary in queue]
    for niter in range(len(nested_list)):
        nested_list[niter][1] = dic[nested_list[niter][1]]
        if nested_list[niter][1] != 5:  # Don't care for missions that are already Done
            nested_list[niter].append(id_dict[fleet.get_mission_robot(nested_list[niter][0])])

        plc.write_queue(nested_list[niter], niter * 8, len(nested_list[niter]) - 1)


def robot_status(plc, robots):
    for i, robot in enumerate(robots):
        status = robot.get_status().json()
        keys = ['state_id', 'uptime', 'battery_time_remaining', 'battery_percentage', 'mission_text']
        values = [status.get(key) for key in keys]
        plc.write_status(values, 284 + 260 * i)
