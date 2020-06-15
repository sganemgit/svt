from core.drivers.DriverFactory import DriverFactory
from core.structs.DeviceInfo import DeviceInfo
from core.drivers.svdriver.SvDriverCommands import *


class cvl:
    'This class contains all the methods to interface with a cvl pf'
    def __init__(self, device_number, port_number):
        self.project_name = "cvl"
        self.driver_type = "sv"
        self.device_number = device_number
        self.port_number = port_number
        if not check_device_availability(self.project_name, device_number, port_number):
            print("cvl device {} port {} could not be found".format(device_number,port_number))
        else:
            self.driver = DriverFactory.create_driver_by_project_name(self.driver_type, self.project_name, device_number, port_number)


    def print_info(self):
        print("device number: {}".format(self.device_number))
        print("port number: ".format(self.port_number))
