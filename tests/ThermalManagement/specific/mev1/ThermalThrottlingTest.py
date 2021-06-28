
# @author Shady Ganem <shady.ganem@intel.com>

TEST = True

from tests.ThermalManagement.specific.mev1.ThermalManagementBase import ThermalManagementBase
from core.exceptions.Exceptions import *
from core.utilities.Timer import Timer
import time

class ThermalThrottlingTest(ThermalManagementBase):
    
    def assert_acc_clk_reduction(self, device):
        acc_clk_cfg = device.get_acc_ss_cpu_clk_status()
        vco = acc_clk_cfg["pll_vco"]
        if not vco:
            self.log.error("invalid cpu clk pll VCO value")
            raise Exception("VCO vlaue is not valid")
        reduced_clk = int(vco/4)
        clk_ok = True
        self.table["CPU_PLL_CFG_0_inst"] = hex(acc_clk_cfg["CPU_PLL_CFG_0_inst"])
        self.table["CPU_PLL_CFG_1_inst"] = hex(acc_clk_cfg["CPU_PLL_CFG_1_inst"])
        self.table["CPU_PLL_CFG_2_inst"] = hex(acc_clk_cfg["CPU_PLL_CFG_2_inst"])

        self.table["cores_0_1_2_3"] = acc_clk_cfg["cores_0_1_2_3"]
        self.table["cores_6_7_8_9"] = acc_clk_cfg["cores_6_7_8_9"]
        self.table["cores_10_11_12_13"] = acc_clk_cfg["cores_10_11_12_13"]
        self.table["cores_4_5_14_15"] = acc_clk_cfg["cores_4_5_14_15"]

        self.log.info("ACC CLK cores 0, 1, 2, 3    : {}MHz".format(acc_clk_cfg["cores_0_1_2_3"]))
        self.log.info("ACC CLK cores 6, 7, 8, 9    : {}MHz".format(acc_clk_cfg["cores_6_7_8_9"]))
        self.log.info("ACC CLK cores 10, 11, 12, 13: {}MHz".format(acc_clk_cfg["cores_10_11_12_13"]))
        self.log.info("ACC CLK cores 4, 5, 14, 15  : {}MHz".format(acc_clk_cfg["cores_4_5_14_15"]))
        self.log.info("NICHOT signal status   : {}".format(hex(device.get_nichot_status())))
        self.log.info("THERMTRIP signal status: {}".format(hex(device.get_thermtrip_status())))

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
        #checking cores 4,5,14,15
        if acc_clk_cfg["cores_4_5_14_15"] != reduced_clk:
            self.log.debug("cores 4 5 14 15 = {} clk not reduced".format(acc_clk_cfg['cores_4_5_14_15']))
            clk_ok = False
        return clk_ok
    
    def assert_acc_clk_boost(self, device):
        acc_clk_cfg = device.get_acc_ss_cpu_clk_status()
        vco = acc_clk_cfg["pll_vco"]
        if not vco:
            self.log.error("invalid cpu clk pll VCO value")
            raise Exception("VCO vlaue is not valid")
        boosted_clk = int(vco/2)
        clk_ok = True
        self.table["CPU_PLL_CFG_0_inst"] = hex(acc_clk_cfg["CPU_PLL_CFG_0_inst"])
        self.table["CPU_PLL_CFG_1_inst"] = hex(acc_clk_cfg["CPU_PLL_CFG_1_inst"])
        self.table["CPU_PLL_CFG_2_inst"] = hex(acc_clk_cfg["CPU_PLL_CFG_2_inst"])

        self.table["cores_0_1_2_3"] = acc_clk_cfg["cores_0_1_2_3"]
        self.table["cores_6_7_8_9"] = acc_clk_cfg["cores_6_7_8_9"]
        self.table["cores_10_11_12_13"] = acc_clk_cfg["cores_10_11_12_13"]
        self.table["cores_4_5_14_15"] = acc_clk_cfg["cores_4_5_14_15"]

        self.log.info("ACC CLK cores 0, 1, 2, 3    : {}MHz".format(acc_clk_cfg["cores_0_1_2_3"]))
        self.log.info("ACC CLK cores 6, 7, 8, 9    : {}MHz".format(acc_clk_cfg["cores_6_7_8_9"]))
        self.log.info("ACC CLK cores 10, 11, 12, 13: {}MHz".format(acc_clk_cfg["cores_10_11_12_13"]))
        self.log.info("ACC CLK cores 4, 5, 14, 15  : {}MHz".format(acc_clk_cfg["cores_4_5_14_15"]))
        self.log.info("NICHOT signal status   : {}".format(hex(device.get_nichot_status())))
        self.log.info("THERMTRIP signal status: {}".format(hex(device.get_thermtrip_status())))

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
        #checking cores 4,5,14,15
        if acc_clk_cfg["cores_4_5_14_15"] != boosted_clk:
            self.log.debug("cores 3 4 14 15 = {} clk not boosted".format(acc_clk_cfg['cores_4_5_14_15']))
            clk_ok = False
        return clk_ok

    def execute_iteration(self):
        self.table["test iteration_number"] = self.test_iteration
        self.log.info("-" * 80)
        self.log.info("Iteration {}".format(self.test_iteration), 'g')
        self.log.info("PVT OTP efuses")
        self.log_pvt_fuses(self.dut)
        #testing for clk reduction above threshold
        if self.last_interrupt_temp is not None:
            nichot_temp = int(self.last_interrupt_temp) - 2
        else:
            nichot_temp = self.dut.get_nichot_threshold(hysteresis_direction="up") 
            
        self.log.info("preheating the SoC")
        self.set_t_case(nichot_temp - 20)
        self.table["NICHOT Threshold"] = nichot_temp
        self.log.info("Setting temperature to {}".format(nichot_temp))
        self.set_temperature(self.dut, nichot_temp)
        max_temp = 125 
           
        throttling_flag = False
        # sweeping through nichot temp and max temp of 130 
        for current_temp in range(nichot_temp, max_temp):
            self.log_pvt_registers(self.dut)
            self.log.info("setting Temperature to {}".format(current_temp))
            self.set_temperature(self.dut, current_temp)
            self.table["T case [C]"] = self.get_t_case()
            self.table["T diode [C]"] = self.get_t_diode(self.dut)
            if self.assert_acc_clk_reduction(self.dut):
                self.last_interrupt_temp = self.get_t_case() 
                throttling_flag = True
                self.log.info("acc clk is redued", 'g')
                self.table.end_row()
                self.log.line()
                break
            self.table.end_row()
        if not throttling_flag:
            self.append_iteration_fail_reason("cpu throttling did not occure within temperature range of {}-{}".format(nichot_temp, max_temp))
                
        #testing for clk boost below hysteresis value
        nichot_temp = self.dut.get_nichot_threshold(hysteresis_direction="down") - 1
        self.table["NICHOT Threshold hysteresis down"] = nichot_temp
        self.log.info("Setting temperature to {}".format(nichot_temp))
        self.set_temperature(self.dut, nichot_temp)
        timer = Timer(10)
        timer.start()
        while True:
            self.log_pvt_registers(self.dut)
            if timer.expired():
                self.log.error("10 sec timer expired. acc clk is not boosted")
                self.append_iteration_fail_reason("10 sec timer expired. acc clk is not boosted ")
                break
            if self.assert_acc_clk_boost(self.dut):
                self.log.info("acc clk is boosted", 'g')
                self.table.end_row()
                break
            self.table.end_row()
            self.log.line()

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
                    if self.args.get("log_level", "INFO") == "debug":
                        import traceback
                        self.log.debug(traceback.format_exc())
                    self.append_fail_reason(str(e))
                finally:
                    self.reset_temperature()
                    self.summarize_iteration()
        else:
            self.log.error("Failed to prepare test")
            self.append_fail_reason("Failed to prepare test")

