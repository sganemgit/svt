
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
            self.do_traffic_before_stress(dut ,lp)
            for i in range(self.stress_quantity):
                self.log.info("stress iteration {}".format(i))
                self.do_stress(dut, lp)
            self.do_traffic_after_stress(dut, lp)