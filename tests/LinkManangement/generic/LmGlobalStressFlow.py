
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
        #TODO: print PF pair info
    	self.perform_stress(dut, lp)
