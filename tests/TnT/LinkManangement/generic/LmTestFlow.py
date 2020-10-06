import time

from GenericLinkManagement import GenericLinkManagement

from core.utilities.Timer import Timer

class LmTestFlow(GenericLinkManagement):

	def run(self):
		

		run_time = 6
		timer = Timer(run_time)
		timer.start()
		while not timer.expired():
			self.do_traffic_before_stress()
			self.perform_stress()
			self.do_traffic_after_stress()



