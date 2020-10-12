
#--------------------------------------------
# @author Shady Ganem <shady.ganem@intel.com>
#--------------------------------------------

from abc import ABC, abstractmethod

class GenericInterface(ABC):
	'''
		GenericInterface defines a common interface for all device. methods that are declared under GenericInterface must be 
		implemented under all inherting classes
		GenericInterface does not define a constructor nor does defice any fucntionality. 
		GenericInterface acts as a template for other classes that need to aline to a unifore interface.
	'''

	@abstractmethod
	def Reset(self, reset_type):
		pass

	@abstractmethod
	def SetPhyConfiguration(self, phytype, fec, debug = False):
		pass



	# TODO add abstract method for each method that is used in the tests
	# need to have a unified interface for all devices 
	# @abstractmethod
	# def EthStartTx(self, ):
	# 	pass