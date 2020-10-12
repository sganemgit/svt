

# @author Shady Ganem <shady.ganem@intel.com>

from core.tests.testBase import testBase 
import time 
import random 

class GenericLinkManagement(testBase):
    
    def get_random_number_of_packets(self):
        max_value = self.args.get('max_number_of_packet', 10000000)
        min_value = self.args.get('min_number_of_packet', 1000000)
        return random.randint(min_value, max_value)

    def get_random_packet_size(self):
        max_value = self.args.get('max_packet_size', 1522)
        min_value = self.args.get('min_packet_size', 64)
        return random.randint(min_value, max_value)

    def _run_traffic_by_number_of_packets(self, dut ,lp , **kwargs):
        ring_id = kwargs.get('ring_id', 0)
        packet_size=  kwargs.get('packet_size', 512)
        number_of_packets = kwargs.get('number_of_packets', 10000)
        print(number_of_packets)
        dut.EthStartRx()
        lp.EthStartRx()
        lp.EthStartTx(packet_size, number_of_packets)
        dut.EthStartTx(packet_size, number_of_packets)
        while not (dut.driver.is_ring_done(ring_id) and lp.driver.is_ring_done(ring_id)):
            time.sleep(0.01)
        dut.EthStopTx(ring_id)
        lp.EthStopTx(ring_id)
        dut.EthStopRx(ring_id)
        lp.EthStopRx(ring_id)

    def _run_traffic_by_traffic_time(self, **kwargs):
        ring_id = kwargs.get('ring_id', 0)
        traffic_time= kwargs.get('traffic_time', 0)
        dut.EthStartRx()
        lp.EthStartRx()
        lp.EthStartTx()
        dut.EthStartTx()
        time.sleep(traffic_time)
        dut.EthStopTx()
        lp.EthStopTx()
        dut.EthStopRx()
        lp.EthStopRx()

    def run_traffic(self, dut, lp, **kwargs):
        log = self.log
        log.info()
        ring_id= kwargs.get('ring_id', 0)
        packet_size= kwargs.get('packet_size', 512)
        number_of_packets=kwargs.get('number_of_packets', 10000)
        if 'traffic_time' in kwargs:
            log.info("running traffic for {} seconds".format(kwargs['traffic_time'] ))
            self._run_traffic_by_traffic_time(dut, lp, ring_id=ring_id, traffic_time=kwargs['traffic_time'])
        else:
            log.info("running traffic: packet size = {} and number of packets = {}".format(packet_size, number_of_packets))
            self._run_traffic_by_number_of_packets(dut, lp, ring_id=ring_id, packet_size=packet_size, number_of_packets=number_of_packets)
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

    def configure_link(self, dut, lp, PhyType, FecType):
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

