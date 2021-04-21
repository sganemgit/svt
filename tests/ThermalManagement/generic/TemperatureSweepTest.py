
# @author Shady Ganem <shady.ganem@intel.com>

TEST = True

from tests.ThermalManagement.generic.ThermalManagementBase import ThermalManagementBase
from core.exceptions.Exceptions import *

class TemperatureSweepTest(ThermalManagementBase):
    
    def prepare_test(self):
        try:
            self.init_test_data()
            self.prepare_instruments()
            self.prepare_devices()
            return True
        except Exception as e:
            self.append_fail_reason(str(e))
            return False

    def execute_iteration(self):
        print(self.devices)
        print(self.dut.get_rail_names_list())

    def run(self):
        self.log.info("Temperature Sweep Test")
        self.log_input_args()
        
        if self.prepare_test():
            for self.test_iteration in range(self.num_of_iterations):
                try:
                    self.execute_iteration()
                except FatalTestError as e:
                    self.append_fail_reason("Fatal Test Error: " + str(e))
                    break
                except Exception as e:
                    self.append_fail_reason(str(e))
                finally:
                    self.summarize_iteration()
