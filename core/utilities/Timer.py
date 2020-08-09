import time
from core.exceptions.Exceptions import *

class Timer:
	"""this is a timer class for perfoming time measurements"""
	def __init__(self, duration):
		self._end_time = 0
		self._duration = duration
		self._set_flag = True

	def set_for(self, duration):
		self._duration = duration
		self._set_flag = True

	def reset(self):
		self._end_time = 0
		self._duration = 0
		self._set_flag = False

	def start(self):
		self._end_time = time.time() + self._duration 

	def expired(self):
		if self._set_flag:
			if time.time() < self._end_time:
				return False
			else:
				return True
		else:
			raise TimerError("timer is not set")