
TEST = True

from LmLocalStressFlow import LmLocalStressFlow

class LmDutCorerTest(LmLocalStressFlow):

	stress_type = "corer"

	def perform_stress(self, dut, lp):
		try: 
			dut.Reset(self.stress_type)
		except Exception as e:
			raise e
