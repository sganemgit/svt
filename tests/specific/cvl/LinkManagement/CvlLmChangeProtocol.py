from core.drivers.svdriver.SvDriverCommands import *
from core.utilities.colors import colors
from core.devices.DeviceFactory import DeviceFactory
from core.tests.testBase import testBase
import time
from core.utilities.Timer import Timer

class LmChangeProtocol(testBase):

    def run_traffic(self, dut, lp, traffic_time):
        log = self.log
        log.info()
        log.info("running traffic for {} seconds".format(traffic_time))
        dut.EthStartRx()
        lp.EthStartRx()
        lp.EthStartTx()
        dut.EthStartTx()
        time.sleep(traffic_time)
        dut.EthStopTx()
        lp.EthStopTx()
        dut.EthStopRx()
        lp.EthStopRx()
        log.info()
        self.check_traffic(dut, lp)
        self.check_mac_counters(dut, lp)

    def check_mac_counters(self, dut,lp):
        log = self.log
        dut_coutners = dut.GetMacCounters()
        log.info("DUT MAC Counters:")
        for key, value in dut_coutners.iteritems():
            log.info("{} = {}".format(key,value))
        lp_counters = lp.GetMacCounters()
        log.info("LP MAC Counters:")
        for key, value in lp_counters.iteritems():
            log.info("{} = {}".format(key,value))

        if dut_coutners['CRCERRS'] > 0:
            log.warning("{} CRC on DUT".format(dut_coutners['CRCERRS']))
            self.append_fail_reason("{} CRC on DUT".format(dut_coutners['CRCERRS']))

    def check_traffic(self, dut, lp):
        log = self.log
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
            log.warning("missed packets on LP")
            self.append_fail_reason("missed packets on LP")

        if lp_PTC['TotalPTC'] != dut_PRC['TotalPRC']:
            log.info("missed packets on DUT")
            self.append_fail_reason("missed packets on DUT")

    def poll_for_link(self, dut, lp, timeout):
        log = self.log
        start_time = time.time()
        end_time = time.time() + timeout
        while time.time() < end_time:
            dut_link = dut.GetMacLinkStatus()
            lp_link = lp.GetMacLinkStatus()
            if dut_link == 1  and lp_link == 1:
                log.info("link is up on dut port {}".format(dut.port_number))
                log.info("link is up on lp port {}".format(lp.port_number))
                log.info("TTL = {}".format(time.time() - start_time))
                return True
        log.info("link is down on dut port {} and lp port {}".format(dut.port_number,lp.port_number),'r')
        self.append_fail_reason("link is down on dut port {} and lp port {}".format(dut.port_number,lp.port_number))
        return False

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
        self.poll_for_link(dut, lp, 15)

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
            lp.DisableFECRequests(0)
            log.info("setting dut to {} with fec {}".format(colors.Green(PhyType), colors.Orange(FecType)))
            dut.SetPhyConfiguration(PhyType,FecType)

        if self.poll_for_link(dut, lp , 15):
            time.sleep(3)
            current_dut_phy_type = dut.GetPhyType()
            current_lp_phy_type = lp.GetPhyType()

            if current_dut_phy_type != PhyType:
                log.info(colors.Red("DUT Phy Type is {} Expected to be {}".format(current_dut_phy_type, PhyType)))
                self.append_fail_reason("DUT Phy Type is {} Expected to be {}".format(current_dut_phy_type, PhyType))
                link_configuratio_status_flag = False
            if current_lp_phy_type != PhyType:
                log.info(colors.Red("LP Phy Type is {} Expected to be {}".format(current_lp_phy_type, PhyType)))
                self.append_fail_reason("DUT Phy Type is {} Expected to be {}".format(current_dut_phy_type, PhyType))
                link_configuratio_status_flag = False

            current_dut_fec = dut.GetCurrentFECStatus()
            current_lp_fec = lp.GetCurrentFECStatus()

            if current_dut_fec != FecType:
                log.info(colors.Red("DUT FEC is {} Expected to be {}".format(current_dut_fec,FecType)))
                self.append_fail_reason("DUT FEC is {} Expected to be {}".format(current_dut_fec,FecType))
                link_configuratio_status_flag = False
            if current_lp_fec != FecType:
                log.info(colors.Red("LP FEC is {} Expected to be {}".format(current_lp_fec, FecType)))
                self.append_fail_reason("LP FEC is {} Expected to be {}".format(current_lp_fec, FecType))
                link_configuratio_status_flag = False
        else:
            link_configuratio_status_flag = False
        return link_configuratio_status_flag

    def run(self):
        log = self.log
        args = self.user_args
        pairs = self.pairs
        run_time = args.get('run_time')
        target_protocol = args.get('protocol','invalid protocol')
        target_fec = args.get('fec')
        traffic_time = int(args.get('traffic_time', 60))
        log.info("target protocol: {}".format(target_protocol))
        log.info("target FEC: {}".format(target_fec))

        log.info("traffic time {}".format(traffic_time))

        test_run_time = time.time() + round(float(run_time)*3600)

        log.info("run time in hours {}".format(run_time))
        log.info("run time in minutes {}".format(float(run_time)*60))

        for device_id, device in self.devices.iteritems():
            log.info("performing globr reset on {} ".format(device_id))
            device.Reset('globr')
        timer = Timer(test_run_time)
        timer.start()
        while not timer.expired():
            log.info("                      iteration #{}".format(self.test_iteration),'g')
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
                        log.info( "                      {}".format(protocol), 'g')
                        for fec in lp.fec_dict[protocol]:
                            log.info("configuting Phy to {}".format(target_protocol), 'g')
                            config_status = self.configure_link(dut,lp,target_protocol,target_fec)
                            if config_status :
                                log.info("{}:".format(colors.Orange(fec)))
                                config_status = self.configure_link(dut, lp, protocol, fec)
                            if config_status :
                                self.run_traffic(dut,lp,traffic_time)
                            else:
                                log.info("link is not configured")
                        self.reset_both_sides(dut,lp,'globr')
                        log.info('------------------------------------------------------------')
                        log.info()
                else:
                    log.info(colors.Red("protocol {} is not a common protocol between the DUT and LP".format(target_protocol)))
            self.test_iteration += 1

if __name__ == '__main__':
    LmChangeProtocol()
