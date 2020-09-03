import snap7
import struct


class PLC:

    def __init__(self, ip):
        self.plc = snap7.client.Client()
        self.plc.connect(ip, 0, 1)  # Always 0, 1 for s1200/1500

    def is_connected(self, ip_panel):
        if self.plc.get_connected():
            print("Connected to PLC at " + ip_panel + "\n" + "-" * 40)
        else:
            print("Not Connected\n")

    def read_short(self, db, byte, number=1):
        raw_byte = self.plc.db_read(db, byte, 2 * number)  # Short is 2 bytes
        value = struct.unpack('>%dh' % number, raw_byte)[0]
        return value

    def read_bool(self, db, byte, number=1):
        raw_byte = self.plc.db_read(db, byte, number)
        value = struct.unpack('>%dB' % number, raw_byte)[0]
        return value

    def write_short(self, db, byte, start, number=1):
        raw_byte = self.pack(byte, '>%dh' % number)
        self.plc.db_write(db, start, raw_byte)

    def write_bool(self, db, byte, start, number=1):
        raw_byte = self.pack(byte, '>%dB' % number)
        self.plc.db_write(db, start, raw_byte)

    def write_int(self, db, byte, start, number=1):
        raw_byte = self.pack(byte, '>%di' % number)
        self.plc.db_write(db, start, raw_byte)

    def write_string(self, string, db, start):
        byte_string = bytes(string, 'utf-8')
        total = (254, len(byte_string), byte_string)
        raw_byte = struct.pack("2B%ds" % len(byte_string), *total)
        self.plc.db_write(db, start, raw_byte)

    @staticmethod
    def pack(byte, fmt):
        if type(byte) == list:
            raw_byte = struct.pack(fmt, *byte)
        else:
            raw_byte = struct.pack(fmt, byte)
        return raw_byte

    # Check for functions
    def is_mission_start(self, db=311, start=4):
        # Mission_Start is on byte 4
        byte = self.read_bool(db, start)
        if byte & 1:
            return True
        else:
            return False

    def is_change_state(self, db, start):
        byte = self.read_bool(db, start)
        return byte

    def mission(self, method, db_out):
        # Buttons are at byte 4 of DB310
        byte_val = self.read_bool(db_out, 4)
        byte_val = method(byte_val)
        self.write_bool(db_out, byte_val, 4)

    def get_mission(self, db):
        value = self.read_short(db, 2)
        if value < 5:
            return value
        else:
            return -1

    def get_mission_id(self, mission_list, db):
        mission_num = self.get_mission(db)
        mission_id = {"mission_id": mission_list[mission_num]["guid"]}
        return mission_id

    @staticmethod
    def check_state_type(byte_value):
        if byte_value & 1:
            return "Pause"
        elif byte_value & 2:
            return "Play"
        elif byte_value & 4:
            return "Reset"
        elif byte_value & 8:
            return "Charge"

    # Static Methods
    @staticmethod
    def mission_end(byte_value):
        # Busy and Accept off
        if byte_value & 4:
            byte_value -= 4
        if byte_value & 1:
            byte_value -= 1
        return byte_value

    @staticmethod
    def mission_received(byte_value):
        # Busy on
        if not byte_value & 4:
            byte_value += 4
        return byte_value

    @staticmethod
    def mission_accepted(byte_value):
        # Accept on
        if not byte_value & 1:
            byte_value += 1
        return byte_value
