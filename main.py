import time
import threading
import handshakes
import updates
from MiR import Fleet
from PLC import PLC
from robotpage import RobotPage
from mainpage import MainPage
from queuepage import UpdatesPage
from robot import Robot


def main():
    # Parameters. Odd in from PLC, Even out to PLC.
    main_db = (311, 310)
    robot_db = (321, 320)
    queue_db = (313, 314)
    ip_panel = "192.168.10.5"

    time_start = time.time()

    '''
    Creating PLC objects
    - Main: Front page on HMI. Has missions to send to fleet 
    - Queue: Queue page in PLC. Just downloads the queue from the fleet and writes it to the PLC 
    - Robots: Robot pages in the PLC. Updates all robot statuses to the PLC
    - Check: Check for signals in the PLC.
    '''
    print("Initialising PLC\n" + "-" * 40)
    connect = False
    while not connect:
        plc_main = MainPage(ip_panel, main_db)
        connect = plc_main.is_connected(ip_panel)

    plc_queue = UpdatesPage(ip_panel, queue_db)
    plc_robots = UpdatesPage(ip_panel, robot_db)
    plc_check = PLC(ip_panel)
    hb_main = MainPage(ip_panel, main_db)
    # Creating fleet object
    print("Initialising Fleet\n" + "-" * 40)
    connect = False
    while not connect:
        fleet1 = Fleet()
        connect = fleet1.connected
    fleet1.print_ip()

    '''
    Create Robot objects.
    - Search fleet for robots.
    - Create a dictionary of ids reordered from 1 and reverse them. eg. 4:1 to 1:4.
    - Create a list of robot objects.
    - Create a list of threads for each robot.
    '''
    print("Initialising Robots\n" + "-" * 40)
    robots_list = fleet1.get_robots()
    id_list = [val['id'] for val in robots_list.json()]
    ip_list = [fleet1.get_robot_ip(item).json()['ip'] for item in id_list]
    robots = [Robot(ip) for ip in ip_list]
    robot_ids = {x: i + 1 for i, x in enumerate(id_list)}
    robot_ids[0] = 0
    reversed_robot_ids = {i + 1: x for i, x in enumerate(id_list)}
    reversed_robot_ids[0] = 0
    robot_pages = [RobotPage(ip_panel, robot_db, identity) for identity in robot_ids]
    number_of_robots = len(robots)
    robot_threads = [None] * number_of_robots
    seen = [False] * number_of_robots
    for robot in robots:
        robot.print_address()

    # Mission States
    print("Ready\n" + "-" * 40)

    prev_main_state = plc_check.is_mission_start(main_db[0])  # 311 is where fleet info is stored on PLC
    prev_robot_state = plc_check.is_mission_start(robot_db[0])  # 321 is where robot info is stored on PLC

    while True:
        time_now = time.time()  # Start Timer
        

        # Look for mission_start button
        current_main_state = plc_check.is_mission_start(main_db[0])
        if prev_main_state < current_main_state:
            # Send mission to Fleet
            status_code, info = handshakes.mission_begin(plc_main, fleet1, robot_ids)
            # End Handshake depending on status code of the mission.
            if status_code:
                fleet_thread = threading.Thread(target=handshakes.accepted, args=(plc_main, fleet1, info))
                fleet_thread.start()
            else:
                fleet_thread = threading.Thread(target=handshakes.end, args=(plc_main,))
                fleet_thread.start()
        prev_main_state = current_main_state

        # Look for mission_start button on robot page
        current_robot_state = plc_check.is_mission_start(robot_db[0])
        if prev_robot_state < current_robot_state:
            # Find the specific robot
            identity = plc_check.read_short(robot_db[0], 6)
            # Check there isn't a live thread.
            try:
                seen[identity - 1] = robot_threads[identity - 1].is_alive()
            except AttributeError:
                seen[identity - 1] = False
            except IndexError:
                continue

            # Send mission to specific robot.
            if not seen[identity - 1]:
                status_code, info = handshakes.mission_begin(robot_pages[identity - 1], fleet1, robot_ids,
                                                             robot=reversed_robot_ids[identity])
                if status_code:
                    robot_threads[identity - 1] = threading.Thread(target=handshakes.accepted,
                                                                   args=(robot_pages[identity - 1], fleet1, info))
                    robot_threads[identity - 1].start()
                else:
                    robot_threads[identity - 1] = threading.Thread(target=handshakes.end,
                                                                   args=robot_pages[identity - 1])
                    robot_threads[identity - 1].start()
        prev_robot_state = current_robot_state

        # Update every 3 seconds
        if time_now - time_start > 3:
            try:
                seen_queue = queue_thread.is_alive()
            except UnboundLocalError:
                seen_queue = False

            if not seen_queue:
                print("Updating Queue...")
                queue_thread = threading.Thread(target=updates.mission_queue, args=(plc_queue, fleet1, robot_ids))
                queue_thread.start()

            try:
                seen_status = status_thread.is_alive()
            except UnboundLocalError:
                seen_status = False

            if not seen_status:
                print("Updating Status...")
                status_thread = threading.Thread(target=updates.robot_status, args=(plc_robots, robots))
                status_thread.start()

            time_start = time.time()

        for i in range(number_of_robots):
            # Check for pause, play, reset
            value = plc_check.is_change_state(robot_db[0], 10 + 2 * i)
            if value:
                handshakes.change_state(robot_pages[i], robots[i], value)

        try:
            connection_status = connection_thread.is_alive()
        except UnboundLocalError:
            connection_status = False

        if not connection_status:
            connection_thread = threading.Thread(target=updates.connection, args=(fleet1, robots))
            connection_thread.start()

        try:
            plc_status = plc_thread.is_alive()
        except UnboundLocalError:
            plc_status = False

        if not plc_status:
            plc_thread = threading.Thread(target=updates.plc_connection(hb_main, fleet1))
            plc_thread.start()




if __name__ == "__main__":
    main()
