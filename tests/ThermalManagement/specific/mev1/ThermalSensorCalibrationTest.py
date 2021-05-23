
# @author Sivan Yehuda <sivan.yehuda@intel.com>

TEST = True

from tests.ThermalManagement.specific.mev1.ThermalManagementBase import ThermalManagementBase

class ThermalSensorCalibrationTest(ThermalManagementBase):
    
    def execute_iteration(self):
        pass

    def run(self):
        self.log.info("Thermal Sensor Calibration Test")
        self.print_input_args()
        self.init_test_args()
        
        for iteration in range(self.num_of_iterations):
            self.test_iteration = iteration
            try:
                self.execute_iteration()
            except Exception as e:
                self.append_fail_reason(str(e))
            finally:
                self.summarize_iteration()
