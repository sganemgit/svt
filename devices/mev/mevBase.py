

from core.drivers.DevieFactory import DeviceFactory

class mevBase:

    def __init__(self, device_nubmer, pf_number, hostname='')
        self.project_name = 'mev'
        self.project_name_2 = 'mevcp'
        self.device_numver = device_nubmer
        self.pf_number = pf_number
        self.hostname = hostname
        self.driver = DriverFactory.create_driver_by_name(project_name
