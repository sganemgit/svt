
TEST = True

from tests.ThermalManagement.specific.mev.ThermalManagementBase import ThermalManagementBase
from core.exceptions.Exceptions import *

class ThermtripTest(ThermalManagementBase):

    def assert_thermtrip_assertion(self, device):
        """
            This function return True if thermtrip siganl is asserted
        """
        status = device.get_nichot_status()
        if status == 0 :
            return True
        else:
            return False

    def assert_thermtrip_deassertion(self, device):
        """
            This function returns True if thermtrip interrupt is deasserted
        """
        status = device.get_thermtrip_status()
        if status != 0:
            return True
        else:
            return False 

    def execute_iteration(self):
        self.log.info("-" * 80)
        self.log.info("Iteration {}".format(self.test_iteration), 'g')
        self.log.info("Setting silicon temperature to NICHOT Threshold")
        self.set_temperature(self.dut, self.dut.get_thermtrip_thershold())
        
        if not self.assert_thermtrip_assertion(self.dut):
            self.append_iteration_fail_reason("NICHOT is not asserted")


    def run(self):
        self.log.info("NICHOT Test")
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
                    self.reset_temperature()
                    self.summarize_iteration()
        else:
            self.log.error("Failed to prepare test")
            self.append_fail_reason("Failed to prepare test")
