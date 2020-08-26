from PLC import PLC


class QueuePage(PLC):
    def __init__(self, ip, db):
        super().__init__(ip)
        self.db_in, self.db_out = db

    def write_queue(self, val, start, number=1):
        raw_byte = self.pack(val, '>i%dh' % number)
        self.plc.db_write(self.db_out, start, raw_byte)