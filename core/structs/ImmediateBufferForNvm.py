
class ImmediateBufferForNvm:
	'''
		field_id = bytes 0-1
		field_flags = bytes 2-3
		field_value = bytes 4-5
	'''
	def __init__(self):
		self.field_id = 0
		self.field_flags = 0
		self.field_value = 0