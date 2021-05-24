
# @author Shady Ganem <shady.ganem@intel.com>

TEST = True

from tests.ThermalManagement.specific.mev1.ThermalManagementBase import ThermalManagementBase
from core.exceptions.Exceptions import *

class TemperatureSweepTest(ThermalManagementBase):
    
    def assert_vnn_itd_enabled(self, device):
        vnn_itd = device.get_pvt_vnn_itd_disable()
        if vnn_itd:
            return False
        else:
            return True

    def assert_vcc_itd_enabled(self, device):
        vcc_itd = device.get_pvt_vcc_itd_disable()
        if vcc_itd:
            return False
        else:
            return True
        
    def execute_iteration(self):
        self.log.info("-"*80)
        self.log.info("Iteration {}".format(self.test_iteration), 'g')
        check_vcc_itd = self.assert_vcc_itd_enabled(self.dut)
        if not check_vcc_itd:
            self.log.info("ITD is disabled for VCC", 'o')
        check_vnn_itd = self.assert_vnn_itd_enabled(self.dut)
        if not check_vcc_itd:
            self.log.info("ITD is disabled for VNN", 'o')
        if check_vcc_itd or check_vnn_itd:
            itd_lut = self.dut.get_itd_lut()
            self.log.info("Iterating over ITD Lookup Talbe")
            self.log.info(self.dut.get_voltage(self.dut.data.mev_vnn_rail_name))
            for temp, vnn_delta, vcc_delta in zip(itd_lut["max_temp"], itd_lut["vnn_delta"], itd_lut["vcc_delta"]):
                self.log.info("setting silicon temperature to {}".format(temp))
                self.set_temperature(self.dut, temp)
                if check_vnn_itd:
                    self.assert_vnn(self.dut, vnn_delta)
                if check_vcc_itd:
                    self.assert_vcc(self.dut, vcc_delta)
        else:
            self.append_fail_reason("ITD is disabled for VNN and VCC")
            raise FatalTestError("exiting test since ITD is disabled")

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
                    self.reset_temperature()
                    self.summarize_iteration()
        else:
            self.log.error("Failed to prepare test")
            self.append_fail_reason("Failed to prepare test")
