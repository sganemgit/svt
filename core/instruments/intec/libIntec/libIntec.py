#!/usr/bin/python3

# @author Shady Ganem <shady.ganem@intel.com>

from __future__ import absolute_import 
from ctypes import *
import os
import platform 
from enum import Enum

if platform.system() == "Linux":
    os.environ["LD_LIBRARY_PATH"] = f"$LD_LIBRARY_PATH:{os.environ['PWD']}"
    __libIntec = cdll.LoadLibrary("libIntec.so")
#elif platform.system() == "Windows":
#    libIntec = ctypes.

IntecUsbDeviceTypeToInt = { "IntecH" : 0,
                            "IntecD" : 1,
                            "TAU"    : 2}

def Initialize(device="IntecH"):
    __device = c_int(IntecUsbDeviceTypeToInt.get(device, 0))
    __ret = c_int()
    try:
        __ret = __libIntec.__libIntec_Initialize(__device)
    except Exception as e:
        raise Exception("libIntec exception at Initialize")
    if __ret != 0:
        raise Exception("libIntec exception at Initialize")
    return True

def Exit():
    __ret = c_int()
    try:
        __ret = __libIntec.__libIntec_Exit()
    except Exception as e:
        raise Exception("libIntec exception at Exit")
    if __ret != 0:
        raise Exception("libIntec exception at Exit")
    return True

def InitializeCard(index):
    __index = c_int(index)
    __ret = c_int()
    try:
        __ret = __libIntec.__libIntec_InitializeCard(__index)
    except Exception as e:
        raise Exception("libIntec exception at InitializeCard")
    if __ret != 0:
        raise Exception("libIntec exception at InitializeCard")
    return True

def GetTemperature(index, cardId):
    __index = c_uint(index)
    __cardId = c_int(cardId)
    __temperature = c_float()
    __timestamp = c_uint()
    try:
        __ret = __libIntec.__libIntec_GetTemperature(__index, __cardId, pointer(__temperature), pointer(__timestamp))
    except Exception as e:
        raise Exception("libIntec exception at GetTemperature")

    if __ret != 0:
        raise Exception("libIntec exception at GetTemperature")
    return __temperature.value

def GetTemperatureWithTimestamp(index, cardId):
    __index = c_uint(index)
    __cardId = c_int(cardId)
    __temperature = c_float()
    __timestamp = c_uint()
    try:
        __ret = __libIntec.__libIntec_GetTemperature(__index, __cardId, pointer(__temperature), pointer(__timestamp))
    except Exception as e:
        raise Exception("libIntec exception at GetTemperature")

    if __ret != 0:
        raise Exception("libIntec exception at GetTemperature")
    return {"temperature": __temperature.value, "timestamp": __timestamp.value}

def SetTemperature(index, cardId, temp):
    __index = c_uint(index)
    __cardId = c_int(cardId)
    __temp = c_float(temp)

    __ret = __libIntec.__libIntec_SetTemperature(__index, __cardId, __temp)
    try:
        pass
        #__ret = __libIntec.__libIntec__SetTemperature(__index, __cardId, __temp)
    except Exception as e:
        raise Exception("libIntec exception at SetTemperature")  

    if __ret != 0:
        raise Exception("libIntec exception at SetTemperature")  
    return True

def GetlibVersion():
    __major = c_uint()
    __minor = c_uint()
    __ret = c_int()
    __ret = __libIntec.__libIntec_GetlibVersion(byref(__major), byref(__minor))
    if __ret is not 0:
        raise Exception("libIntec exception at GetlibVersion")
    return {"major":__major.value, "minor":__minor.value}

if __name__=="__main__":
    try:
        import time
        ver = GetlibVersion()
        print(f"libIntec Versrion {ver['major']}.{ver['minor']}")
        Initialize()
        InitializeCard(0)
        set_temp = 25 
        SetTemperature(0, 0, set_temp)
        temp = GetTemperature(0, 0)
        print(temp["temperature"])
        while temp["temperature"] < set_temp - 0.5 or temp["temperature"]  > set_temp + 0.5:
            temp = GetTemperature(0, 0)
            print(temp["temperature"])
            time.sleep(1)
        Exit()
    except Exception as e:
        Exit()

