
TEST = True

from LmProtcolChangeStressFlow import LmProtcolChangeStressFlow

class LmLpProtocolChangeTest(LmProtcolChangeStressFlow):
	
	stress_type = "protocol_change_lp"

	def perform_stress(self, dut, lp):
		try: 
			dut.Reset(self.stress_type)
		except Exception as e:
			raise e