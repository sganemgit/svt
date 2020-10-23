
TEST = True 

from LmGlobalStressFlow import LmGlobalStressFlow

class LmDutEmprTest(LmGlobalStressFlow):
	
	stress_type = "empr"
	link_config_persistency = False

	def perform_stress(self, dut, lp):
		try: 
			dut.Reset(self.stress_type)
		except Exception as e:
			raise e

