from core.drivers.svdriver.SvDriverCommands import *
from core.utilities.colors import colors
from cvl.cvl import cvl
import time

def run_traffic(dut, lp, traffic_time):
    print
    print "running traffic for {} seconds".format(traffic_time)
    dut.EthStartRx()
    lp.EthStartTx()
    dut.EthStartTx()
    lp.EthStartRx()
    time.sleep(traffic_time)
    dut.EthStopTx()
    lp.EthStopTx()
    dut.EthStopRx()
    lp.EthStopRx()
    print
    check_traffic(dut, lp)

def check_traffic(dut, lp):
    pass

def poll_for_link(dut, lp, timeout):
    end_time = time.time() + timeout
    while time.time() < end_time:
        dut_link = dut.GetMacLinkStatus()
        lp_link = lp.GetMacLinkStatus()
        if dut_link == 1  and lp_link == 1:
            print "link is up on dut port {}".format(dut.port_number)
            print "link is up on lp port {}".format(lp.port_number)
            return True
    print "link is down on dut port {} and lp port {}".format(dut.port_number,lp.port_number)

def get_common_protocols(dut,lp):
    try:
        dut_phy_types = dut.GetPhyTypeAbilities(1)
        lp_phy_types = lp.GetPhyTypeAbilities(1)
        return list(set(dut_phy_types).intersection(lp_phy_types))
    except Exception as e:
        print "Exception {} raised in {}".format(str(e), get_cmmmon_protocols.__name__)
        raise e

def reset_both_sides(dut,lp,reset):
    print "performing {} reset on lp".format(reset)
    lp.Reset(reset)
    print "performing {} reset on dut".format(reset)
    dut.Reset(reset)

def configure_link(dut,lp,PhyType,FecType):
    link_configuratio_status_flag = True
    if PhyType in cvl.force_phy_types_list:
        print colors.Red("{} does not support AN".format(colors.Green(PhyType)))
        print "setting dut to {} with fec {}".format(colors.Green(PhyType), colors.Orange(FecType))
        dut.SetPhyConfiguration(PhyType,FecType)
        print "setting lp to {} with fec {}".format(colors.Green(PhyType), colors.Orange(FecType))
        lp.SetPhyConfiguration(PhyType,FecType)
    else:
        print "setting dut to {} with fec {}".format(colors.Green(PhyType), colors.Orange(FecType))
        dut.SetPhyConfiguration(PhyType,FecType)
    time.sleep(3)

    current_dut_phy_type = dut.GetPhyType()
    current_lp_phy_type = lp.GetPhyType()

    if current_dut_phy_type != PhyType:
        print colors.Red("DUT Phy Type is {} Expected to be {}".format(current_dut_phy_type, PhyType))
        link_configuratio_status_flag = False
    if current_lp_phy_type != PhyType:
        print colors.Red("LP Phy Type is {} Expected to be {}".format(current_lp_phy_type, PhyType))
        link_configuratio_status_flag = False

    current_dut_fec = dut.GetCurrentFECStatus()
    current_lp_fec = lp.GetCurrentFECStatus()

    if current_dut_fec != FecType:
        print colors.Red("DUT FEC is {} Expected to be {}".format(current_dut_fec,FecType))
        link_configuratio_status_flag = False
    if current_lp_fec != FecType:
        print colors.Red("LP FEC is {} Expected to be {}".format(current_lp_fec, FecType))
        link_configuratio_status_flag = False

    return link_configuratio_status_flag

def run():
    print svdt('-s')
    print svdt('-v')
    print svdt('-f')
    devices = get_detected_devices("cvl")
    connected_pairs = detect_connected_devices()
    pairs = list()
    for pair in connected_pairs:
       DutLpPair = dict()
       lpinfo = devices[pair['first']]
       dutinfo = devices[pair['second']]
       DutLpPair['lp'] = cvl(lpinfo['device_number'], lpinfo['port_number'])
       DutLpPair['dut'] = cvl(dutinfo['device_number'], dutinfo['port_number'])
       pairs.append(DutLpPair)

    for index, pair in enumerate(pairs):
        print "perfoming globar on pair {}".format(index)
        reset_both_sides(pair['dut'],pair['lp'],'globr')

    for index , pair in enumerate(pairs):
        dut = pair['dut']
        lp = pair['lp']
        if poll_for_link(dut,lp,15):
            run_traffic(dut,lp,10)
        common_protocol_list = get_common_protocols(dut,lp) 
        print "the common protocols are:"
        for protocol in common_protocol_list:
            print protocol
        print
        for protocol in common_protocol_list:
            print '------------------------------------------------------------'
            print "                      {}".format(colors.Green(protocol))
            if protocol in cvl.fec_dict:
                for fec in cvl.fec_dict[protocol]:
                    print "{}:".format(colors.Orange(fec))
                    config_status = configure_link(dut, lp, protocol, fec)
                    if config_status and poll_for_link(dut,lp,15):
                        run_traffic(dut,lp,10)
                    else:
                        print "link is not configured"

            reset_both_sides(dut,lp,'globr')
            print '------------------------------------------------------------'
            print


if __name__=="__main__":
    run()
