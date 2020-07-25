from core.drivers.svdriver.SvDriverCommands import *
from cvl.cvl import cvl
def run():
    connected_pairs = detect_connected_devices()
    devices = get_detected_devices("cvl")
    pairs = list()
    for pair in connected_pairs:
       DutLpPair = dict()
       lpinfo = devices[pair['first']]
       dutinfo = devices[pair['second']]
       DutLpPair['lp'] = cvl(lpinfo['device_number'], lpinfo['port_number'])
       DutLpPair['dut'] = cvl(dutinfo['device_number'], dutinfo['port_number'])
       pairs.append(DutLpPair)

    for pair in pairs:
        print "perfoming globar on all pfs"
        pair['lp'].Reset('globr')
        pair['dut'].Reset('globr')


if __name__=="__main__":
    run()
