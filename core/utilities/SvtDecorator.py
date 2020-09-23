
import time

def timer(function):
	def wrapper(*args, **kwargs):
		start_time = time.time()
		result = function(*args, **kwargs)
		print("{} executed in {}".format(function.__name__, time.time() - start_time))
		return result
	return wrapper