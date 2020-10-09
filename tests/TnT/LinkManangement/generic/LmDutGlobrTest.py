
TEST = True

from LmGeneralStressFlow import LmGeneralStressFlow

class LmDutGlobrTest(LmGeneralStressFlow):
	
	stress_type = "globr"


	def perform_stress(self, dut, lp):
		try: 
			dut.Reset('globr')
		except Exception as e:
			raise e

if __name__=="__main__":
	LmDutGlobrTest()
