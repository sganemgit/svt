
# @author Shady Ganem <shady.ganem@intel.com>

from core.structs.DeviceInfo import DeviceInfo

class DriverFactory():
    """
        This class acts as a common interface for driver object creation
    """

    @classmethod
    def _create_driver_by_name(cls, device_name, device_number, port_number, hostname = ""):
        '''This method constructs an SvDriver object
            input params @device_name
                         @device_number
                         @port_number
                         @hostname
         '''
        from core.drivers.svdriver.SvDriver import SvDriver
        device_info = DeviceInfo()
        device_info.device_name = device_name
        device_info.device_number = str(device_number)
        device_info.port_number = str(port_number)
        device_info.hostname = hostname
        return SvDriver(device_info)

    @classmethod
    def create_driver_by_project_name(cls, driver_type, project_name, device_number, pf_number, hostname):
        device_info = None
        if driver_type == "sv":
            device_info = cls._create_device_info(project_name, device_number, pf_number, hostname)
            if project_name == 'mev' or project_name == 'mev1':
                return cls._create_driver_by_name(project_name, device_number, pf_number, hostname)
                return None
            else:
                return cls._create_driver_by_name(project_name, device_number, pf_number, hostname)


    @classmethod
    def create_driver(cls, driver_type, device_info):
        '''
            Class method that creates driver according to driver type.
            If driver type not supported RuntimeError will be raised.
       '''
        if driver_type == 'sv':
            from core.drivers.svdriver import SvDriver
            return SvDriver(device_info)
        else:
            error = "Failed to create driver of type {}, Unsupported dirver type".format(driver_type)
            raise RuntimeError(error)

    @classmethod
    def _create_device_info(cls, device_name, device_number, pf_number, hostname = ""):
        device_info = DeviceInfo()
        device_info.device_name = device_name
        device_info.device_number = str(device_number)
        device_info.port_number = str(pf_number)
        device_info.hostname = hostname
        return device_info

    @classmethod
    def create_sv_driver(cls, project_name, device_number, pf_number, hostname, driver_family):
        device_info = cls._create_device_info(project_name, device_number, pf_number, hostname)
        if driver_family == "igb":
            from core.drivers.svdriver.igb import igb
            return igb(device_info)
        elif driver_family == "ixgbe":
            from core.drivers.svdriver.ixgbe import ixgbe
            return ixgbe(device_info)
        elif driver_family == "i40e":
            from core.drivers.svdriver.i40e import i40e
            return i40e(device_info)
        elif driver_family == "i200e":
            from core.drivers.svdriver.i200e import i200e
            return i200e(device_info)
        elif driver_family == "idpf":
            from core.drivers.svdriver.idpf import idpf
            return idpf(device_info)
        elif driver_family == "icpf":
            from core.drivers.svdriver.icpf import icpf
            return icpf(device_info)
        else:
            raise Exception("{}: Undefined Driver Family ".format(driver_family))

    @classmethod
    def create_ftdi_driver(cls, ftdi_index=1):
        from core.drivers.ftdidriver.FtdiDriver import FtdiDriver
        return FtdiDriver(ftdi_index)
