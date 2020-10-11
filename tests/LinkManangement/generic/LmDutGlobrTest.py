
TEST = True

from LmGlobalStressFlow import LmGlobalStressFlow

class LmDutGlobrTest(LmGlobalStressFlow):
	
	stress_type = "globr"

	def perform_stress(self, dut, lp):
		try: 
			dut.Reset(self.stress_type)
		except Exception as e:
			raise e

if __name__=="__main__":
	LmDutGlobrTest()
