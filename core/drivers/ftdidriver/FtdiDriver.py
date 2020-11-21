from core.drivers.ftdidriver.ftd2xx import ftd2xx as ftd
import sys


class FtdiDriver:

    @classmethod
    def GetFtdiDevices(cls):
        return ftd.listDevices()

    def __init__(self, index):
        self.index = index 
        try:
            self._driver_proxy = ftd.open(index)
            self.set_bit_mode(0x01, 1) #set pin D0 as the output pin
        except Exception as e:
            print("error at FtdiDriver")
            raise e

    def get_driver_version(self):
        return self._driver_proxy.getDriverVersion()
    
    def set_bit_mode(self, mask, enable):
        self._driver_proxy.setBitMode(mask, enable)

    def set_baud_rate(self, baud_rate):
        self._driver_proxy.setBaudRate(baud_rate)

    def ft_write(self, data):
        s = str(bytearray(data)) if sys.version_info<(3,) else bytes(data)
        return self._driver_proxy.write(s)
    
    def ft_read(self, n_bytes):
        s = self._driver_proxy.read(n_bytes)
        return [ord(c) for c in s] if type(s) is str else list(s)

    def get_device_info(self):
        return self._driver_proxy.getDeviceInfo()

if __name__=='__main__':
    d = FtdiDriver(1)
    print d.get_driver_version()
    print d.get_device_info()
    a = [0,1,2,3, 4]
    print d.ft_write(a)
    print d.ft_read(10)
