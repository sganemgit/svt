from core.drivers import DriverFactory
from core.structs.PortInfo import PortInfo
from core.drivers.svdriver.SvDriverCommands import *


class cvl:
    'This class contains all the methods to interface with a cvl pf'
    def __init__(self, device_number, port_number):
        self.project_name = "cvl"
        self.driver_type = "sv"
        self.device_number = device_number
        self.port_number = port_number
        self.dev_id  

    def print_info(self):
        print(F"device number: {self.device_number}")
        print(F"port number: {self.port_number}")
