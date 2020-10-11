

from LmLocalStressFlow import LmLocalStressFlow

class LmDutCorerTest(LmLocalStressFlow):

	stress_type = "corer"

	def perform_stress(self, dut, lp):
		try: 
			dut.Reset('corer')
		except Exception as e:
			raise e

if __name__=="__main__":
	LmDutCorerTest()