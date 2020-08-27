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
        mission_groups = self.get("mission_groups").json()
        for item in mission_groups:
            if item['name'] == "ROEQ Utility":
                self.guid = item['guid']
                break


    def print_address(self):
        print(self.host)
        print(self.name)

    def get(self, url, value=None):
        status = requests.get(self.host + url, json=value, headers=self.headers)
        return status

    def put(self, url, value):
        status = requests.put(self.host + url, json=value, headers=self.headers)
        return status

    def get_status(self):
        status = self.get("status")
        return status

    def set_state(self, value):
        # Note. You can only pause or play, values 3 & 4
        status = self.put("status", {"state_id": value})
        return status

    def get_charge_mission(self):
        status = self.get("mission_groups/" + self.guid + "/missions").json()
        pass

    def change_state(self, state):
        if state == "Pause":
            status = self.pause()
            return status
        elif state == "Play":
            status = self.play()
            return status
        elif state == "Reset":
            status = self.reset()
            return status
        elif state == "Charge":
            return 0
        else:
            return 0

    def reset(self):
        # Clears an error after an E-Stop
        status = self.put("status", {"clear_error": True})
        print("Cleared Error")
        return status

    def pause(self):
        status = self.set_state(4)
        return status

    def play(self):
        status = self.set_state(3)
        return status
