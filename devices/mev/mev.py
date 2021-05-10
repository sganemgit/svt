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

    def get_thermtrip_threshold(self):
        return self.data.mev_default_thermtrip_b_threshold

    def get_nichot_threshold(self, hysteresis_direction="up"):
        if hysteresis_direction == "up":
            return self.data.mev_default_nichot_b_threshold
        elif hysteresis_direction == "down":
            return self.data.mev_default_nichot_b_thershold_hysteresis

    def get_thermtrip_thershold(self, hysteresis_dircetion="up"):
        if hysteresis_dircetion == "up":
            return self.data.mev_default_thermtrip_b_threshold
        elif hysteresis_dircetion == "down":
            return self.data.mev_default_thermtrip_b_threshold_hysteresis
    
    def get_acc_ss_clock_status(self):
        if self.driver is not None:
            pass

        
