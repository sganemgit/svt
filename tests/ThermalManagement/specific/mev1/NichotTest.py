
# @author Shady Ganem <shady.ganem@intel.com>

TEST = True

from tests.ThermalManagement.specific.mev1.ThermalManagementBase import ThermalManagementBase
from core.exceptions.Exceptions import *
from core.utilities.Timer import Timer
import time 

class NichotTest(ThermalManagementBase):

    def assert_nichot_assertion(self, device):
        status = device.get_nichot_status()
        self.table["NICHOT_B"] = status
        return True if status == 0 else False

    def assert_nichot_deassertion(self, device):
        status = device.get_nichot_status()
        self.table["NICHOT_B"] = status
        return True if status != 0 else False

    def execute_iteration(self):
        self.log.info("-" * 80)
        self.table["test iteration"] = self.test_iteration
        self.log.info("Iteration {}".format(self.test_iteration), 'g')
        self.log.info("PVT OTP efuses")
        self.log_pvt_fuses(self.dut)
        #testing for NICHOT siganl assertion above threshold
        if self.last_interrupt_temp is not None:
            nichot_temp = int(self.last_interrupt_temp) - 3
        else: 
            nichot_temp = self.dut.get_nichot_threshold(hysteresis_direction="up") + 1
            
        self.log.info("preheating SoC")
        self.set_t_case(nichot_temp - 20)
        self.table["NICHOT Threshold"] = nichot_temp
        self.log.info("Setting temperature to {}".format(nichot_temp))
        self.set_temperature(self.dut, nichot_temp)
        max_temp = 125 
           
        nichot_flag = False
        # sweeping through nichot temp and max temp of 130 
        for current_temp in range(nichot_temp, max_temp):
            self.log.info("setting Temperature to {}".format(current_temp))
            self.set_temperature(self.dut, current_temp)
            self.table["T case [C]"] = self.get_t_case()
            self.log.info("T case = {}C".format(self.get_t_case()))
            self.table["T diode [C]"] = self.get_t_diode(self.dut)
            self.log.info("T Diode = {}C".format(self.get_t_diode(self.dut)))
            
            if self.assert_nichot_assertion(self.dut):
                self.last_interrupt_temp = self.get_t_case() 
                nichot_flag = True
                self.log.info("NICHOT signal asserted", 'g')
                self.table.end_row()
                break
            self.table.end_row()
            self.log.line()
        if not nichot_flag:
            self.append_iteration_fail_reason("NICHOT signal was not asserted within temperature range of {}C-{}C".format(nichot_temp, max_temp))
                
        nichot_temp = self.dut.get_nichot_threshold(hysteresis_direction="down") - 1
        self.table["NICHOT Threshold hysteresis down"] = nichot_temp
        self.log.info("Setting temperature to {}".format(nichot_temp))
        self.set_temperature(self.dut, nichot_temp)
        timer = Timer(self.int_timeout)
        timer.start()
        while True:
            if timer.expired():
                self.log.error("10 sec timer expired. Nichot siganl not de-asserted")
                self.append_iteration_fail_reason("{} sec timer expired. Nichot signal not asserted")
                break
            if self.assert_nichot_deassertion(self.dut):
                self.log.info("NICHOT siganl is de-asserted", 'g')
                break
            self.table.end_row()
            self.log.line()

    def run(self):
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
