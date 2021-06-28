
TEST = True

from tests.specific.mev.ThermalManagement.ThermalManagementBase import ThermalManagementBase
from core.exceptions.Exceptions import *
from core.utilities.Timer import Timer

class MevThermtripTest(ThermalManagementBase):

    def assert_thermtrip_assertion(self, device):
        status = device.get_nichot_status()
        if status == 0 :
            return True
        else:
            return False

    def assert_thermtrip_deassertion(self, device):
        status = device.get_thermtrip_status()
        if status != 0:
            return True
        else:
            return False 

    def execute_iteration(self):
        self.log.info("-" * 80)
        self.log.info("Iteration {}".format(self.test_iteration), 'g')
        
        self.log.info("PVT OTP efuses")
        self.log_pvt_fuses(self.dut)

        if self.dut.get_pvt_ts_cattrip_disable() == 1:
            raise FatalTestError("CATTRIP is disabled in fuse")
    
        self.log.info("Setting silicon temperature to Thermtrip Threshold")
        temp = self.dut.get_thermtrip_threshold()
        self.set_temperature(self.dut, temp)
        timer = Timer(10)
        timer.start()
        while True:
            if timer.expired():
                self.append_iteration_fail_reason("Thermtrip is not asserted")
                break
            
            if self.assert_thermtrip_assertion(self.dut):
                self.log.info("Thermtirp signal was asserted" , "g")
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
