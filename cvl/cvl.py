from core.drivers import DriverFactory
from core.structs.PortInfo import PortInfo


class cvl:
    'This class contains all the methods to interface with a cvl pf'
    def __init__(self, device_number, port_number):
        self.port_info = PortInfo()
        self.port_info.device_name = "cvl"
        self.port_info.device_number = device_number
        self.port_info.port_info = port_number
        self.port_info.dev_id = 
        self.driver_type = "sv"
        self.device_number =  device_number
        self.port_number = port_number
        self.driver = DriverFactory.create_driver(self.driver_type, )

    def print_info(self):
        print(F"device number: {self.device_number}")
        print(F"port number: {self.port_number}")
