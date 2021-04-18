
from core.tests.testBase import testBase


class ThermalManagementBase(testBase):
    
    def print_input_args(self):
        self.log.info("-"*80)
        self.log.info("input arguments", 'o')
        for key, val in self.args.items():
            self.log.info(f"{key} : {val}")
        self.log.info("-"*80)

    def init_test_args(self):
        self.ftdi_index = int(self.args.get("ftdi_index", "1"))
        self.num_of_iterations = int(self.args.get("num_of_iter", "1"))

    def summarize_iteration(self):
        self.log.info("-"*80)
        #TODO: need to implement the iteration summary function
        self.log.info("Iteration summary goes here")
        self.log.info("-"*80)

    def set_T_case(self, intec, temparture_value):
        intec.SetTemperature(temaprute_value)



        
