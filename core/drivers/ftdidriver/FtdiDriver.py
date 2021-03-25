from ftd2xx import ftd2xx as ftd

import sys
import time


class FtdiDriver:

    BIT_MODES = {"reset": 0x0,
                 "asyc_bit_bang": 0x1,
                 "mpsse": 0x2,
                 "sync_bit_bang": 0x4,
                 "mcu_host_bus_emulated":0x8,
                 "fast_opto-isolated_serial": 0x10,
                 "cbus_bit_bang": 0x20,
                 "single_channel_sync": 0x40} 

    def __init__(self, index):
        self.index = index 
        try:
            self._driver_proxy = ftd.open(index)
            self._driver_proxy.resetDevice()
        except Exception as e:
            print("error at FtdiDriver")
            raise e

    def __del__(self):
        try:
            self._driver_proxy.close()
        except Exception as e:
            print("exception raised while trying to close ftdi handler")
            raise e

    def configure_mpsse(self):
        self._driver_proxy.resetDevice()
        num_of_bytes = self._driver_proxy.getQueueStatus()
        #self._driver_proxy.read(num_of_bytes)
        self._driver_proxy.setUSBParameters(65536, 65535)
        self._driver_proxy.setChars(False, 0, False, 0)
        self._driver_proxy.setTimeouts(0, 5000)
        self._driver_proxy.setLatencyTimer(1)
        self._driver_proxy.setFlowControl(0x0100, 0x0, 0x0)
        self._driver_proxy.setBitMode(0, 0)
        self._driver_proxy.setBitMode(0, 0x2)
        return self._driver_proxy.status

    def configure_asyc_bit_bang(self, mask):
        self._driver_proxy.setBitMode(mask, 0x1)
        return self._driver_proxy.status

    def get_driver_version(self):
        return self._driver_proxy.getDriverVersion()
    
    def set_bit_mode(self, mask, enable):
        self._driver_proxy.setBitMode(mask, enable)

    def set_baud_rate(self, baud_rate):
        self._driver_proxy.setBaudRate(baud_rate)

    def ft_write(self, data):
        s = str(bytearray(data)) if sys.version_info < (3,) else bytes(data)
        return self._driver_proxy.write(s)
    
    def ft_read(self, n_bytes):
        s = self._driver_proxy.read(n_bytes)
        return [ord(c) for c in s] if type(s) is str else list(s)

    def ft_reset_device(self):
        self._driver_proxy.resetDevice()
        return self._driver_proxy.status

    def get_device_info(self):
        return self._driver_proxy.getDeviceInfo()

if __name__=='__main__':
    d = FtdiDriver(0)

    #d = FtdiDriver(1)
    #from core.structs.FtdiFpgaPacket import FtdiFpgaPacket as fpack
    #read_pack = fpack()
    #read_pack.op_code = 0x1
    #read_pack.len 
    #print d.get_driver_version()
    #print d.get_device_info()
    #a = [0,0xff,2,3, 4]
    #print d.ft_write(a)
