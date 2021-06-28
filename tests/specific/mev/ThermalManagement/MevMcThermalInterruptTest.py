
# @author Shady Ganem <shady.ganem@intel.com>

TEST = True

from tests.specific.mev.ThermalManagement.ThermalManagementBase import ThermalManagementBase

class MevMcThermalInterruptTest(ThermalManagementBase):
    
    def execute_iteration(self):
        pass

    def run(self):
        self.log.info("MC Thermal Interrupt Test - Test currently not available")
