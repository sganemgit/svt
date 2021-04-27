
from core.tests.testBase import testBase
from core.exceptions.Exceptions import *
import time

class ThermalManagementBase(testBase):
    
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
            temperature = self.intec.GetTemperature() + step
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
            return self.intec.GetTemperature()
        else:
            raise FatalTestError("could not find an instance of an intec device")

    def set_t_case(self, temp_val):
        if self.intec is not None:
            self.log.info("setting case temperature to {}".format(temp_val))
            self.intec.SetTemperature(temp_val)
            temperature = self.intec.GetTemperature()
            stability_couter = False
            log_odd = False
            while stability_couter < 4:
                temperature = self.intec.GetTemperature()
                if temperature > temp_val - 0.4 and temperature < temp_val + 0.4:
                    stability_couter += 1
                else:
                    stability_couter = 0
                if log_odd:
                    self.log.info("case temperature {}".format(round(temperature, 2)))
                    log_odd = False
                else:
                    log_odd = True
                time.sleep(0.5)
            self.log.info("case temperature is set to {}".format(round(temperature, 2))) 
                
        else:
            raise FatalTestError("could not find an instance of an intec device")

        def get_t_diode(self, device):
            if "mev" in device.name:
                return device.get_diode_temperature()
            else:
                raise FatalTestError("could not identify the device name")

