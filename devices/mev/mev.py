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

    def get_thermal_diode_temperature(self):
        if self.fpga is not None:
            return self.fpga.read_thermal_diode()
        else:
            return None

