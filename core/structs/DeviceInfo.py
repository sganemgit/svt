from core.drivers.svdriver.SvDriverCommands import svdt

'''This data structure holds the information neccessry for creating a driver instance'''
class DeviceInfo():
    def __init__(self):
        self.device_name = None
        self.device_number = None
        self.port_number = None
        self.dev_id = None
        self.driver_specific_id = None
        self.location = None
        self.hostname = None
