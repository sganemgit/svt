TEST = True


from LmRandomStressFlow import LmRandomStressFlow

class LmRandomEventsCrossLfcTest(LmRandomStressFlow):
	
	stress_type = "random_events_cross_lfc"


if __name__=="__main__":
	LmRandomEventsCrossLfcTest()
