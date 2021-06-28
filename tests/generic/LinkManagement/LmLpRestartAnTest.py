
TEST = True

from LmLocalStressFlow import LmLocalStressFlow

class LmLpRestartAnTest(LmLocalStressFlow):
	
	stress_type = "RestartAN"
	link_config_persistency = True

	def perform_stress(self, dut, lp):
		try:
			lp.RestartAn()
		except Exception as e:
			raise e