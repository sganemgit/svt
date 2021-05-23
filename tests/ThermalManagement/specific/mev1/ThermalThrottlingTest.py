
# @author Sivan Yehuda <sivan.yehuda@intel.com>

TEST = True

from tests.ThermalManagement.specific.mev1.ThermalManagementBase import ThermalManagementBase
from core.exceptions.Exceptions import *
from core.utilities.Timer import Timer

class ThermalThrottlingTest(ThermalManagementBase):
    
    def assert_acc_clk_reduction(self, device):
        acc_clk_cfg = device.get_acc_ss_cpu_clk_status()
        vco = acc_clk_cfg["pll_vco"]
        reduced_clk = int(vco/4)
        clk_ok = True
        #checking cores 0,1,2,3
        if acc_clk_cfg["cores_0_1_2_3"] != reduced_clk:
            self.log.debug("cores 0 1 2 3 = {} clk not reduced".format(acc_clk_cfg['cores_0_1_2_3']))
            clk_ok = False
        #checking cores 6,7,8,9
        if acc_clk_cfg["cores_6_7_8_9"] != reduced_clk:
            self.log.debug("cores 6 7 8 9 = {} clk not reduced".format(acc_clk_cfg['cores_6_7_8_9']))
            clk_ok = False
        #checking cores 10,11,12,13
        if acc_clk_cfg["cores_10_11_12_13"] != reduced_clk:
            self.log.debug("cores 10 11 12 13 = {} clk not reduced".format(acc_clk_cfg['cores_10_11_12_13']))
            clk_ok = False
        #checking cores 3,4,14,15
        if acc_clk_cfg["cores_3_4_14_15"] != reduced_clk:
            self.log.debug("cores 3 4 14 15 = {} clk not reduced".format(acc_clk_cfg['cores_3_4_14_15']))
            clk_ok = False
        return clk_ok
    
    def assert_acc_clk_boost(self, device):
        acc_clk_cfg = device.get_acc_ss_cpu_clk_status()
        vco = acc_clk_cfg["pll_vco"]
        boosted_clk = int(vco/2)
        clk_ok = True
        #checking cores 0,1,2,3
        if acc_clk_cfg["cores_0_1_2_3"] != boosted_clk:
            self.log.debug("cores 0 1 2 3 = {} clk not boosted".format(acc_clk_cfg['cores_0_1_2_3']))
            clk_ok = False
        #checking cores 6,7,8,9
        if acc_clk_cfg["cores_6_7_8_9"] != boosted_clk:
            self.log.debug("cores 6 7 8 9 = {} clk not boosted".format(acc_clk_cfg['cores_6_7_8_9']))
            clk_ok = False
        #checking cores 10,11,12,13
        if acc_clk_cfg["cores_10_11_12_13"] != boosted_clk:
            self.log.debug("cores 10 11 12 13 = {} clk not boosted".format(acc_clk_cfg['cores_10_11_12_13']))
            clk_ok = False
        #checking cores 3,4,14,15
        if acc_clk_cfg["cores_3_4_14_15"] != boosted_clk:
            self.log.debug("cores 3 4 14 15 = {} clk not boosted".format(acc_clk_cfg['cores_3_4_14_15']))
            clk_ok = False
        return clk_ok

    def execute_iteration(self):
        self.log.info("-" * 80)
        self.log.info("Iteration {}".format(self.test_iteration), 'g')
        #testing for clk reduction above threshold
        temp = self.dut.get_nichot_threshold(hysteresis_direction="up") + 1
        self.log.info("Setting temperature to {}".format(temp))
        self.set_temperature(self.dut, temp)
        timer = Timer(10)
        timer.start()
        while True:
            if timer.expired():
                self.append_iteration_fail_reason("10 sec timer expired. Nichot signal not asserted")
                break
            if self.assert_acc_clk_reduction(self.dut):
                self.log.info("acc clk is redued", 'g')
                break
                
        #testing for clk boost below hysteresis value
        temp = self.dut.get_nichot_threshold(hysteresis_direction="down") - 1
        self.log.info("Setting temperature to {}".format(temp))
        self.set_temperature(self.dut, temp)
        timer.reset()
        timer.start()
        while True:
            if timer.expired():
                self.append_iteration_fail_reason("10 sec timer expired. acc clk is not boosted ")
                break
            if self.assert_acc_clk_boost(self.dut):
                self.log.info("acc clk is boosted", 'g')
                break

    def run(self):
        self.log.info("Thermal Throttling Test")
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

