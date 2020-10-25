
#--------------------------------------------
# @author Shady Ganem <shady.ganem@intel.com>
#--------------------------------------------

from core.drivers.DriverFactory import DriverFactory
from core.devices.deviceBase import deviceBase
from devices.fvl.DataHandler import DataHandler 
from devices.fvl.AdminCommandHandler import AdminCommandHandler
import sys

class fvlBase:
    '''
        This class is the base class for FVL inferface, defines the constructor 
        and holds information about the object instance
        dervied classed define functionality
    '''
    def __init__(self, device_number, port_number, hostname="", driver_type = "sv"):
        self.project_name = "fvl"
        self.driver_type = driver_type
        self.device_number = device_number
        self.port_number = port_number
        self.hostname = hostname
        self._host_or_baseT = 0
        try:
            self.driver = DriverFactory.create_driver_by_project_name(self.driver_type, self.project_name, device_number, port_number, hostname)
            self.aq = AdminCommandHandler(self.driver)
            self.data = DataHandler()
        except Exception as e:
            print("Driver Creation has failed")
            print(str(e))
            sys.exit()
