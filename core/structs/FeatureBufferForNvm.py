

class FeatureBufferForNvm:
	'''
		feature_id: bytes 0-1
		feature_flags : bytes 2-3
		feature_selection : bytes 4-5
	'''
	def __init__(self):
		self.feature_id = 0 
		self.feature_flags = 0
		self.feature_selection = 0