
# @author Shady Ganem <shady.ganem@intel.com>

TEST = True

from tests.specific.mev.ThermalManagement.ThermalManagementBase import ThermalManagementBase

class MevThermalSensorCalibrationTest(ThermalManagementBase):
    
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
