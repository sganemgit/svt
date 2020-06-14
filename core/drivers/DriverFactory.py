class DriverFactory(object):
    """Class that is responsible for creation of drivers"""

    @classmethod
    def create_driver(cls, driver_type, device_info):
        """ 
        Class method that creates driver according to driver type.
        If driver type not supported RuntimeError will be raised.
        """
        if driver_type == 'sv':
            from core.drivers.svdriver import SvDriver
            return SvDriver(device_info)  
        if driver_type == 'svcp':
            from core.drivers.svcpdriver import SvCpDriver
            return SvCpDriver(device_info) 

        error = 'Failed to create driver of type {}, Unsupported dirver type'.format(driver_type)
        raise RuntimeError(error)
    
def does_driver_require_admin_mode(driver_type):
    if driver_type == 'qv':
        return True
    r
