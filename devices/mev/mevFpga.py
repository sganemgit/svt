
# @author Shady Ganem <shady.ganem@intel.com)

from core.drivers.ftdidriver.FtdiDriver import FtdiDriver
from core.structs.FpgaPacket import FpgaReadPacket 
from core.structs.FpgaPacket import FpgaWritePacket 
import time, math

class mevFpga:

    def __init__(self, ftdi_index):
        self._ftdi_driver = FtdiDriver(ftdi_index)
        self.offset_fpga = 0
        self.write_register(0x0, 0)

    def _to_int(self, ls):
        ret_list = list()
        for word in range(int(len(ls)/4)):
            offset = word*4
            ret_list.append(ls[offset+3] << 24 | ls[offset+2] << 16 | ls[offset + 1] | ls[offset])
        return ret_list 
    
    def write_register(self, address, value):
        """
            return True if request was acknoleged
            note: sometimes the fpga will write the register but will not return an ack
        """
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

    def read_I2C(self, devadd, address, num_of_bytes=1):
        self.write_register(0x5001, address & 0xffff)
        address_length = 1 if address == 0 else (int(math.log(address, 256))+1)
        ctrl_reg = (devadd & 0xffff) << 16 | address_length << 12 | (num_of_bytes & 0xf) << 8 | 0x1
        self.write_register(0x5000, ctrl_reg)
        status = self.read_register(0x5001)[0]
        if status & 0x4:
            if num_of_bytes = 1:
                return self.read_register(0x5003)[0] & 0xff
            elif num_of_bytes < 4:
                return list(self.read_register(0x5003)[0].to_type(num_of_bytes, 'big'))
            elif num_of_bytes < 8:
                ret_vals = list(self.read_register(0x5003)[0].to_bytes(4, 'big'))
                ret_vals.extend(self.read_register(0x5005)[0].to_bytes(num_of_bytes-4, 'big')
                return ret_vals
        else:
            return False

    def write_I2C(self, devadd, address, value, num_of_bytes=1):
        self.write_register(0x5001, address & 0xffff)
        self.write_register(0x5002, value)
        address_length = 1 if address == 0 else (int(math.log(address, 256))+1)
        ctrl_reg = (devadd & 0xffff) << 16 | address_length << 12 | (num_of_bytes & 0xf) << 8 | 0x1
        self.write_register(0x5000, ctrl_reg)
        status = self.read_register(0x5001)[0]
        if status & 0x4:
            return True
        else:
            return False

    def pwr_get_rail_status(self):
        pm_status = self.read_register(0x102)[0]
        ret_dict = dict()
        ret_dict["prf_rails_ok"] = pm_status & 0x1
        ret_dict["dut_rails_ok"] = pm_status & 0x2
        ret_dict["prf_rails_err"] = pm_status & 0x4
        ret_dict["dut_rails_err"] = pm_status & 0x8
        ret_dict["prf_rails_down"] = pm_status & 0x10
        ret_dict["dut_rails_down"] = True if pm_status & 0x20 else False
        return ret_dict
    
    def get_nichot_status(self):
        GPIO = self.read_register(0x226)[0]
        if GPIO:
            return True if GPIO & 0x10 else False
        else:
            return None

    def set_gpio_value(self, gpio, value):
        gpio_status = self.read_register(0x226)[0]
        mask = 1 << gpio    
        if gpio_status is not None:
            gslkdjf;alksdjfpio_new_val = gpio_status & mask
            self.write_register(0x224, gpio_new_val)

if __name__=="__main__":
    fpga = mevFpga(1)
    #print(fpga.get_nichot_status())
    


    for i in range(50):
        fpga.write_register(0x5001, i)
        if i == fpga.read_register(0x5001)[0]:
            print("pass")
        
