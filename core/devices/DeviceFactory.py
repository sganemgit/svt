
# @author Shady Ganem <shady.ganem@intel.com>

class DeviceFactory:
    _supported_devices_list = ['cvl', 'mev', 'mev1', 'crsvl']

    @classmethod
    def create_device(cls, device_name, device_number, pf_number, hostname = ''):
        if device_name == 'cvl':
            from devices.cvl.cvl import cvl
            return cvl(device_number, pf_number, hostname)
        elif device_name == 'crsvl':
            from devices.crsvl.crsvl import crsvl
            return crsvl(device_number, pf_number, hostname)
        elif device_name == 'mev' or device_name == 'mev1':
            from devices.mev.mev import mev
            return mev(device_number, pf_number, hostname)

    @classmethod
    def get_supported_devices(cls):
        return cls._supported_devices_list

    @classmethod
    def create_device_pairs(cls):
        pass

#    def _create_devices(self):
#        devices_info_dict = dict()
#        try:
#            devices_list = self._setup_dom.getroot().findall('devices/device')
#            for device_ET in devices_list:
#                port_list = device_ET.findall('port')
#                for port_ET in port_list:
#                    info_dict = dict()
#                    info_dict['device_name'] = device_ET.get('name')
#                    info_dict['device_number'] = device_ET.get('driverDeviceNumber')
#                    info_dict['hostname'] = device_ET.get('host')
#                    info_dict['port_number'] = port_ET.get('driverPortNumber')
#                    devices_info_dict[port_ET.get('uniqueId')] = info_dict
#            devices_dict = dict()
#            for device, info in devices_info_dict.iteritems():
#                devices_dict[device] = DeviceFactory.create_device(info['device_name'], info['device_number'], info['port_number'], info['hostname'])
#            return devices_dict
#        except Exception as e:
#            raise e

    @classmethod
    def create_devices_from_setup(cls, devices):
        '''
            @input devices (dict)
                    device = {'device_index': {'name': value,
                                               'number' : value,
                                               'hostname': value,
                                               'Ports': {id:number,
                                                         id: nubmer,
                                                         ...},
                              ...}}

        '''
        pf_dict = dict()
        for device_id, device_dict, in devices.items():
            for pf_id, number in device_dict['Ports'].items():
                pf_dict[pf_id] = cls.create_device(device_dict['name'], int(device_dict['number']), int(number), device_dict['hostname'])
        return pf_dict
 

