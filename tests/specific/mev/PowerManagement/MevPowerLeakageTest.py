
# @author Shady Ganem <shady.ganem@intel.com>

Test = True

from test.specific.mev.PowerManagement.MevPowerManagementBase import MevPowerManagementBase

class MevPowerLeackageTest(MevPowerManagementBase):
    
    def run(self):
        self.log_input_args()
        self.init_test_args()
        
        for iteration in range(self.num_of_iterations):
            self.test_iteration = iteration
            try:
                self.execute_iteration()
            except Exception as e:
                self.append_fail_reason(str(e))
            finally:
                self.summarize_iteration()
