import requests


class Robot:
    def __init__(self, ip):
        self.host = "http://" + ip + "/api/v2.0.0/"
        file = open('address.txt', 'r+')
        ignore, auth = file.readlines()
        file.close()
        auth = auth.rstrip('\n')
        self.headers = {"Content-Type": "application/json", "Authorization": auth}
        self.name = self.get_status().json()['robot_name']

    def print_address(self):
        print(self.host)
        print(self.name)

    def get(self, url, value=None):
        status = requests.get(self.host + url, json=value, headers=self.headers)
        return status

    def put(self, url, value):
        status = requests.get(self.host + url, json=value, headers=self.headers)
        return status

    def get_status(self):
        status = self.get("status")
        return status

    def set_state(self, value):
        # Note. You can only pause or play, values 3 & 4
        status = self.put("status", {"state_id": value})
        return status

    def reset(self):
        # Clears an error after an E-Stop
        self.put("status", {"clear_error": True})
        self.set_state(3)  # 3 = Ready
        print("Cleared Error")

    def pause(self):
        status = self.set_state(4)
        return status

    def play(self):
        status = self.set_state(3)
        return status
