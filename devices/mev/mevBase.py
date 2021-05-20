
#@author Shady Ganem <shady.ganem@intel.com>

import sys
#from core.devices.deviceBase import deviceBase
from core.drivers.DriverFactory import DriverFactory
from devices.mev.mevFpga import mevFpga
from devices.mev.mevData import mevData

class mevBase:

    def __init__(self, device_number, pf_number, mev_type="mev", driver_family="idpf", hostname=''):
        self.name = mev_type 
        self.project_name = mev_type
        self.driver_family = driver_family
        self.name_2 = 'mevcp'
        self.driver_type = 'sv'
        self.device_number = device_number
        self.pf_number = pf_number
        self.hostname = hostname
        self.fpga = None
        self.driver = None
        self.data = mevData()
        self.init_sv_driver()
    
    @classmethod
    def create_mev1(cls, device_number, pf_number, driver_family="idpf", hostname=''):
        return cls(device_number, pf_number, "mev1", driver_family, hostname)
    
    @classmethod
    def create_mev(cls, device_number, pf_number, driver_family="idpf", hostname=''):
        return cls(device_number, pf_number, "mev", driver_family, hostname)
    
    def init_fpga(self, ft_index):
        try:
            self.fpga = mevFpga(ft_index)
            self.fpga.connect()
        except Exception as e:
            raise e
    
    def init_sv_driver(self):
        try:
            self.driver = DriverFactory.create_sv_driver(self.project_name, self.device_number, self.pf_number, self.hostname, self.driver_family)
        except Exception as e:
            print("Driver Creation has failed")
            print(str(e))
            sys.exit()

