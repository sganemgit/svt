
# @author Shady Ganem <shady.ganem@intel.com>

from core.drivers.DriverFactory import DriverFactory
from core.devices.deviceBase import deviceBase
import sys
from devices.cnv.AdminCommandHandler import AdminCommandHandler
from devices.cnv.DataHandler import DataHandler

class cnvBase:
    '''
        This class is the base class for CNV infreface, defines the constructor 
        and holds information about the object instance
        dervied classes define functionality
    '''
    def __init__(self, device_number, port_number, hostname="", driver_type = "sv"):
        self.project_name = "cvn"
        self.driver_type = driver_type
        self.device_number = device_number
        self.port_number = port_number
        self.hostname = hostname
        try:
            self.driver = DriverFactory.create_driver_by_project_name(self.driver_type, self.project_name, device_number, port_number, hostname)
            self.aq = AdminCommandHandler(self.driver)    
            self.data = DataHandler() 
        except Exception as e:
            print("Driver Creation has failed")
