
TEST = True

from LmGlobalStressFlow import LmGlobalStressFlow

class LmDutGlobrTest(LmGlobalStressFlow):
	
	stress_type = "globr"
	link_config_persistency = False

	def perform_stress(self, dut, lp):
		try: 
			self.log.info("")
			self.log.info("performing {} reset on DUT".format(self.stress_type))
			dut.Reset(self.stress_type)
		except Exception as e:
			raise e

