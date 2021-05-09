
# @author Shady Ganem <shady.ganem@intel.com>

from core.drivers.DriverFactory import DriverFactory
from core.devices.deviceBase import deviceBase
from devices.cpk.AdminCommandHandler import AdminCommandHandler
from devices.cpk.DataHandler import DataHandler
import sys

class cpkBase:
    '''
        This class is the base class for CPK infreface, 
        defines the constructor and holds information about the object instance
        driver classed define functionality
    '''
    def __init__(self, device_number, pf_number, hostname=""):
        self.project_name = "cpk"
        self.driver_family = "i200e"
        self.device_number = device_number
        self.pf_number = pf_number
        self.hostname = hostname
        self.driver = None
        try:
            self.driver = DriverFactory.create_sv_driver(self.project_name, self.device_number, self.pf_number, self.hostname, self.driver_family)
            self.aq = AdminCommandHandler(self.driver)
            self.data = DataHandler()
        except Exception as e:
            print("Driver Creation has failed")
            raise e
