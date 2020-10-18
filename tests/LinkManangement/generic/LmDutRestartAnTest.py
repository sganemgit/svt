TEST = True

from LmLocalStressFlow import LmLocalStressFlow

class LmDutRestartAnTest(LmLocalStressFlow):
	
	stress_type = "RestartAN"
	link_config_persistency = True

	def perform_stress(self, dut, lp):
		try:
			dut.RestartAn()
		except Exception as e:
			raise e





