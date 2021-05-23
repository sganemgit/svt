
# @author Sivan Yehuda <sivan.yehuda@intel.com>

TEST = True

from tests.ThermalManagement.specific.mev1.ThermalManagementBase import ThermalManagementBase

class McThermalInterruptTest(ThermalManagementBase):
    
    def execute_iteration(self):
        pass

    def run(self):
        self.log.info("MC Thermal Interrupt Test - Test currently not available")
