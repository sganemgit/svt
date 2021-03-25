
from core.drivers.ftdidriver.FtdiDriver import FtdiDriver
from core.structs.FpgaPacket import FpgaPacket
import time

class mevFpga:

    def __init__(self, ftdi_index):
        self._ftdi_driver = FtdiDriver(ftdi_index)
        self._ftdi_driver.configure_for_sv_fpga()
        self.offset_fpga = 0
    
    def write_register(self, address, value):
        pass

    def read_register(self, address):
        packet = FpgaPacket()
        packet.op_code = 0x1
        packet.body_size = 8
        packet.offset_fpga = self.offset_fpga
        packet.start_address = address
        packet.address_inc = 1 
        packet.num_of_dwords = 1 
        self._ftdi_driver.ft_write(packet.packet_bytearry)
        print(bytes(packet.packet_bytearry))
        try:
            for _ in range(100):
                queue_stat = self._ftdi_driver.ft_get_queue_status()
                print(f"queue = {queue_stat}")
                if queue_stat > 0:
                    print(f"queue = {queue_stat}")
                    return self._ftdi_driver.ft_read(queue_stat)
                time.sleep(0.05)
        except Exception as e:
            return None

if __name__=="__main__":
    fpga = mevFpga(1)
    print(fpga.read_register(0x10))




        
        


        

