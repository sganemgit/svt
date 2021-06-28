
from LmStressFlow import LmStressFlow

class LmGlobalStressFlow(LmStressFlow):

    def do_traffic_before_stress(self, dut, lp):
        self.number_of_packets = int(self.args.get('number_of_packets', self.get_random_number_of_packets()))
        self.packet_size = int(self.args.get('packet_size', self.get_random_packet_size()))
        self.log.info("starting traffic before stress")
        self.log.info("running traffic on dut port {}".format(dut.port_number))
        self.log.info("running traffic on lp port {}".format(lp.port_number))
        self.run_traffic(dut, lp, number_of_packets=self.number_of_packets, packet_size=self.packet_size)

    def do_traffic_after_stress(self, dut, lp):
        self.log.info("starting traffic after stress")
        self.log.info("running traffic on dut port {}".format(dut.port_number))
        self.log.info("running traffic on lp port {}".format(lp.port_number))
        self.run_traffic(dut, lp, number_of_packets=self.number_of_packets, packet_size=self.packet_size)

    def do_stress(self, dut, lp):
        self.log.info("performing global stress")
        self.log.info("performing global stress on dut port {}".format(dut.port_number))
        self.log.info("performing global stress on lp port {}".format(lp.port_number))
        self.perform_stress(dut, lp)

    def run_stress_flow(self):
        for dut, lp in self.dut_lp_pairs:
            common_phy_types = self.get_common_protocols(dut, lp)
            self.log.info("Common Phy Types are:")
            for phy_type in common_phy_types:
                self.log.info(phy_type)
            if self.phy_type in common_phy_types:
                for fec in dut.fec_dict[self.phy_type]:
                    self.configure_link(dut, lp, self.phy_type, fec)
                    if self.assert_link_status(dut, lp, self.phy_type, fec):
                        self.do_traffic_before_stress(dut ,lp)
                        for i in range(self.stress_quantity):
                            self.log.info("stress iteration {}".format(i))
                            self.do_stress(dut, lp)
                        if not self.link_config_persistency:
                            self.log.info("Setting link after stress")
                            self.configure_link(dut, lp, self.phy_type, fec)
                            self.assert_link_status(dut, lp, self.phy_type, fec)
                        self.do_traffic_after_stress(dut, lp)
                        if not self.assert_link_status(dut, lp, self.phy_type, fec):
                            self.set_test_status("fail")
                            self.append_fail_reason("Link not configured correctly after stress traffic ")
                    else:
                        self.set_test_status("fail")
                        self.append_fail_reason("Fail to configure link of {} ".format(self.phy_type))
            else:
                self.set_test_status("fail")
                self.append_fail_reason("iteration {} - {} is not in common PHY types".format(self.test_iteration, self.phy_type))
