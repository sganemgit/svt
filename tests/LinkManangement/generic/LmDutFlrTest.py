
TEST = True

from LmDutCorerTest import LmDutCorerTest

class LmDutFlrTest(LmDutCorerTest):
	
	stress_type = "flr"

	def perform_stress(self, dut, lp):
		try: 
			dut.Reset(self.stress_type)
		except Exception as e:
			raise e

