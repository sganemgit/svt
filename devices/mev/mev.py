from devices.mev.mevBase import mevBase

class mev(mevBase):

    def info(self):
        print ("mev1")

    def get_rail_voltage(self, rail_name):
        if self.fpga is not None:
            return self.fpga.read_voltage_by_rail_name(rail_name)
        else: 
            return None
