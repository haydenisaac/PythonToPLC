from PLC import PLC


class MainPage(PLC):
    def __init__(self, ip, db):
        super().__init__(ip)
        self.db_in, self.db_out = db

    def status_code(self, code):
        self.write_short(self.db_out, code, 12)

    def set_recent_mission(self, val):
        self.write_short(self.db_out, val, 2)

    def set_recent_mission_id(self, val):
        self.write_int(self.db_out, val, 6)

    def set_recent_robot_id(self, val):
        self.write_short(self.db_out, val, 10)

    def is_mission_start(self, db=0, start=4):
        db = self.db_in
        return super().is_mission_start(db, start)

    def get_mission(self, db):
        db = self.db_in
        return super().get_mission(db)

    def mission(self, method, db_out=0):
        db_out = self.db_out
        return super().mission(method, db_out)

    def get_mission_id(self, mission_list, db=0):
        db = self.db_in
        return super().get_mission_id(mission_list, db)

    def is_mission_acknowledged(self, start=4):
        return not super().is_mission_start(self.db_in, start)
