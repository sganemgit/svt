# @author Shady Ganem <shady.ganem@intel.com>
try:
    from ftd2xx import ftd2xx as ftd
except Exception as e:
    print("unable to import ftd2xx")
    raise e

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

    def configure_for_sv_fpga(self):
        # no need to call this funtion
        self._driver_proxy.setBaudRate(12000000)
        self._driver_proxy.setDataCharacteristics(8, 0, 0)
        self._driver_proxy.setFlowControl(0x100, 0x11, 0x13)
        self._driver_proxy.setTimeouts(5000, 5000)
        time.sleep(0.05)

    def configure_mpsse(self):
        #no need to call this function
        self._driver_proxy.resetDevice()
        num_of_bytes = self._driver_proxy.getQueueStatus()
        if num_of_bytes:
            self._driver_proxy.read(num_of_bytes)
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

    def ft_write(self, bytedata):
        return self._driver_proxy.write(bytedata)
    
    def ft_read(self, n_bytes):
        queue_status = self._driver_proxy.getQueueStatus()
        if queue_status == 0:
            return [] 
        if n_bytes > queue_status:
            s = self._driver_proxy.read(queue_status)
        else: 
            s = self._driver_proxy.read(n_bytes)
        return list(s)
        return [ord(c) for c in s] if type(s) is str else list(s)

    def ft_reset_device(self):
        self._driver_proxy.resetDevice()
        return self._driver_proxy.status

    def ft_get_queue_status(self):
        return self._driver_proxy.getQueueStatus()

    def ft_get_device_info(self):
        return self._driver_proxy.getDeviceInfo()
    
    @classmethod
    def ft_get_all_devices_info(self):
        devices = ftd.listDevices()
        ret_dict = dict()
        for dev in range(len(devices)):
            ret_dict[dev] = ftd.getDeviceInfoDetail(dev)
        return ret_dict

    @classmethod 
    def print_all_devices_info(cls):
        devices = cls.ft_get_all_devices_info()
        for index, info_dict in sorted(devices.items()):
            print(f"device index : {index}")
            print()
            for key, val in sorted(info_dict.items()):
                print(f"{key} : {val}")
            print()
            print("-"*10)
            print()

if __name__=='__main__':
    FtdiDriver.print_all_devices_info()
