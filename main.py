import time
import threading
import handshakes
import updates
from MiR import Fleet
from PLC import PLC
from robotpage import RobotPage
from mainpage import MainPage
from queuepage import QueuePage
from robot import Robot


def main():
    time_start = time.time()
    # Creating PLC object
    # Creating PLC object
    print("Initialising PLC\n" + "-" * 40)
    ip_panel = "192.168.10.5"
    plc_main = MainPage(ip_panel, (311, 310))
    plc_queue = QueuePage(ip_panel, (313, 314))
    plc_status = QueuePage(ip_panel, (321, 320))
    plc_check = PLC(ip_panel)

    # Creating robot object
    print("Initialising Robot\n" + "-" * 40)
    fleet1 = Fleet()
    fleet1.print_ip()

    # Search for available robots in the fleet
    robots_list = fleet1.get_robots()
    id_list = [val['id'] for val in robots_list.json()]
    ip_list = [fleet1.get_robot_ip(item).json()['ip'] for item in id_list]
    robots = [Robot(ip) for ip in ip_list]
    robot_ids = {x: i + 1 for i, x in enumerate(id_list)}
    robot_ids[0] = 0
    reversed_robot_ids = {i + 1: x for i, x in enumerate(id_list)}
    reversed_robot_ids[0] = 0
    robot_pages = [RobotPage(ip_panel, (321, 320), identity) for identity in robot_ids]
    number_of_robots = len(robots)
    robot_threads = [None] * number_of_robots
    seen = [False] * number_of_robots
    print(robot_threads[0])

    for robot in robots:
        robot.print_address()

    # Mission States
    print("Ready\n" + "-" * 40)
    while True:
        time_now = time.time()

        # Look for mission_start button
        if plc_check.is_mission_start(311):
            try:
                seen_mission = fleet_thread.is_alive()
            except UnboundLocalError:
                seen_mission = False

            if not seen_mission:
                status_code, info = handshakes.mission_begin(plc_main, fleet1, robot_ids)
                if status_code:
                    fleet_thread = threading.Thread(target=handshakes.accepted, args=(plc_main, fleet1, info))
                    fleet_thread.start()
                else:
                    fleet_thread = threading.Thread(target=handshakes.end, args=plc_main)
                    fleet_thread.start()

        if plc_check.is_mission_start(321):
            identity = plc_check.read_short(321, 6)
            print(identity - 1)
            try:
                seen[identity - 1] = robot_threads[identity - 1].is_alive()
            except AttributeError:
                seen[identity - 1] = False
            except IndexError:
                continue

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
                time_start = time.time()

            try:
                seen_status = status_thread.is_alive()
            except UnboundLocalError:
                seen_status = False

            if not seen_status:
                print("Updating Status...")
                status_thread = threading.Thread(target=updates.robot_status, args=(plc_status, robots))
                status_thread.start()

        for i in range(number_of_robots):
            # Check for pause, play, reset
            value = plc_check.is_change_state(321, 10 + 260 * i)
            if value:
                handshakes.change_state(robot_pages[i], robots[i], value)

        # cycle_time = time.time() - time_now
        # print(cycle_time)

        time.sleep(0.005)


if __name__ == "__main__":
    main()
