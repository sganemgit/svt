
# @author Shady Ganem <shady.ganem@intel.com>

TEST = True

from tests.ThermalManagement.specific.mev1.ThermalManagementBase import ThermalManagementBase
from core.exceptions.Exceptions import *
from core.utilities.Timer import Timer

class NichotTest(ThermalManagementBase):

    def assert_nichot_assertion(self, device):
        status = device.get_nichot_status()
        if status == 0 :
            return True
        else:
            return False

    def assert_nichot_deassertion(self, device):
        status = device.get_nichot_status()
        if status != 0:
            return True
        else:
            return False 

    def execute_iteration(self):
        self.log.info("-" * 80)
        self.log.info("Iteration {}".format(self.test_iteration), 'g')
        
        #testing for nichot assertion above threshold
        temp = self.dut.get_nichot_threshold(hysteresis_direction="up") + 1
        self.log.info("setting temperature to {}".format(temp))
        self.set_temperature(self.dut, temp)
        timer = Timer(10)
        timer.start()
        while True:
            if timer.expired():
                self.append_iteration_fail_reason("10 sec timer expired. Nichot signal not asserted")
                break
            if self.assert_nichot_assertion(self.dut):
                self.log.info("NICHOT siganl is asserted", 'g')
                break
                
        #testing for deassertion below hysteresis value
        temp = self.dut.get_nichot_threshold(hysteresis_direction="down") - 1
        self.set_temperature(self.dut, temp)
        timer.reset()
        timer.start()
        while True:
            if timer.expired():
                self.append_iteration_fail_reason("{} sec timer expired. Nichot signal not asserted")
                break
            if self.assert_nichot_deassertion(self.dut):
                self.log.info("NICHOT siganl is asserted", 'g')
                break

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
