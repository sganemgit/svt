TEST = True

from LmProtcolChangeStressFlow import LmProtcolChangeStressFlow

class LmDutProtocolChangeTest(LmProtcolChangeStressFlow):
	
	stress_type = "protocol_change_dut"

	def perform_stress(self, dut, lp):
		try: 
			dut.Reset(self.stress_type)
		except Exception as e:
			raise e


