
#@author Shady Ganem <shady.ganem@intel.com>

import sys
from core.devices.deviceBase import deviceBase
from core.drivers.DriverFactory import DriverFactory
from devices.mev.mevFpga import mevFpga
from devices.mev.mevData import mevData

class mevBase:

    def __init__(self, device_number, pf_number, hostname=''):
        self.project_name = 'mev'
        self.project_name_2 = 'mevcp'
        self.driver_type = 'sv'
        self.device_numver = device_number
        self.pf_number = pf_number
        self.hostname = hostname
        self.fpga = None
        self.driver = None
        self.data = mevData()
    
    def init_fpga(self, ft_index):
        try:
            self.fpga = mevFpga(ft_index)
            self.fpga.connect()
        except Exception as e:
            raise e
    
    def init_sv_driver(self):
        try:
            self.driver = DriverFactory.create_driver_by_project_name(self.driver_type, self.project_name, self.device_number, self.pf_number, self.hostname)
        except Exception as e:
            print("Driver Creation has failed")
            print(str(e))
            sys.exit()

