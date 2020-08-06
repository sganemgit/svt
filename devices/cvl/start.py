from cvl import cvl 
import sys
import time
from core.drivers.svdriver.SvDriverCommands import *
try:
    import readline
except ImportError:
    print("Module readline not available.")
else:
    import rlcompleter
    readline.parse_and_bind("tab: complete")

devices = get_detected_devices("cvl")
if devices:
    for device,info in devices.iteritems():
        globals()[device] = cvl(info['device_number'],info['port_number'])

if __name__=="__main__":
    pass
#    MacloopbackWithLP()


cvlr = cvl(0,0,"ladh444")
