
# @author Shady Ganem <shady.ganem@intel.com>

class DeviceFactory:
    _supported_devices_list = ['cvl', 'mev', 'mev1', 'crsvl','cpk']

    @classmethod
    def create_device(cls, device_name, device_number, pf_number, hostname = ''):
        if device_name == 'cvl':
            from devices.cvl.cvl import cvl
            return cvl(device_number, pf_number, hostname)
        elif device_name == 'cpk':
            from devices.cpk.cpk import cpk
            return cpk(device_number, pf_number, hostname)
        elif device_name == 'fvl':
            from devices.fvl.fvl import fvl
            return fvl(device_number, pf_number, hostname)
        elif device_name == 'fpk':
            from devices.fpk.fpk import fpk
            return fpk(device_number, pf_number, hostname)
        elif device_name == 'mev' or device_name == 'mev1':
            from devices.mev.mev import mev
            return mev(device_number, pf_number, hostname)

    @classmethod
    def create_dut_lp_pairs(cls, links, devices):
        pair_list = list()
        for link, roles in links.items():
            if roles['dut'] in devices.keys() and roles['lp'] in devices.keys():
                pair_list.append((devices[roles['dut']], devices[roles['lp']]))
            else:
                print("Error: Ports with IDs {}, {} do not appear in devices".format(roles['dut'], roles['lp']))
        return pair_list

    @classmethod
    def get_supported_devices(cls):
        return cls._supported_devices_list

    @classmethod
    def create_device_pairs(cls):
        pass

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
 

