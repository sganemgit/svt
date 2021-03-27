
# @author Shady Ganem <shady.ganem@intel.com>
# @PyVersion python3.x

class FpgaPacket:
    pass

class FpgaWritePacket(FpgaPacket):

    def __init__(self):
        self.op_code = 0x2 
        self.body_len = 0
        self.offset_fpga = 0 
        self.start_address = 0 
        self.address_inc = 0 
        self.data = list()

    @property
    def packet_bytes(self):
        self.body_len = int(6 + len(self.data)*4)
        array = bytearray(4 + self.body_len)
        array[0] = self.op_code
        body_len_bytes = self.body_len.to_bytes(3, 'big')
        array[1] = body_len_bytes[0]
        array[2] = body_len_bytes[1]
        array[3] = body_len_bytes[2]
        array[4] = self.offset_fpga
        start_adress_bytes = self.start_address.to_bytes(4, 'big')
        array[5] = start_adress_bytes[0]
        array[6] = start_adress_bytes[1]
        array[7] = start_adress_bytes[2]
        array[8] = start_adress_bytes[3]
        array[9] = self.address_inc
        for index, data_item in enumerate(self.data):
            data_item_bytes = data_item.to_bytes(4, 'big')
            array[10 + index*4] = data_item_bytes[0]
            array[10 + index*4 + 1] = data_item_bytes[1]
            array[10 + index*4 + 2] = data_item_bytes[2]
            array[10 + index*4 + 3] = data_item_bytes[3]
        return bytes(array)

class FpgaReadPacket(FpgaPacket):

    def __init__(self):
        self.op_code = 0x1 
        self.body_len = 8 
        self.offset_fpga = 0
        self.start_address = 0
        self.address_inc = 0
        self.num_of_dwords = 0

    @property
    def packet_bytes(self):
        array = bytearray(12)
        array[0] = self.op_code
        body_size_bytes = self.body_len.to_bytes(3, 'big')
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

