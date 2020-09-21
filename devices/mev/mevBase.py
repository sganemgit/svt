
import sys
from core.devices.deviceBase import deviceBase
from core.drivers.DriverFactory import DriverFactory

class mevBase:

    def __init__(self, device_number, pf_number, hostname=''):
        self.project_name = 'mev'
        self.project_name_2 = 'mevcp'
        self.driver_type = 'sv'
        self.device_numver = device_number
        self.pf_number = pf_number
        self.hostname = hostname
        try:
            self.driver = DriverFactory.create_driver_by_project_name(self.driver_type, self.project_name, device_number, pf_number, hostname)
        except Exception as e:
            print("Driver Creation has failed")
            print(str(e))
            sys.exit()
