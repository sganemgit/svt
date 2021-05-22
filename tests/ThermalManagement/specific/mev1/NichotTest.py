
# @author Shady Ganem <shady.ganem@intel.com>

TEST = True

from tests.ThermalManagement.specific.mev.ThermalManagementBase import ThermalManagementBase
from core.exceptions.Exceptions import *
from core.utilites.Timer import Timer

class NichotTest(ThermalManagementBase):

    def assert_nichot_assertion(self, device):
        """
            This function return True if nichot siganl is asserted
        """
        status = device.get_nichot_status()
        if status != 0 :
            self.log.info("NICHOT is asserted", 'g')
            return True
        else:
            self.log.error("NICHOT is not asserted")
            return False

    def assert_nichot_deassertion(self, device):
        """
            This function returns True if nichot interrupt is deasserted
        """
        status = device.get_nichot_status()
        if status == 0:
            self.log.info("NICHOT is deasserted", 'g')
            return True
        else:
            self.log.error("NICHOT is asserted")
            return True

    def execute_iteration(self):
        self.log.info("-" * 80)
        self.log.info("Iteration {}".format(self.test_iteration), 'g')
        temp = self.dut.get_nichot_threshold(hysteresis_direction="up")
        self.log.info("setting temperature to {}".foramt(temp))
        self.set_temperature(self.dut, temp)
        timer = Timer(10)
        while 
        if not self.assert_nichot_assertion(self.dut):
            self.append_iteration_fail_reason("NICHOT is not asserted")
        self.set_temperature(self.dut, self.dut.get_nichot_threshold(hysteresis_direction="down"))
        if not self.assert_nichot_deassertion(self.dut):
            self.append_iteration_fail_reason("NICHOT is asserted")

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
