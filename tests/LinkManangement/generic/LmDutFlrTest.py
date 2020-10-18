
TEST = True

from LmLocalStressFlow import LmLocalStressFlow

class LmDutFlrTest(LmLocalStressFlow):
	
	stress_type = "flr"
	link_config_persistency = True

	def perform_stress(self, dut, lp):
		try: 
			dut.Reset(self.stress_type)
		except Exception as e:
			raise e

