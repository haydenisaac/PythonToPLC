import time
import threading
import handshakes
import updates
from MiR import Fleet
from PLC import PLC


def main():
    time_start = time.time()
    # Creating PLC object
    print("Initialising PLC\n" + "-" * 40)
    ip_panel = "192.168.10.5"
    plc1 = PLC(ip_panel)
    plc1.is_connected(ip_panel)

    # Creating robot object
    print("Initialising Robot\n" + "-" * 40)
    fleet1 = Fleet()
    fleet1.print_ip()

    # Mission States
    print("Ready\n" + "-" * 40)
    while True:
        time_now = time.time()

        if plc1.is_mission_start():
            mission_id, info = handshakes.mission_begin(plc1, fleet1)
            if mission_id:
                thread1 = threading.Thread(handshakes.accepted(plc1, fleet1, info))
                thread1.start()

        if time_now - time_start > 3:
            print("Updating Queue.")
            thread2 = threading.Thread(updates.mission_queue(plc1, fleet1))
            thread2.start()
            time_start = time.time()


if __name__ == "__main__":
    main()
