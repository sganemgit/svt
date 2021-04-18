
# @author Shady Ganem <shady.ganem@intel.com>

TEST = True

from tests.ThermalManagement.generic.ThermalManagementBase import ThermalManagementBase

class TemperatureSweepTest(ThermalManagementBase):

    def run(self):
        self.log.info("Temperature Sweep Test")
