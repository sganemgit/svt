
class FpgaPacket:

    def __init__(self):
        self.op_code = 0
        self.body_size = 0
        self.offset_fpga = 0
        self.start_address = 0
        self.address_inc = 0
        self.num_of_dwords = 0

    @property
    def packet_bytearry(self):
        array = bytearray(12)
        array[0] = self.op_code
        body_size_bytes = self.body_size.to_bytes(3, 'big')
        array[1] = body_size_bytes[0]
        array[2] = body_size_bytes[1]
        array[3] = body_size_bytes[2]
        array[4] = self.offset_fpga
        start_adress_bytes = self.start_address.to_bytes(4, 'big')
        array[5] = start_adress_bytes[0]
        array[6] = start_adress_bytes[1]
        array[7] = start_adress_bytes[2]
        array[8] = start_adress_bytes[3]
        array[9] = self.address_inc
        num_of_words_byte_arr =  self.num_of_dwords.to_bytes(2, 'big')
        array[10] = num_of_words_byte_arr[0]
        array[11] = num_of_words_byte_arr[1]
        return bytes(array)

