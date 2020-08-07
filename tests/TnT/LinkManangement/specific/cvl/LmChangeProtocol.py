from core.drivers.svdriver.SvDriverCommands import *
from core.utilities.colors import colors
from core.devices.DeviceFactory import DeviceFactory
from core.tests.testBase import testBase
import time

class LmChangeProtocol(testBase):

    def run_traffic(self, dut, lp, traffic_time):
        log = self.log
        log.info()
        log.info("running traffic for {} seconds".format(traffic_time))
        dut.EthStartRx()
        lp.EthStartTx()
        dut.EthStartTx()
        lp.EthStartRx()
        time.sleep(traffic_time)
        dut.EthStopTx()
        lp.EthStopTx()
        dut.EthStopRx()
        lp.EthStopRx()
        log.info()
        self.check_traffic(dut, lp)

    def check_traffic(self, dut, lp):
        dut_PTC = dut.GetPTC()
        log.info("DUT MAC transmitted packets counters")
        for key, value in dut_PTC.iteritems():
            log.info("{} = {}".format(key,value))
        log.info("LP MAC received packets counters")
        lp_PRC = lp.GetPRC()
        for key, value in lp_PRC.iteritems():
            log.info("{} = {}".format(key,value))
        log.info("LP MAC transmitted packet counters")
        lp_PTC = lp.GetPTC()
        for key,value in lp_PTC.iteritems():
            log.info("{} = {}".format(key, value))
        log.info("DUT MAC received packets counters")
        dut_PRC = dut.GetPRC()
        for key,value in dut_PRC.iteritems():
            log.info("{} = {}".format(key, value))

        if dut_PTC['TotalPTC'] != lp_PRC['TotalPRC']:
            log.info(colors.Red("missed packets on LP"))

        if lp_PTC['TotalPTC'] != dut_PRC['TotalPRC']:
            log.info(colors.Red("missed packets on DUT"))

    def poll_for_link(self, dut, lp, timeout):
        log = self.log
        end_time = time.time() + timeout
        while time.time() < end_time:
            dut_link = dut.GetMacLinkStatus()
            lp_link = lp.GetMacLinkStatus()
            if dut_link == 1  and lp_link == 1:
                log.info("link is up on dut port {}".format(dut.port_number))
                log.info("link is up on lp port {}".format(lp.port_number))
                return True
        log.info("link is down on dut port {} and lp port {}".format(dut.port_number,lp.port_number))

    def get_common_protocols(self, dut,lp):
        log = self.log
        try:
            dut_phy_types = dut.GetPhyTypeAbilities(1)
            lp_phy_types = lp.GetPhyTypeAbilities(1)
            return list(set(dut_phy_types).intersection(lp_phy_types))
        except Exception as e:
            log.info("Exception {} raised in {}".format(str(e), get_cmmmon_protocols.__name__))
            raise e

    def reset_both_sides(self, dut,lp,reset):
        log = self.log
        log.info("performing {} reset on lp".format(reset))
        lp.Reset(reset)
        log.info("performing {} reset on dut".format(reset))
        dut.Reset(reset)

    def configure_link(self, dut,lp,PhyType,FecType):
        log = self.log
        link_configuratio_status_flag = True
        if PhyType in dut.force_phy_types_list:
            log.info(colors.Red("{} does not support AN".format(colors.Green(PhyType))))
            log.info("setting dut to {} with fec {}".format(colors.Green(PhyType), colors.Orange(FecType)))
            dut.SetPhyConfiguration(PhyType,FecType)
            log.info("setting lp to {} with fec {}".format(colors.Green(PhyType), colors.Orange(FecType)))
            lp.SetPhyConfiguration(PhyType,FecType)
        else:
            log.info("setting dut to {} with fec {}".format(colors.Green(PhyType), colors.Orange(FecType)))
            dut.SetPhyConfiguration(PhyType,FecType)
        time.sleep(3)

        current_dut_phy_type = dut.GetPhyType()
        current_lp_phy_type = lp.GetPhyType()

        if current_dut_phy_type != PhyType:
            log.info(colors.Red("DUT Phy Type is {} Expected to be {}".format(current_dut_phy_type, PhyType)))
            link_configuratio_status_flag = False
        if current_lp_phy_type != PhyType:
            log.info(colors.Red("LP Phy Type is {} Expected to be {}".format(current_lp_phy_type, PhyType)))
            link_configuratio_status_flag = False

        current_dut_fec = dut.GetCurrentFECStatus()
        current_lp_fec = lp.GetCurrentFECStatus()

        if current_dut_fec != FecType:
            log.info(colors.Red("DUT FEC is {} Expected to be {}".format(current_dut_fec,FecType)))
            link_configuratio_status_flag = False
        if current_lp_fec != FecType:
            log.info(colors.Red("LP FEC is {} Expected to be {}".format(current_lp_fec, FecType)))
            link_configuratio_status_flag = False

        return link_configuratio_status_flag

    def run(self):
        log = self.log
        log.info(str(svdt('-s')))
        log.info(str(svdt('-v')))
        log.info(str(svdt('-f')))
        devices = get_detected_devices("cvl")
        connected_pairs = detect_connected_devices()
        pairs = list()
        for pair in connected_pairs:
           DutLpPair = dict()
           lpinfo = devices[pair['first']]
           dutinfo = devices[pair['second']]
           DutLpPair['lp']  = DeviceFactory.create_device(lpinfo['device_number'], lpinfo['port_number'])
           DutLpPair['dut'] = DeviceFactory.create_device(dutinfo['device_number'], dutinfo['port_number'])
           pairs.append(DutLpPair)

        for index, pair in enumerate(pairs):
            log.info("perfoming globar on pair {}".format(index))
            self.reset_both_sides(pair['dut'],pair['lp'],'globr')

        target_protocol = '25GBase-CR'
        target_fec = '25G_RS_544_FEC'
        #target_protocol = self.user_args['protocol']
        #target_fec = self.user_args['fec']
        log.info("this is a log message")
        for index , pair in enumerate(pairs):
            dut = pair['dut']
            lp = pair['lp']
            if self.poll_for_link(dut,lp,15):
                self.run_traffic(dut,lp,10)
            common_protocol_list = self.get_common_protocols(dut,lp)
            log.info("the common protocols are:")
            for protocol in common_protocol_list:
                log.info(protocol)
            log.info()
            if target_protocol in common_protocol_list:
                for protocol in common_protocol_list:
                    log.info('------------------------------------------------------------')
                    log.info( "                      {}".format(colors.Green(protocol)))
                    if protocol in lp.fec_dict:
                        for fec in lp.fec_dict[protocol]:
                            log.info("configuting Phy to {}".format(colors.Green(target_protocol)))
                            config_status = self.configure_link(dut,lp,target_protocol,target_fec)
                            if config_status and self.poll_for_link(dut, lp, 15):
                                log.info("{}:".format(colors.Orange(fec)))
                                config_status = self.configure_link(dut, lp, protocol, fec)
                            if config_status and self.poll_for_link(dut,lp,15):
                                self.run_traffic(dut,lp,10)
                            else:
                                log.info("link is not configured")
                    self.reset_both_sides(dut,lp,'globr')
                    log.info('------------------------------------------------------------')
                    log.info()
            else:
                log.info(colors.Red("protocol {} is not a common protocol between the DUT and LP".format(target_protocol)))

if __name__ == '__main__':
#    arg = dict()
#    arg['protocol'] = '25GBase-CR'
#    arg['fec'] = '25G_RS_544_FEC'
    LmChangeProtocol()
