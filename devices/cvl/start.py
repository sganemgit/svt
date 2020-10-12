#!/usr/bin/python -i
#--------------------------------------------
# @author Shady Ganem <shady.ganem@intel.com>
#--------------------------------------------

import sys
import time
import argparse
from cvl import cvl 
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
cvl1 = cvl(0,0,'ladh1234')
		  ''')

parser = argparse.ArgumentParser()

parser.add_argument('-a', '--auto' , help="try to create devices automatically", action="store_true")
parser.add_argument('-s', '--setup' , help="path to setup file")
parser.add_argument('-r', '--remote', help="hostame or ip of a remote device")
args = parser.parse_args()

if args.auto:
    if args.remote:
        devices = get_detected_devices("cvl", args.remote)
    else:
        devices = get_detected_devices("cvl")

    if devices:
        for device,info in devices.items():
            globals()[device] = cvl(info['device_number'],info['port_number'])
if args.setup:
	print("currently not available")
else:
	help()
#
#for device in devices.keys():
#    print "reseting link on port {}".format(globals()[device].port_number)
#    globals()[device].RestartAn()
#    time.sleep(0.2)
