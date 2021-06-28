
# @author Shady Ganem <shady.ganem@intel.com>

TEST = True

from tests.specific.mev.ThermalManagement.ThermalManagementBase import ThermalManagementBase
from core.exceptions.Exceptions import *

class MevTemperatureSweepTest(ThermalManagementBase):

    def describe_test(self):
        self.log.info("Test Describtion:")
        self.log.info("This test checks the ITD feature in MEV1")
    
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
    
    def calculate_mid_range_temps(self, temps):
        mid_range_temps = list()
        mid_range_temps.append(temps[0] - 1)
        for i in range(len(temps)-1):
            mid_range_temps.append(int((temps[i] + temps[i+1])/2))
        return mid_range_temps

    def assert_vnn(self, device, mv_delta):
        vnn_voltage = device.get_voltage(device.data.mev_vnn_rail_name)
        self.table["VNN [V]"] = round(vnn_voltage, 3)
        self.log.debug("{} = {}".format(vnn_voltage, device.data.mev_vnn_rail_name))
        if round(vnn_voltage, 3) == device.get_hvm_vnn_volatge() - mv_delta*0.001:
            return True
        else:
            return False
    
    def assert_vcc(self, device, mv_delta):
        vcc_voltage = device.get_voltage(device.data.mev_vcc_rail_name)
        self.table["VCC [V]"] = round(vcc_voltage, 3)
        vcc_mode = device.get_vcc_operational_mode()
        self.log.debug("{} = {}".format(vnn_voltage, device.data.mev_vcc_rail_name))
        if round(vcc_voltage, 3) == device.get_hvm_vcc_voltage(vcc_mode) - mv_delta*0.001:
            return True
        else:
            False
        
    def execute_iteration(self):
        self.log.info("-"*80)
        self.log.info("Iteration {}".format(self.test_iteration), 'g')

        self.log.info("PVT OTP efuses")
        self.log_pvt_fuses(self.dut)

        if self.assert_ts_calibration(self.dut):
            self.log.info("TS Calibrated")
        else:
            self.log.info("TS not calibirated")

        check_vcc_itd = self.assert_vcc_itd_enabled(self.dut)
        if not check_vcc_itd:
            self.log.info("ITD is disabled for VCC", 'o')
        check_vnn_itd = self.assert_vnn_itd_enabled(self.dut)
        if not check_vcc_itd:
            self.log.info("ITD is disabled for VNN", 'o')

        if not check_vcc_itd and not check_vnn_itd:
            self.append_fail_reason("ITD is disabled for VNN and VCC")
            raise FatalTestError("exiting test iteration because ITD is disabled")

        pvt_vid_vcc_pm = self.dut.get_pvt_vid_vcc_pm()
        if pvt_vid_vcc_pm == 0:
            self.log.info("pvt_vid_vcc_pm == 0. Only VCC standard mode is supported")
        else:
            self.log.info("pvt_vid_vcc_pm > 0. Both VCC standard mode and performance mode are supported")

        pvt_vid_vcc_sm = self.dut.get_pvt_vid_vcc_sm()
        pvt_vid_vnn = self.dut.get_pvt_vid_vnn()

        itd_lut = self.dut.get_itd_lut()
        mid_range_temps = self.calculate_mid_range_temps(itd_lut["max_temp"])
        self.log.info("Iterating over ITD Lookup Talbe")
        self.log.info(self.dut.get_voltage(self.dut.data.mev_vnn_rail_name))
        for temp, vnn_delta, vcc_delta in zip(mid_range_temps, itd_lut["vnn_delta"], itd_lut["vcc_delta"]):
            self.table["Temperature"] = temp
            self.table["VNN Delta"] = vnn_delta
            self.table["VCC Delta"] = vcc_delta
            self.log.info("setting silicon temperature to {}".format(temp))
            self.set_temperature(self.dut, temp)
            if check_vnn_itd:
                if self.assert_vnn(self.dut, vnn_delta):
                    self.log.info("{} is set according to ITD LUT".format(device.data.mev_vnn_rail_name))
                else:
                    msg = "{} is not set according to ITD LUT".format(device.data.mev_vnn_rail_name)
                    self.log.error(msg)
                    self.append_iteration_fail_reason(msg)
                    
            if check_vcc_itd:
                if self.assert_vcc(self.dut, vcc_delta):
                    self.log.info("{} is set according to ITD LUT".format(device.data.mev_vcc_rail_name))
                else:
                    msg = "{} is not set according to ITD LUT".format(device.data.mev_vcc_rail_name)
                    self.log.error(msg)
                    self.append_iteration_fail_reason(msg)

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
