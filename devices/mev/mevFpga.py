
# @author Shady Ganem <shady.ganem@intel.com)

from core.drivers.ftdidriver.FtdiDriver import FtdiDriver
from core.structs.FpgaPacket import FpgaReadPacket 
from core.structs.FpgaPacket import FpgaWritePacket 
import time

class mevFpga:

    def __init__(self, ftdi_index):
        self._ftdi_driver = FtdiDriver(ftdi_index)
        self.offset_fpga = 0

    def _to_int(self, ls):
        ret_list = list()
        for word in range(int(len(ls)/4)):
            offset = word*4
            ret_list.append(ls[offset+3] << 24 | ls[offset+2] << 16 | ls[offset + 1] | ls[offset])
        return ret_list 
    
    def write_register(self, address, value):
        queue_stat = self._ftdi_driver.ft_get_queue_status()
        if queue_stat:
            self._ftdi_driver.ft_read(queue_stat)
        packet = FpgaWritePacket()
        packet.offset_fpga = self.offset_fpga
        packet.start_address = address
        packet.address_inc = 1 
        if isinstance(value, int):
            packet.data = [value]
        elif isinstance(value, list):
            packet.data = value
        self._ftdi_driver.ft_write(packet.packet_bytes)
        time.sleep(len(packet.data) * 0.05)
        try:
            for _ in range(10):
                queue_stat = self._ftdi_driver.ft_get_queue_status()
                if queue_stat == 2: 
                    ack = self._ftdi_driver.ft_read(queue_stat)
                    if ack[0] == 170:
                        return True
                time.sleep(0.05)
            return False 
        except Exception as e:
            return False 

    def read_register(self, address, num_of_words=0x1):
        queue_stat = self._ftdi_driver.ft_get_queue_status()
        if queue_stat:
            self._ftdi_driver.ft_read(queue_stat)
        packet = FpgaReadPacket()
        packet.offset_fpga = self.offset_fpga
        packet.start_address = address
        packet.address_inc = 0 
        packet.num_of_dwords = num_of_words 
        self._ftdi_driver.ft_write(packet.packet_bytes)
        try:
            for _ in range(100):
                queue_stat = self._ftdi_driver.ft_get_queue_status()
                if queue_stat == 4*num_of_words + 2: 
                    return self._to_int(self._ftdi_driver.ft_read(queue_stat)[:-2])
                time.sleep(0.05)
            return None
        except Exception as e:
            return None

    def read_I2C(self, devadd, page, address):
        pass

    def write_I2C(self, devadd, page, address, value):
        pass



if __name__=="__main__":
    fpga = mevFpga(1)
    for i in range(100):
        fpga.write_register(0x5001, i)
        print(fpga.read_register(0x5001))




        
        


        

