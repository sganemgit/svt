
# @author Shady Ganem <shady.ganem@intel.com>

from core.utilities.BitManipulation import *
from core.structs.AqDescriptor import AqDescriptor

class AdminCommandHandler:
    def __init__(self, driver_reference):
        self.driver = driver_reference

    def SetPhyConfig(self, config, debug=False):
        pass 
