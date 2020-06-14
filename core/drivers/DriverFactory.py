class DriverFactory(object):
    '''This class is responsible for creation of drivers'''

    @classmethod
    def create_driver(cls, driver_type, port_info):
        ''' 
        Class method that creates driver according to driver type.
        If driver type not supported RuntimeError will be raised.
       ''' 
        if driver_type == 'sv':
            from core.drivers.svdriver import SvDriver
            return SvDriver(port_info)  

        error = F"Failed to create driver of type {driver_type}, Unsupported dirver type"
        raise RuntimeError(error)
