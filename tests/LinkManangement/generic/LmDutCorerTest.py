
TEST = True

from LmLocalStressFlow import LmLocalStressFlow

class LmDutCorerTest(LmLocalStressFlow):

	stress_type = "corer"
	link_config_persistency = True

	def perform_stress(self, dut, lp):
		try: 
			dut.Reset(self.stress_type)
		except Exception as e:
			raise e
