
# @author Shady Ganem <shady.ganem@intel.com>

from core.drivers.DriverFactory import DriverFactory
from core.drivers.svdriver.SvDriverCommands import *
from core.structs.DeviceInfo import DeviceInfo
import sys
class cvlBase:
    '''
        This class is the base class for CVL classes 
        it defines the init method and interacts with the infrastructure of the
        environment
        dervied classed define functionality
    '''
    def __init__(self, device_number, port_number, hostname=""):
        self.project_name = "cvl"
        self.driver_type = "sv"
        self.device_number = device_number
        self.port_number = port_number
	self.hostname = hostname
        try:
            self.driver = DriverFactory.create_driver_by_project_name(self.driver_type, self.project_name, device_number, port_number, hostname)
        except Exception as e:
            print("Driver Creatiot failed ",str(e))
            sys.exit()

