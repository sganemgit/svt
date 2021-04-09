# @author Shady Ganem <shady.ganem@intel.com>

#import libIntec as intec

class InTEC:
    
    @staticmethod
    def GetDevicesInfo():
        pass

    def __init__(self, index, intec_type="IntecH"):
        self._dev_index = index
        self._type = intec_type 

    def connect(self):
        pass

    def GetTemperature(self):
        pass
