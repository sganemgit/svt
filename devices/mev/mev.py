from devices.mev.mevBase import mevBase

class mev(mevBase):

    def info(self):
        print ("mev1")

    def scan_ftdi_devices(self):
        pass

    def get_voltage(self, rail_name="all"):
        if self.fpga is not None:
            if rail_name is "all":
                return self.fpga.read_all_voltages()
            else:
                return self.fpga.read_voltage_by_rail_name(rail_name)
        else: 
            return None

    def get_diode_temperature(self):
        if self.fpga is not None:
            return self.fpga.read_thermal_diode()
        else:
            return None

    def get_rail_names_list(self):
        if self.fpga is not None:
            return self.fpga.get_rail_name_list()
        else:
            return None

    def get_itd_lut(self, mode="SM"):
        '''
            This method return the itd lookup Table
            mode = SM/PM standard mode/performance mode
        '''
        #TODO this method must retreive the LUT from file /etc/hwconf/active/pvt from the imc filesystem
        return self.data.mev_default_itd_lut

    def get_nichot_status(self):
        if self.fpga is not None:
            return self.fpga.get_nichot_status()
        else:
            return None

    def get_thermtrip_status(self):
        if self.fpga is not None:
            return self.fpga.get_thermtrip_status()
        else:
            return None