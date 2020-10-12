
from LmLocalStressFlow import LmLocalStressFlow
from LmGeneralStressFlow import LmGeneralStressFlow
from LmProtcolChangeStressFlow import LmProtcolChangeStressFlow

class LmRandomStressFlow(LmLocalStressFlow, LmGeneralStressFlow, LmProtcolChangeStressFlow):

	def run(self):
		pass