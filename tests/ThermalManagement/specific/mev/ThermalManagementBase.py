
from core.tests.testBase import testBase
from core.exceptions.Exceptions import *
import time

class ThermalManagementBase(testBase):

    def prepare_instruments(self):
        for inst_name, inst in self.instruments.items():
            if inst is not None:
                if inst.GetInstrumentName() == "intec":
                    self.intec = inst
                    self.intec.connect()
                    self.log.info("InTEC device ready", 'g')
        if self.intec is None:
            msg = "could not find an instance of an intec device"
            self.append_fail_reason(msg)
            self.log.error(msg)
            raise FatalTestError(msg)

    def prepare_test(self):
        try:
            self.init_test_data()
            self.prepare_instruments()
            self.prepare_devices()
            return True
        except Exception as e:
            self.append_fail_reason(str(e))
            return False

    def prepare_devices(self):
        #TODO prepare deivce should be generic
        self.dut = self.devices['mev0:0']
        self.dut.init_fpga(self.ftdi_index)
        self.log.info("Devices ready", 'g')
    
    def log_input_args(self):
        self.log.info("-"*80)
        self.log.info("input arguments:", 'o')
        for key, val in self.args.items():
            self.log.info(f"{key} : {val}")
        self.log.info("-"*80)

    def init_test_data(self):
        self.intec = None
        self.iteration_fail_reasons = list()
        self.ftdi_index = int(self.args.get("ftdi_index", "1"))
        self.num_of_iterations = int(self.args.get("num_of_iter", "1"))
        self.log.info("Test data ready", 'g')

    def append_iteration_fail_reason(self, msg):
        self.append_fail_reason(msg)
        self.iteration_fail_reasons.append("Interation {} - {}".format(self.test_iteration, msg))

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
        """
            This method returns the temperature as a float with 2 digits after decimal point accuracy
            @ input - none
            @ return - float
        """
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
            This method sets the temperature on the silicon and uses the t_diode as a loopback refrence
        '''
        done = False
        stability_counter = 0
        while not done:
            current_t_diode = self.get_t_diode(device)
            self.log.debug("T diode = {}".format(current_t_diode))
            if current_t_diode < temp - 0.25:
                self.inc_t_case()
                stability_counter = 0
            elif current_t_diode > temp + 0.25:
                self.dec_t_case()
                stability_counter = 0
            else:
                stability_counter += 1
            if stability_counter == 3:
                done = True

        self.log.info("T diode = {}".format(self.get_t_diode(device)))
        self.log.info("T case is set to {}".format(self.get_t_case()))
    
    def assert_vnn(self, device, delta):
        vnn_voltage = device.get_voltage(device.data.mev_vnn_rail_name)
        self.log.debug("{} = {}".format(vnn_voltage, device.data.mev_vnn_rail_name))
        if vnn_voltage == device.data.mev_default_vnn + delta:
            self.log.info("{} is set according to ITD LUT".format(device.data.mev_vnn_rail_name))
        else:
            msg = "{} is not set according to ITD LUT".format(device.data.mev_vnn_rail_name)
            self.log.error(msg)
            self.append_fail_reason(msg)
    
    def assert_vcc(self, device, delta):
        vnn_voltage = device.get_voltage(device.data.mev_vcc_rail_name)
        self.log.debug("{} = {}".format(vnn_voltage, device.data.mev_vcc_rail_name))
        if vnn_voltage == device.data.mev_default_vnn + delta:
            self.log.info("{} is set according to ITD LUT".format(device.data.mev_vcc_rail_name))
        else:
            msg = "{} is not set according to ITD LUT".format(device.data.mev_vcc_rail_name)
            self.log.error(msg)
            self.append_fail_reason(msg)
