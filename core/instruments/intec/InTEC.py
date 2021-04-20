
# @author Shady Ganem <shady.ganem@intel.com>

import core.instruments.intec.libIntec.libIntec as intec

class InTEC:
    
    @staticmethod
    def GetLibVersion():
        ver = intec.GetlibVersion()
        return f"{ver['major']}.{ver['minor']}"
    
    def GetInstrumentName(self):
        return "intec"

    def GetType(self):
        return self._type

    def __init__(self, index, intec_type="IntecH"):
        self._dev_index = index
        self._type = intec_type 
        self._card_id = 0
        self._connection_flag = False

    def SetCardId(self, cardId):
        self._card_id = cardId

    def connect(self):
        try:
            if not intec.Initialize(self._type):
                raise Exception("Failed to initialize libIntec")
            if not intec.InitializeCard(self._dev_index):
                raise Exception("Failed to initialize card")
            self._connection_flag = True
            return True
        except Exception as e:
            return None 
    
    def __del__(self):
        try:
            intec.Exit()
        except Exception as e:
            raise e
    
    def disconnect(self):
        try:
            intec.Exit()
            return True
        except Exception as e:
            return None 

    def GetTemperature(self):
        try:
            if self._connection_flag:
                return intec.GetTemperature(self._dev_index, self._card_id)
            else:
                print("must call connect before using intec API")
                exit(1)
        except Exception as e:
            return None 

    def SetTemperature(self, temp):
        try:
            if self._connection_flag:
                return intec.SetTemperature(self._dev_index, self._card_id, temp)
            else:
                print("must call connect before using intec API")
                exit(1)
        except Exception as e:
            return None 

#if __name__=="__main__":
#    tec = InTEC(0)
#    tec.connect()
#    print(tec.GetLibVersion())
#    print(tec.GetTemperature())
#    print(tec.SetTemperature(25))

