
# @author Shady Ganem <shady.ganem@intel.com>

class SvDriverError(Exception):
    pass

class SetupFileError(Exception):
	pass

class RegressionFileError(Exception):
	pass

class DeviceRoleError(Exception):
	pass

class PhysicalLinkError(Exception):
	pass

class TimerError(Exception):
	pass

class FatalTestError(Exception):
    pass
