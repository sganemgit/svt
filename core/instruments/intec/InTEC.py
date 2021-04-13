# @author Shady Ganem <shady.ganem@intel.com>

import libIntec.libIntec as intec

class InTEC:
    
    @staticmethod
    def GetLibVersion():
        ver = intec.GetlibVersion()
        return f"{ver['major']}.{ver['minor']}"

    def __init__(self, index, intec_type="IntecH"):
        self._dev_index = index
        self._type = intec_type 
        self._card_id = 0

    def SetCardId(self, cardId):
        self._card_id = cardId

    def connect(self):
        try:
            if not intec.Initialize(self._type):
                raise Exception("Failed to initialize libIntec")
            if not intec.InitializeCard(self._dev_index):
                raise Exception("Failed to initialize card")
            return True
        except Exception as e:
            return False

    def GetTemperature(self):
        try:
            return intec.GetTemperature(self._dev_index, self._card_id)
        except Exception as e:
            return False

    def SetTemperature(self, temp):
        try:
            return intec.SetTemperature(self._dev_index, self._card_id, temp)
        except Exception as e:
            return False

if __name__=="__main__":
    tec = InTEC(0)
    tec.connect()
    print(tec.GetLibVersion())
    print(tec.GetTemperature())
    print(tec.SetTemperature(25))

