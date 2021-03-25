
from core.drivers.ftdidriver.FtdiDriver import FtdiDriver
from core.structs.FpgaPacket import FpgaPacket
import time

class mevFpga:

    def __init__(self, ftdi_index):
        self._ftdi_driver = FtdiDriver(ftdi_index)
        #self._ftdi_driver.configure_for_sv_fpga()
        self.offset_fpga = 0

    def _to_int(self, ls):
        return ls[3] << 24 | ls[2] << 16 | ls[1] << 8 | ls[0]
    
    def write_register(self, address, value):
        pass

    def read_register(self, address):
        packet = FpgaPacket()
        packet.op_code = 0x1
        packet.body_size = 8
        packet.offset_fpga = self.offset_fpga
        packet.start_address = address
        packet.address_inc = 1 
        packet.num_of_dwords = 0x1 
        self._ftdi_driver.ft_write(packet.packet_bytearry)
        try:
            for _ in range(100):
                queue_stat = self._ftdi_driver.ft_get_queue_status()
                if queue_stat == 6: 
                    return self._to_int(self._ftdi_driver.ft_read(queue_stat)[:4])
                time.sleep(0.05)
            return None
        except Exception as e:
            return None

if __name__=="__main__":
    fpga = mevFpga(1)
    print(fpga.read_register(0x40))




        
        


        

