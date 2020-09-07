
#--------------------------------------------
# @author Shady Ganem <shady.ganem@intel.com>
#--------------------------------------------

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