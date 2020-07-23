class DriverFactory():
    '''This class is responsible for creation of drivers'''
    @classmethod
    def create_driver_by_project_name(cls, driver_type, project_name, device_number, port_number):
        if driver_type == "sv":
            from core.drivers.svdriver.SvDriver import SvDriver
            return SvDriver.create_driver_by_name(project_name, device_number, port_number)

    @classmethod
    def create_driver(cls, driver_type, device_info):
        ''' 
        Class method that creates driver according to driver type.
        If driver type not supported RuntimeError will be raised.
       ''' 
        if driver_type == 'sv':
            from core.drivers.svdriver import SvDriver
            return SvDriver(device_info)  
        else if driver_type == "svcp":
            from core.drivers.svcpdriver import SvCpDriver
            return SvCpDriver SvCpDriver(device_info)

        error = "Failed to create driver of type {}, Unsupported dirver type".format(deriver_type)
        raise RuntimeError(error)
