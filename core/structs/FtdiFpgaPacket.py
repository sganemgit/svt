
class FtdiFpgaPacket:


    def __init__(self):
        self.op_code = 0
        self.payload_length = 0
        self.payload_32 = list()

    def append_32bit_word(self, word):
        self.payload_32.append(word & 0xffffffff)

    def get_payload_8(self):
        paylaod_8 = list()
        paylaod_8.append(self.op_code & 0xff)
        payload_8.append(self.payload_length & 0xff)
        payload_8.append((self.payload_length >> 8) & 0xff)
        paylaod_8.append((self.payload_length >> 16) & 0xff)
        for word in self.payload_32:
            paylaod_8.append(word & 0xff)
            paylaod_8.append((word >> 8) & 0xff)
            paylaod_8.append((word >> 16) & 0xff)
            paylaod_8.append((word >> 24) & 0xff)
        return paylaod_8

