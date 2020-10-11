TEST = True

from LmDutCorerTest import LmDutCorerTest

class LmDutPfrTest(LmDutCorerTest):
	
	stress_type = "pfr"


if __name__=="__main__":
	LmDutPfrTest()

