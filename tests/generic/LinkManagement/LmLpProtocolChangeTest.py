
TEST = True

from LmProtcolChangeStressFlow import LmProtcolChangeStressFlow

class LmLpProtocolChangeTest(LmProtcolChangeStressFlow):
	        
	stress_type = "ProtocolChangeLp"

	def perform_stress(self, dut, lp):
		try: 
			self.configure_link(lp, dut, self.test_phy_type, self.test_fec_type)
		except Exception as e:
			raise e