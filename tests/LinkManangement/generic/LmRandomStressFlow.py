
from LmLocalStressFlow import LmLocalStressFlow
from LmGlobalStressFlow import LmGlobalStressFlow 
from LmProtcolChangeStressFlow import LmProtcolChangeStressFlow

class LmRandomStressFlow(LmLocalStressFlow, LmGlobalStressFlow, LmProtcolChangeStressFlow):

	def run(self):
		pass
