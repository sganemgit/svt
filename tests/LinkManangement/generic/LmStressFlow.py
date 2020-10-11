
import time
from GenericLinkManagement import GenericLinkManagement
from core.utilities.Timer import Timer


class LmStressFlow(GenericLinkManagement):


    def do_traffic_before_stress(self, dut = None, lp = None):
        print("starting traffic before stress")

    def do_traffic_after_stress(self, dut = None, lp = None):
        print("starting traffic after stress")

	def run(self):
		
		run_time = 6
		timer = Timer(run_time)
		timer.start()
		while not timer.expired():
			for dut, lp in self.pairs:
				self.do_traffic_before_stress(dut ,lp)
				self.perform_stress(dut, lp)
				self.do_traffic_after_stress(dut, lp)