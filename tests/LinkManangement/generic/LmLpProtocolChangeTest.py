TEST = True

from LmProtcolChangeStressFlow import LmProtcolChangeStressFlow

class LmLpProtocolChangeTest(LmProtcolChangeStressFlow):
	
	stress_type = "protocol_change_lp"


if __name__=="__main__":
	LmLpProtocolChangeTest()
