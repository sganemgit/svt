from core.drivers.DriverFactory import DriverFactory
from core.drivers.svdriver.SvDriverCommands import *
from core.structs.DeviceInfo import DeviceInfo

class cvlBase:
    '''
        This class is the base class for CVL classes 
        it defines the init method and interacts with the infrastructure of the
        environment
        dervied classed define functionality
    '''
    def __init__(self, device_number, port_number):
        self.project_name = "cvl"
        self.driver_type = "sv"
        self.device_number = device_number
        self.port_number = port_number
        if not check_device_availability(self.project_name, device_number, port_number):
            print("cvl device {} port {} could not be found".format(device_number,port_number))
            sys.exit()
        else:
            self.driver = DriverFactory.create_driver_by_project_name(self.driver_type, self.project_name, device_number, port_number)
            if self.driver is None:
                raise RuntimeError("driver not intialized")

