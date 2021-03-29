
# @author Shady Ganem <shady.ganem@intel.com)

from core.drivers.ftdidriver.FtdiDriver import FtdiDriver
from core.structs.FpgaPacket import FpgaReadPacket 
from core.structs.FpgaPacket import FpgaWritePacket 
import time, math
import json

class mevFpga:

    def __init__(self, ftdi_index):
        self.pisgah_config = self.get_board_config()
        self.voltage_read_resolution = 0.0039 
        self.pmbus_address = 0
        self.vout_cmd = 0x21
        self.page_cmd = 0
        self._ftdi_driver = FtdiDriver(ftdi_index)
        self.offset_fpga = 0
        self.write_register(0x0, 0)
        self.ticks = 1 
        self.read_register(0x10)
        self.ticks = 5 
    
    def get_board_config(self):
        self.config_filename = "data/mev_pisgah_config.json"
        with open(self.config_filename, 'r') as f:
            data = json.load(f)
        return data

    def get_rails_info(self):
        return self.pisgah_config["Rails"]

    def print_rails_info(self):
        rail_list = self.pisgah_config["Rails"]
        for rail in rail_list:
            if rail['PowerType'] == "pmbus":
                for key, val in rail.items():
                    print(f"{key} : {val}")
            print("-"*80)

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
            for _ in range(self.ticks):
                queue_stat = self._ftdi_driver.ft_get_queue_status()
                if queue_stat == 4*num_of_words + 2: 
                    return self._to_int(self._ftdi_driver.ft_read(queue_stat)[:-2])
                time.sleep(0.05)
            return None
        except Exception as e:
            return None

    def read_i2c(self, devadd, address, num_of_bytes=1):
        self.write_register(0x5001, address & 0xffff)
        address_length_in_bytes = 1 if address == 0 else (int(math.log(address, 256))+1)
        ctrl_reg = (devadd & 0xffff) << 16 | address_length_in_bytes << 12 | (num_of_bytes & 0xf) << 8 | 0x1
        self.write_register(0x5000, ctrl_reg)
        time.sleep(0.005)
        status = self.read_register(0x5001)[0]
        status = 0x4
        if status & 0x4:
            if num_of_bytes == 1:
                return [self.read_register(0x5003)[0] & 0xff]
            elif num_of_bytes < 4:
                return list(self.read_register(0x5003)[0].to_bytes(num_of_bytes, 'big'))
            elif num_of_bytes < 8:
                ret_vals = list(self.read_register(0x5003)[0].to_bytes(4, 'big'))
                ret_vals.extend(self.read_register(0x5005)[0].to_bytes(num_of_bytes-4, 'big'))
                return ret_vals
        else:
            return False

    def write_i2c(self, devadd, address, value, num_of_bytes=1):
        self.write_register(0x5001, address & 0xffff)
        self.write_register(0x5002, value)
        address_length_in_bytes = 1 if address == 0 else (int(math.log(address, 256))+1)
        ctrl_reg = (devadd & 0xffff) << 16 | address_length_in_bytes << 12 | (num_of_bytes & 0xf) << 8 | 0x1
        self.write_register(0x5000, ctrl_reg)
        time.sleep(0.1)
        status = self.read_register(0x5001)[0]

        if status & 0x4:
            return True
        else:
            return False

    def _enable_pmbus_mux(self):
        self.write_register(0x300, 0) # enable_mux
        self.write_register(0x301, 1) # fpga_i2c to pmbus

    def _disable_pmbus_mux(self):
        self.write_register(0x300, 1) # enable_mux
        self.write_register(0x301, 0) # fpga_i2c to pmbus
        
    def get_pmbus_voltage(self, rail_number):
        for rail in self.get_rails_info():
            if int(rail['RailNumber']) == rail_number and rail['PowerType'] == 'pmbus':
                target_rail = rail

        if "target_rail" in locals():
            self._enable_pmbus_mux()
            self.write_i2c(int(target_rail['PmbusAddress']), int(target_rail['RailPageNumber']), 0, 1)  # change to the right page number
            data = self.read_i2c(self.pmbus_address, self.vout_cmd, 2)
            data_int = data[0] << 8 | data[1]
            voltage_value = float(data_int) * float(target_rail['VoltageReadResolution'])
            self._disable_pmbus_mux()
            return voltage_value

    def get_pmbus_current(self):
        pass

    def set_pmbus_voltage(self, voltage_val, correction_set=True):
        pass
