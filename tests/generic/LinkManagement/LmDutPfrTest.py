TEST = True

from LmLocalStressFlow import LmLocalStressFlow

class LmDutPfrTest(LmLocalStressFlow):
	
	stress_type = "pfr"
	link_config_persistency = True

	def perform_stress(self, dut, lp):
		try: 
			dut.Reset(self.stress_type)
		except Exception as e:
			raise e



