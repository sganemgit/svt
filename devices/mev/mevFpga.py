
from core.drivers.ftdidriver.FtdiDriver import FtdiDriver
from core.structs.FpgaPacket import FpgaPacket
import time

class mevFpga:

    def __init__(self, ftdi_index):
        self._ftdi_driver = FtdiDriver(ftdi_index)
        self._ftdi_driver.configure_sv_fpga()
        self.offset_fpga = 0
    
    def read_register(self, address):
        packet = FpgaPacket()
        packet.op_code = 0x1
        packet.body_size_higher_byte = 0
        packet.body_size_med_byte = 0
        packet.body_size_lower_byte = 8
        packet.offset_fpga = self.offset_fpga
        packet.start_address = address
        packet.address_inc = 1 
        packet.num_of_dwords = 1 
        self._ftdi_driver.ft_write(packet.packet_bytearry)

        for poll in range(50):
            if self._ftdi_driver.ft_get_queue_status() == 6:
                break
            time.sleep(0x005)

        return self._ftdi_driver.ft_read(6)


if __name__=="__main__":
    fpga = mevFpga(1)
    print(fpga.read_register(0x10))




        
        


        

