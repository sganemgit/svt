
TEST = True

from LmProtcolChangeStressFlow import LmProtcolChangeStressFlow

class LmDutProtocolChangeTest(LmProtcolChangeStressFlow):
	
	stress_type = "protocolchangedut"

	def perform_stress(self, dut, lp):
		try: 
			self.configure_link(dut, lp, self.test_phy_type, self.test_fec_type)
		except Exception as e:
			raise e