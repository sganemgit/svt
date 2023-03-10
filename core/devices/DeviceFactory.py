
# @author Shady Ganem <shady.ganem@intel.com>

from core.utilities.colors import colors
class DeviceFactory:
    _supported_devices_list = ['cvl', 'mev', 'mev1', 'crsvl','cpk', 'fvl', 'fpk']

    @classmethod
    def create_device(cls, device_name, device_number, pf_number, driver=None, hostname = ''):
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
        elif device_name == 'mev':
            from devices.mev.mev import mev
            return mev.create_mev(device_number, pf_number, driver if driver is not None else "idpf", hostname)
        elif device_name == 'mev1':
            from devices.mev.mev import mev
            return mev.create_mev1(device_number, pf_number, driver if driver is not None else "idpf", hostname)

    @classmethod
    def create_dut_lp_pairs(cls, links, devices):
        pair_list = list()
        for link, roles in links.items():
            if roles['dut'] in devices.keys() and roles['lp'] in devices.keys():
                pair_list.append((devices[roles['dut']], devices[roles['lp']]))
            else:
                print(colors.Orange("WARNING: Ports with IDs {}, {} do not appear in devices".format(roles['dut'], roles['lp'])))
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
        for device_id, device_attrib in devices.items():
            for pf_id, pf_attrib in device_attrib['PFs'].items():
                pf_dict[pf_id] = cls.create_device(device_attrib['name'], int(device_attrib['number']), int(pf_attrib['number']), pf_attrib.get('driver', None), device_attrib['hostname'])
        return pf_dict
 

