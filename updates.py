# State Dictionary
dic = {'Pending': 1, 'Executing': 2, 'Invalid': 3, 'Aborted': 4, 'Done': 5}


def mission(plc, fleet, info):
    (identity, guid, robot_id) = info
    plc.set_recent_mission_id(identity)
    plc.set_recent_mission(fleet.get_mission_number(guid))
    plc.set_recent_robot_id(robot_id)


def mission_queue(plc, fleet):
    queue = fleet.get_mission_queue().json()[0:100]
    queue_list = [value for dictionary in queue for key, value in dictionary.items() if key not in ['url']]
    queue_list[1::2] = [dic[x] for x in queue_list[1::2]]
    plc.write_queue(queue_list, 0, len(queue_list))


def robot_status(robot):
    status = robot.get_status().json()
    keys = ['state_id', 'state_text', 'battery_percentage', 'mission_text', 'uptime', 'battery_time_remaining']
    values = [status.get(key) for key in keys]
    print(values)

