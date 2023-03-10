
# @author Shady Ganem <shady.ganem@intel.com>

from core.drivers.DriverFactory import DriverFactory
from core.devices.deviceBase import deviceBase
import sys
from devices.cvl.cvlAq import cvlAq 
from devices.cvl.cvlData import cvlData 

class cvlBase:
    '''
        This class is the base class for CVL infreface, defines the constructor 
        and holds information about the object instance
        dervied classed define functionality
    '''
    def __init__(self, device_number, port_number, hostname="", driver_type = "sv"):
        self.project_name = "cvl"
        self.driver_family = "i200e"
        self.driver_type = driver_type
        self.device_number = device_number
        self.port_number = port_number
        self.hostname = hostname
        try:
            self.driver = DriverFactory.create_sv_driver(self.project_name, device_number, port_number, hostname, self.driver_family)
            self.aq = cvlAq(self.driver)    
            self.data = cvlData() 
        except Exception as e:
            print("Driver Creation has failed")
            print(str(e))
            sys.exit()

