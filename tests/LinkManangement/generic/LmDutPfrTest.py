TEST = True

from LmDutCorerTest import LmDutCorerTest

class LmDutPfrTest(LmDutCorerTest):
	
	stress_type = "pfr"

	def perform_stress(self, dut, lp):
		try: 
			dut.Reset(self.stress_type)
		except Exception as e:
			raise e


if __name__=="__main__":
	LmDutPfrTest()

