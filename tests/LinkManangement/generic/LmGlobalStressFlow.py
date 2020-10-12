
from LmStressFlow import LmStressFlow

class LmGlobalStressFlow(LmStressFlow):

    def do_traffic_before_stress(self, dut = None, lp = None):
        self.log.info("starting traffic before stress")
        #TODO: print PF pair info
        self.run_traffic(dut, lp, number_of_packets=self.number_of_packets, packet_size=self.packet_size)

    def do_traffic_after_stress(self, dut = None, lp = None):
        self.log.info("starting traffic after stress")
        #TODO: print PF pair info
        self.run_traffic(dut, lp, number_of_packets=self.number_of_packets, packet_size=self.packet_size)

    def do_stress(self, dut, lp):
        self.log.info("performing global stress")
        #TODO: print which pf are under stress
    	self.perform_stress(dut, lp)

    def run_stress_flow(self):
        # we need to configure the to the test phy type
        for dut, lp in self.dut_lp_pairs:
            self.do_traffic_before_stress(dut ,lp)
            for i in range(self.stress_quantity):
                self.log.info("stress iteration {}".format(i))
                self.do_stress(dut, lp)
            self.do_traffic_after_stress(dut, lp)
        
