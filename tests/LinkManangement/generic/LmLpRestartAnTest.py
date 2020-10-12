
TEST = True

from LmDutCorerTest import LmDutCorerTest

class LmLpRestartAnTest(LmDutCorerTest):
	
	stress_type = "restart_an_lp"

	def perform_stress(self, dut, lp):
		try: 
			dut.Reset(self.stress_type)
		except Exception as e:
			raise e