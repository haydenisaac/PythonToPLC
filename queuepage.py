from PLC import PLC


class UpdatesPage(PLC):
    def __init__(self, ip, db):
        super().__init__(ip)
        self.db_in, self.db_out = db

    def write_queue(self, val, start, number=1):
        raw_byte = self.pack(val, '>i%dh' % number)
        self.plc.db_write(self.db_out, start, raw_byte)

    def write_status(self, val, start=294):
        raw_byte = self.pack(val[:-2], '>h2if')
        self.plc.db_write(self.db_out, start, raw_byte)
        self.write_string(val[-2], self.db_out, start + 14)
        extra_data = self.pack(val[-1], '>h')
        self.plc.db_write(self.db_out, start + 270, extra_data)
