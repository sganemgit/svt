
# @author Shady Ganem <shady.ganem@intel.com)

from core.drivers.ftdidriver.FtdiDriver import FtdiDriver
from core.structs.FpgaPacket import FpgaReadPacket 
from core.structs.FpgaPacket import FpgaWritePacket 
import time, math
import json

class mevFpga:

    def __init__(self, ftdi_index):
        self.config_filename = "data/mev_svb_config.json"
        self.svb_config = self.get_board_config()
        self.vout_cmd = 0x21
        self.page_cmd = 0
        self._ftdi_driver = FtdiDriver(ftdi_index)
        self.offset_fpga = 0
        self.write_register(0x0, 0)
        self.ticks = 1 
        self.read_register(0x10)
        self.ticks = 5 
    
    def get_board_config(self):
        with open(self.config_filename, 'r') as f:
            data = json.load(f)
        return data

    def get_rails_info(self):
        return self.svb_config["Rails"]

    @property
    def rails_info(self):
        return self.svb_config['Rails']

    def print_rails_info(self):
        for rail in self.rails_info:
            for key, val in rail.items():
                print(f"{key} : {val}")
            print("-"*80)

    def print_pmbus_rails_info(self):
        for rail in self.rails_info:
            if rail['PowerType'] == "pmbus":
                for key, val in rail.items():
                    print(f"{key} : {val}")
            print("-"*80)
         

    def _to_int(self, ls):
        ret_list = list()
        for word in range(int(len(ls)/4)):
            offset = word*4
            ret_list.append(ls[offset+3] << 24 | ls[offset+2] << 16 | ls[offset + 1] << 8 | ls[offset])
        return ret_list 
    
    def _clean_queue(self):
        queue_stat = self._ftdi_driver.ft_get_queue_status()
        if queue_stat:
            self._ftdi_driver.ft_read(queue_stat)
    
    def write_register(self, address, value):
        """
            return True if request was acknoleged
            note: sometimes the fpga will write the register but will not return an ack
        """
        self._clean_queue()
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
            for _ in range(self.ticks):
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
        self._clean_queue()
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
                    data = self._ftdi_driver.ft_read(queue_stat)
                    return  self._to_int(data[:-2])
                time.sleep(0.05)
            return None
        except Exception as e:
            return None

    def read_i2c(self, devadd, address, num_of_bytes=1, pre_wr_data=None):
        if pre_wr_data is None:
            pre_wr_data = 1 if address == 0 else (int(math.log(address, 256))+1)
        ctrl_reg = (devadd & 0xffff) << 16 | pre_wr_data << 12 | (num_of_bytes & 0xf) << 8 | 0x2
        self.write_register(0x5001, address & 0xffff)
        self.write_register(0x5000, ctrl_reg)
        time.sleep(0.01)
        status = self.read_register(0x5001)[0]
        #TODO according to the FPGA user guid the status LSB i.e. 0b0100 = Done and 0b1000 = Error. This is not the behaivor of the FPGA
        status = 0x4
        if status & 0x4:
            if num_of_bytes == 1:
                return [self.read_register(0x5003)[0] & 0xff]
            elif num_of_bytes < 4:
                data = self.read_register(0x5003)
                return list(data[0].to_bytes(num_of_bytes, 'big') )
            elif num_of_bytes < 8:
                ret_vals = list(self.read_register(0x5003)[0].to_bytes(4, 'big'))
                ret_vals.extend(self.read_register(0x5005)[0].to_bytes(num_of_bytes-4, 'big'))
                return ret_vals
        else:
            return False

    def write_i2c(self, devadd, address, data, num_of_bytes=1, pre_wr_data=None):
        if pre_wr_data is None:
            pre_wr_data = 1 if address == 0 else (int(math.log(address, 256))+1)
        ctrl_reg = (devadd & 0xffff) << 16 | pre_wr_data << 12 | (num_of_bytes & 0xf) << 8 | 0x1
        self.write_register(0x5001, address & 0xffff)

        if num_of_bytes > 4:
            value_0 = data[0]
            value_1 = data[1]
            self.write_register(0x5004, value_1)
        else:
            value_0 = data
        self.write_register(0x5002, value_0)
        self.write_register(0x5000, ctrl_reg)
        time.sleep(0.01)
        status = self.read_register(0x5001)[0]
        if status & 0x4:
            return True
        else:
            return False

    def _enable_pmbus_mux(self):
        self.write_register(0x300, 0) # enable mux
        self.write_register(0x301, 1) # fpga_i2c to pmbus

    def _disable_pmbus_mux(self):
        self.write_register(0x300, 1) # disable mux 
        self.write_register(0x301, 0) # fpga_i2c to pmbus
        
    def get_pmbus_voltage(self, rail_number):
        for rail in self.rails_info:
            if int(rail['RailNumber']) == rail_number and rail['PowerType'] == 'pmbus':
                target_rail = rail

        if "target_rail" in locals():
            self._enable_pmbus_mux()
            self.write_i2c(int(target_rail['PmbusAddress'], 16), self.page_cmd, int(target_rail['RailPageNumber'], 16), 1) 
            data = self.read_i2c(int(target_rail['PmbusAddress'], 16), self.vout_cmd, 2 )
            data_int = data[0] << 8 | data[1]
            voltage_value = float(data_int) * float(target_rail['VoltageReadResolution'])
            self._disable_pmbus_mux()
            return voltage_value
        else:
            return None
    
    @staticmethod
    def _convert_twos_complement(num, count_bits):
        bin_str = '{0:b}'.format(num).zfill(count_bits)
        if bin_str[0] == '0':
            return int(bin_str, 2)
        converted_str = ''.join('1' if x == '0' else '0' for x in bin_str)
        return -int(converted_str, 2)

    def get_pmbus_current(self, rail_number):
        for rail in self.rails_info:
            if int(rail['RailNumber']) == rail_number and rail['PowerType'] == 'pmbus':
                target_rail = rail

        if "target_rail" in locals():
            self._enable_pmbus_mux()
            self.write_i2c(int(target_rail['PmbusAddress'], 16), self.page_cmd, int(target_rail['RailPageNumber'], 16), 1) 
            data = self.read_i2c(int(target_rail['PmbusAddress'], 16), int(target_rail['ReadIOUTAddress'], 16), 2)
            data_int = data[0] << 8 | data[1]
            converted_data = self.__class__._convert_twos_complement(data_int & 0x3ff, 10)
            voltage_value = float(converted_data) * float(target_rail['IReadFactor'])
            self._disable_pmbus_mux()
            return voltage_value
        else:
            return None

    def set_pmbus_voltage(self,rail_number, voltage_val):
        for rail in self.rails_info:
            if int(rail['RailNumber']) == rail_number and rail['PowerType'] == 'pmbus':
                target_rail = rail

        if "target_rail" in locals():
            self._enable_pmbus_mux()
            self.write_i2c(int(target_rail['PmbusAddress'], 16), self.page_cmd, int(target_rail['RailPageNumber'], 16), 1) 
            voltage = round(voltage_val/float(target_rail['VoltageReadResolution']))
            self.write_i2c(int(target_rail['PmbusAddress'], 16), self.vout_cmd, volatge, 2, 1)
            self._disable_pmbus_mux()
            return voltage_value
        else:
            return None

    def read_ad7998(self, dev_address, port_number, a2d_vref):
        data = self.read_i2c(dev_address, hex(port_number + 7)[2:] + "0", 2, 1)
        a2d_read = data[0] << 8 | data[1]
        return round((a2d_vref * a2d_read) / 4096, 2)
        
    def read_ads11112_a2d(self, dev_address, config_mode):
        voltage_const = 2.048
        cycle_ctr = 0
        self.write_i2c(dev_address, 0, a2d_command , 1)
        time.sleep(0.15)
        while lsb_val != 0 and cycle_ctr < 4:
            a2d_val = self.read_i2c(dev_address, 0, 3)
        return round(voltage_const * int((a2d_val[-2:] + a2d_val[-4:-2]), 16) / 32768, 3)

    def read_ad5272(self, dev_address):
        # the AD5272 requier the I2C high byte to come first, not like we send it
        # enable to program the resistor.
        rdata = 0x0800  # program the RDAC fuse to current resistor value.
        rdata_s = swapbytehex(rdata)
        # print(rdata_s)
        rdata_s = str(swapbytehex(int(self.read_i2c_dev(ftdi, dev_address, rdata_s, 2, 2), 16)))
        # print(rdata_s)
        return rdata_s
    
    def print_all_rails_voltage(self):
        rail_list = self.svb_config["Rails"]
        for rail in rail_list:
            pass
    
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
    
    def check_power_good(self, power_good_bit):
        pass
        
        
if __name__=="__main__":
    fpga = mevFpga(1)
    #fpga.print_rails_info()
    fpga.print_pmbus_rails_info()
    for rail in fpga.rails_info:
        if rail["PowerType"] == "pmbus":
            name = rail['RailName']
            
            print(f"rail name {name}")
            print(fpga.get_pmbus_voltage(int(rail["RailNumber"])))
            print(fpga.get_pmbus_current(int(rail["RailNumber"])))
