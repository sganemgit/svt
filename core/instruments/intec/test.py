#!/usr/bin/python3 

import inspect 
import libIntec.libIntec as intec
from libIntec.libIntec import *

import sys

if __name__=="__main__":
    import time
    print(GetlibVersion())
    Initialize()
    InitializeCard(0)
    try:
        set_temp = float(sys.argv[1])
        print(set_temp)
    except:
        set_temp = 25
    SetTemperature(0, 0, set_temp)
    temp = GetTemperature(0, 0)

    print(temp)
    while temp < set_temp - 0.5 or temp  > set_temp + 0.5:
        temp = GetTemperature(0, 0)
        print(temp)
        time.sleep(1)
    Exit()

