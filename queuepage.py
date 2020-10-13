from PLC import PLC


class UpdatesPage(PLC):
    def __init__(self, ip, db):
        super().__init__(ip)
        self.db_in, self.db_out = db

    def write_queue(self, val, start, number=1):
        raw_byte = self.pack(val, '>i%dh' % number)
        self.plc.db_write(self.db_out, start, raw_byte)

    def write_status(self, val, start=284):
        raw_byte = self.pack(val[:-1], '>h2if')
        self.plc.db_write(self.db_out, start, raw_byte)
        self.write_string(val[-1], self.db_out, start + 14)
