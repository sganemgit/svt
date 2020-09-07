
#--------------------------------------------
# @author Shady Ganem <shady.ganem@intel.com>
#--------------------------------------------

from core.drivers.DriverFactory import DriverFactory
from core.devices.deviceBase import deviceBase
import sys

class cvlBase:
    '''
        This class is the base class for CVL infreface, defines the constructor 
        and holds information about the object instance
        dervied classed define functionality
    '''
    def __init__(self, device_number, port_number, hostname="", driver_type = "sv"):
        self.project_name = "cvl"
        self.driver_type = driver_type
        self.device_number = device_number
        self.port_number = port_number
        self.hostname = hostname
        try:
            self.driver = DriverFactory.create_driver_by_project_name(self.driver_type, self.project_name, device_number, port_number, hostname)
        except Exception as e:
            print("Driver Creation has failed")
            print(str(e))
            sys.exit()