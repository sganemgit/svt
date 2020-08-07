

class DeviceFactory:
	
	@classmethod
	def create_device(cls, device_name, device_number, pf_number, hostname):

		if device_name == 'cvl':
			from device.cvl.cvl import cvl
			return cvl(device_number, pf_number, hostname)
		elif device_name == 'mev' or device_name == 'mev1':
			from devices.mev.mev import mev
			return mev(device_number, pf_number, hostname)