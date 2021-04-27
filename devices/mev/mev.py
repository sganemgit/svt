from devices.mev.mevBase import mevBase

class mev(mevBase):

    def info(self):
        print ("mev1")

    def get_voltage(self, rail_name="all"):
        if self.fpga is not None:
            if rail_name is "all":
                return self.fpga.read_all_voltages()
                print("hello")
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

    def get_itd_lut(self):
        return self.data.mev_default_itd_lut
