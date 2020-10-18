
from LmStressFlow import LmStressFlow
import thread

class LmLocalStressFlow(LmStressFlow):

    def do_traffic_before_stress(self, dut = None, lp = None):
        self.log.info("starting traffic before stress")
        self.run_traffic(dut, lp, 10)

    def do_traffic_after_stress(self, dut = None, lp = None):
        self.log.info("starting traffic after stress")
        number_of_packets = self.args('number_of_packets', 1000)
        packet_size = self.args('packet_size', 512)
        self.run_traffic(dut, lp, 10)

    def do_stress(self, dut, lp):
        self.log.info("performing global stress")
    	self.perform_stress(dut, lp)

    def run_stress_flow(self):
        for dut, lp in self.dut_lp_pairs:
            common_phy_types = self.get_common_protocols(dut, lp)
            self.log.info("Common Phy Types are:")
            for phy_type in common_phy_types:
                self.log.info(phy_type)
            if self.phy_type in common_phy_types:
                for fec in dut.fec_dict[self.phy_type]:
                    if self.configure_link(dut, lp,self.phy_type, fec):
                        self.do_traffic_before_stress(dut ,lp)
                        for i in range(self.stress_quantity):
                            self.log.info("stress iteration {}".format(i))
                            self.do_stress(dut, lp)
                        self.do_traffic_after_stress(dut, lp)
                        self.assert_link_status(dut, lp)
                    else:
                        self.set_test_status("fail")
                        self.append_fail_reason("Fail to configure link of {} ".format(self.phy_type))
            else:
                self.set_test_status("fail")
                self.append_fail_reason("iteration {} - {} is not in common PHY types".format(self.test_iteration, self.phy_type))