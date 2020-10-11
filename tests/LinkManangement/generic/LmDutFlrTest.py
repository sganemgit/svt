
TEST = True

from LmDutCorerTest import LmDutCorerTest

class LmDutFlrTest(LmDutCorerTest):
	
	stress_type = "flr"

	def perform_stress(self, dut, lp):
		try: 
			dut.Reset('corer')
		except Exception as e:
			raise e

if __name__=="__main__":
	LmDutFlrTest()