#        try:
#            self._ftdi.open()
#            if not self.check_power_good():
#                raise Exception(self.rail_name + "rail is off")
#
#            self._pmbus_enable_select(True)
#            self._fpga.write_i2c_dev(self._ftdi, self.pmbus_address, self._page_cmd, self.rail_page_number, 1,
#                                     1)  # change to the right page number
#            self._fpga.write_i2c_dev(self._ftdi, self.pmbus_address, self._vout_cmd,
#                                     str(format(int(round((voltage_val / self.voltage_read_resolution))), 'x')), 2, 1)
#
#            self._pmbus_enable_select(False)
#            self._ftdi.close()
#        except Exception as e:
#            raise BaseRailError(e.message)

    def read_ads11112_a2d(self, dev_address, config_mode):
        voltage_const = 2.048
        cycle_ctr = 0
        self.write_i2c(dev_address, 0, a2d_command , 1)
        time.sleep(0.15)
        while lsb_val != 0 and cycle_ctr < 4:
            a2d_val = self.read_i2c(dev_address, 0, 3)

        return round(voltage_const * int((a2d_val[-2:] + a2d_val[-4:-2]), 16) / 32768, 3)

    def read_ad5272(self, ftdi, dev_address):
        """

        :param dev_address:
        :type ftdi: FTDI
        """
        # the AD5272 requier the I2C high byte to come first, not like we send it
        # enable to program the resistor.
        rdata = 0x0800  # program the RDAC fuse to current resistor value.
        rdata_s = swapbytehex(rdata)
        # print(rdata_s)
        rdata_s = str(swapbytehex(int(self.read_i2c_dev(ftdi, dev_address, rdata_s, 2, 2), 16)))
        # print(rdata_s)
        return rdata_s
    
    def get_fpga_version(self):
        reg_val = self.read_register(0x10)
        return reg_val[0] if reg_val else reg_val
    
    def get_fpga_gp_sw(self):
        reg_val = self.read_register(0x53)
        return reg_val[0] if reg_val else reg_val

    def get_therm_led_n_status(self):
        reg_val = self.read_register(0x308)
        return reg_val[0] if reg_val else reg_val

    def get_i2c_version(self):
        val = self.read_register(0x5fff)
        return val[0] if val else val
 
    def get_gpio_status(self):
        GPIO = self.read_register(0x226)
        return GPIO[0] if GPIO else GPIO

    def get_therm_pwr_ok_dis_status(self):
        reg_val = self.read_register(0x323)
        return reg_val[0] if reg_val else reg_val

    def get_therm_alert_status(self):
        reg_val = self.read_register(0x324)
        return reg_val[0] if reg_val else reg_val
    
    def get_nichot_status(self):
        reg_val = self.read_register(0x325)
        return reg_val[0] if reg_val else reg_val

    def get_thermtrip_status(self):
        reg_val = self.read_register(0x326)
        return reg_val[0] if reg_val else reg_val

    def set_gpio_value(self, gpio, value):
        gpio_status = self.read_register(0x226)[0]
        mask = 1 << gpio    
        if gpio_status is not None:
            gpio_new_val = gpio_status & mask
            self.write_register(0x224, gpio_new_val)

    def get_eth_config_status(self):
        reg_val = self.read_register(0x326)
        if reg_val:
            if reg_val[0] == 0:
                return "single_qsfp"
            elif reg_val[0] == 1:
                return "double_qsfp"
        else:
            return reg_val

    def pwr_get_rail_status(self):
        pm_status = self.read_register(0x102)
        if pm_status:
            ret_dict = dict()
            ret_dict["prf_rails_ok"] = pm_status & 0x1
            ret_dict["dut_rails_ok"] = pm_status & 0x2
            ret_dict["prf_rails_err"] = pm_status & 0x4
            ret_dict["dut_rails_err"] = pm_status & 0x8
            ret_dict["prf_rails_down"] = pm_status & 0x10
            ret_dict["dut_rails_down"] = True if pm_status & 0x20 else False
            return ret_dict
        return pm_status
        
if __name__=="__main__":
    fpga = mevFpga(1)
    fpga.print_rails_info()
    print(fpga.get_pmbus_voltage(6))
    #print(fpga.get_nichot_status())
    #fpga.set_gpio_value(1, 0)
    #print(fpga.get_therm_pwr_ok_dis_status())
    #print(hex(fpga.get_gpio_status()))
    


    #for i in range(50):
    #    fpga.write_register(0x5001, i)
    #    if i == fpga.read_register(0x5001)[0]:
    #        print("pass")
        
