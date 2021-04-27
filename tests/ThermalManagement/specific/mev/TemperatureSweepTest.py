
# @author Shady Ganem <shady.ganem@intel.com>

TEST = True

from tests.ThermalManagement.specific.mev.ThermalManagementBase import ThermalManagementBase
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
        self.log.info(self.get_t_diode(self.dut))
        itd_lut = self.dut.get_itd_lut()
        self.log.info("Iterating over ITD Lookup Talbe of Temperatures")
        for temp, vnn_delta, vcc_delta in zip(itd_lut["max_temp"], itd_lut["vnn_delta"], itd_lut["vcc_delta"]):
            self.log.info("setting silicon temperature to {}".format(temp))
            self.set_temperature(self.dut, temp)
            self.assert_vnn(self.dut, vnn_delta)
            self.assert_vcc(self.dut, vcc_delta)

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
