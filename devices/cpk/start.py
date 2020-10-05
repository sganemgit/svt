#!/usr/bin/python -i
#--------------------------------------------
# @author Shady Ganem <shady.ganem@intel.com>
#--------------------------------------------

import sys
import time
import argparse
from cpk import cpk
from core.drivers.svdriver.SvDriverCommands import *
try:
    import readline
except ImportError:
    print("Module readline not available.")
else:
    import rlcompleter
    readline.parse_and_bind("tab: complete")

def help():
	print('''input params 
	@device number 
	@port nubmer
	@hostname - optional
	@driver type - optional
Example:
cpk1 = cpk(0,0,'ladh1234')
		  ''')

parser = argparse.ArgumentParser()

parser.add_argument('-a', '--auto' , help="try to create devices automatically", action="store_true")
parser.add_argument('-s', '--setup' , help="path to setup file")
args = parser.parse_args()

if args.auto:
    devices = get_detected_devices("cpk")
    if devices:
        for device,info in devices.items():
            globals()[device] = cpk(info['device_number'],info['port_number'])
if args.setup:
	print("currently not available")
else:
	help()

cpk_dut = cpk(0,0,'ladh1841')
cpk_lp  = cpk(0,0,'ladh1833')

