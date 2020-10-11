
from LmGeneralStressFlow import LmGeneralStressFlow

class LmDutEmprTest(LmGeneralStressFlow):
	
	stress_type = "empr"

	def perform_stress(self, dut, lp):
		try: 
			dut.Reset('corer')
		except Exception as e:
			raise e

if __name__=="__main__":
	LmDutEmprTest()
