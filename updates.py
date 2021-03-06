# Dictionary of state a mission can hold
dic = {'Pending': 1, 'Executing': 2, 'Invalid': 3, 'Aborted': 4, 'Done': 5}


def mission(plc, fleet, info):
    (identity, guid, robot_id) = info
    plc.set_recent_mission_id(identity)
    plc.set_recent_mission(fleet.get_mission_number(guid))
    plc.set_recent_robot_id(robot_id)
    print("Updated info")


def mission_queue(plc, fleet, id_dict):
    queue = fleet.get_mission_queue().json()
    keys = ['id', 'state']
    nested_list = [[dictionary[key] for key in keys] for dictionary in queue]
    for niter in range(len(nested_list)):
        nested_list[niter][1] = dic[nested_list[niter][1]]
        if nested_list[niter][1] != 5:  # Don't care for missions that are already Done
            try:
                nested_list[niter].append(id_dict[fleet.get_mission_robot(nested_list[niter][0])])
            except KeyError:
                # If a robot that doesn't exist on the fleet anymore completed a past mission it will be recorded as -1
                nested_list[niter].append(-1)
        plc.write_queue(nested_list[niter], niter * 8, len(nested_list[niter]) - 1)


def robot_status(plc, robots):
    for i, robot in enumerate(robots):
        if robot.connect:
            status = robot.get_status()
            if status:

                status_val = status.json()
                register_value = robot.get_register(50).json()

                keys = ['state_id', 'uptime', 'battery_time_remaining', 'battery_percentage', 'mission_text']
                values = [status_val.get(key) for key in keys]
                values.append(int(register_value["value"]))
        else:
            values = [0, 00000, 00000, 0.0, "No Connection", 0]

        # 284 is the start value in the db and repeats every 270 for each different robot.
        plc.write_status(values, 294 + 280 * i)


def connection(fleet, robots):
    fleet_state = fleet.is_connected()
    robots_states = []
    for robot in robots:
        robots_states.append(robot.is_connected())


def plc_connection(plc, fleet):
    plc.set_connection_status(fleet.connected)

