import requests
import simplejson


class Fleet:

    def __init__(self):
        file = open('address.txt', 'r+')
        self.ip, self.auth = file.readlines()
        self.ip = self.ip.rstrip('\n')
        self.auth = self.auth.rstrip('\n')
        file.close()
        self.host = "http://" + self.ip + "/api/v2.0.0/"
        self.headers = {}
        self.set_headers()
        self.connected = False
        try:
            mission_groups = self.get("mission_groups").json()
            for item in mission_groups:
                if item['name'] == "200 Demo":
                    self.guid = item['guid']
                    break
            self.connected = True
        except requests.exceptions.ConnectionError:
            print("Failed to reach the fleet. Trying again.")
        except simplejson.errors.JSONDecodeError:
            print("Failed to gather missions from fleet")

    def is_connected(self):
        try:
            self.get("status/")
            self.connected = True
            return True
        except requests.exceptions.ConnectionError:
            self.connected = False
            return False

    def set_headers(self, content="application/json"):
        self.headers["Content-Type"] = content
        self.headers["Authorization"] = self.auth

    def print_ip(self):
        print("MiR ip address is: " + self.ip + "\n")
        print("Authorization code is: " + self.auth + "\n")

    def get(self, url, value=None):
        status = requests.get(self.host + url, json=value, headers=self.headers)
        return status

    def post(self, url, value):
        status = requests.post(self.host + url, json=value, headers=self.headers)
        return status

    def put(self, url, value):
        status = requests.put(self.host + url, json=value, headers=self.headers)
        return status

    # Get functions
    def get_mission_list(self):
        try:
            mission_list = self.get("mission_groups/" + self.guid + "/missions")
        except requests.exceptions.ConnectionError:
            mission_list = None
        return mission_list

    def get_mission_queue(self):
        mission_queue = self.get("mission_scheduler?limit=100")
        return mission_queue

    def get_mission_status(self, identity):
        status = self.get("mission_scheduler/%d" % identity)
        return status

    def get_robots(self):
        status = self.get("robots")
        return status

    def get_robot_ip(self, identity):
        status = self.get("robots/%d" % identity)
        return status

    # Post functions
    def post_mission(self, mission_id, direct=None):
        if direct is not None:
            mission_id["robot_id"] = direct
        state = self.post('mission_scheduler/', mission_id)
        return state

    def get_mission_number(self, guid):
        mission_list = self.get_mission_list().json()
        for i in range(len(mission_list)):
            if mission_list[i]['guid'] == guid:
                return i
        return 0

    def get_mission_robot(self, identity):
        state = self.get_mission_status(identity)
        return state.json()['robot_id']
