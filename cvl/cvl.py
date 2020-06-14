from core.drivers import DriverFactory



class cvl:
    'This class contains all the methods to interface with a cvl pf'
    def __init__(self, device_number, port_number):
        self.device_number =  device_number
        self.port_number = port_number

    def print_info(self):
        print(F"device number: {self.device_number}")
        print(F"port number: {self.port_number}")
