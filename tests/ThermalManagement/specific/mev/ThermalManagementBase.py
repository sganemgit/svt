
from core.tests.testBase import testBase
from core.exceptions.Exceptions import *
import time

class ThermalManagementBase(testBase):
    
    mev_itd_lut = {"_comment": "ITD lookup table (max_temp values are in Celsius, resolution of *_delta in mv)",
                   "max_temp":[43,47,51,55,59,63,67,71,75,79,125],
                   "vnn_delta":[10,9,8,7,6,5,4,3,2,1,0],
                   "vcc_delta":[10,9,8,7,6,5,4,3,2,1,0]} 

    def prepare_instruments(self):
        self.log.info("preparing instruments")
        self.intec = None
        for inst_name, inst in self.instruments.items():
            if inst is not None:
                if inst.GetInstrumentName() == "intec":
                    self.intec = inst
                    self.intec.connect()
                    self.log.info("intec device read")
        if self.intec is None:
            raise FatalTestError("could not find an instance of an intec device")
    
    def prepare_devices(self):
        self.log.info("preparing devices")
        self.dut = self.devices['mev0:0']
        self.dut.init_fpga(self.ftdi_index)
    
    def log_input_args(self):
        self.log.info("-"*80)
        self.log.info("input arguments:", 'o')
        for key, val in self.args.items():
            self.log.info(f"{key} : {val}")
        self.log.info("-"*80)

    def init_test_data(self):
        self.log.info("initializing test data")
        self.iteration_fail_reasons = list()
        self.ftdi_index = int(self.args.get("ftdi_index", "1"))
        self.num_of_iterations = int(self.args.get("num_of_iter", "1"))

    def summarize_iteration(self):
        self.log.info("-"*80)
        self.log.info("Iteration number {}".format(self.test_iteration))
        for fail_reason in self.iteration_fail_reasons:
            self.log.info("Fail: {}".format(fail_reason))
        self.iteration_fail_reasons.clear()
        self.log.info("-"*80)

    def inc_t_case(self, step=1):
        if self.intec is not None:
            temperature = round(self.intec.GetTemperature(), 2) + step
            self.set_t_case(temperature)
        else:
            raise FatalTestError("could not find an instance of an intec device")
        pass

    def dec_t_case(self, step=1):
        if self.intec is not None:
            temperature = self.intec.GetTemperature() - 1
            self.set_t_case(temperature)
        else:
            raise FatalTestError("could not find an instance of an intec device")

    def get_t_case(self):
        if self.intec is not None:
            return round(self.intec.GetTemperature(), 2)
        else:
            raise FatalTestError("could not find an instance of an intec device")

    def set_t_case(self, temp_val):
        if self.intec is not None:
            self.log.info("setting T case to {}".format(temp_val))
            self.intec.SetTemperature(temp_val)
            temperature = self.intec.GetTemperature()
            stability_couter = False
            log_odd = False
            while stability_couter < 2:
                temperature = self.intec.GetTemperature()
                if temperature > temp_val - 0.2 and temperature < temp_val + 0.2:
                    stability_couter += 1
                else:
                    stability_couter = 0
                if log_odd:
                    self.log.debug("T case = {}".format(round(temperature, 2)))
                    log_odd = False
                else:
                    log_odd = True
                time.sleep(0.5)
                
        else:
            raise FatalTestError("could not find an instance of an intec device")

    def get_t_diode(self, device):
        if "mev" in device.name:
            return device.get_diode_temperature()
        else:
            raise FatalTestError("could not identify the device name")

    def reset_temperature(self):
        self.set_t_case(25)

    def set_temperature(self, device, temp):
        '''
            this method sets the temperature on the silicon and uses the t_diode as a loopback refrence
        '''
        done = False
        stability_couter = 0
        while not done:
            current_t_diode = self.get_t_diode(device)
            self.log.debug("T diode = {}".format(current_t_diode))
            if current_t_diode < temp - 0.25:
                self.inc_t_case()
                stability_couter = 0
            elif current_t_diode > temp + 0.25:
                self.dec_t_case()
                stability_couter = 0
            else:
                stability_couter += 1
            if stability_couter == 4:
                done = True

        self.log.info("T diode = {}".format(self.get_t_diode(device)))
        self.log.info("T case is set to {}".format(self.get_t_case()))
    
    def assert_vnn(self, device, delta):
        pass
    
    def assert_vcc(self, device, delta):
        pass
        
