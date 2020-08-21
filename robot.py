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

    def get_status(self):
        status = self.get("status")
        return status



