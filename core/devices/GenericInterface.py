
#--------------------------------------------
# @author Shady Ganem <shady.ganem@intel.com>
#--------------------------------------------

from abc import ABCMeta, abstractmethod

class GenericInterface(ABCMeta):
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

	@abstractmethod
	def info(self):
		pass

	# TODO add abstract method for each method that is used in the tests
	# need to have a unified interface for all devices 
	@abstractmethod
	def EthStartTx(self, packet_size = 512, number_of_packets = None):
		pass

	@abstractmethod
	def EthStartRx(self):
		pass

	@abstractmethod
	def EthStartTraffic(self, packet_size = 512, number_of_packets = None):
		pass

	@abstractmethod
	def EthStopRx(self, ring_id=0):
		pass

	@abstractmethod
	def EthStopTx(self, ring_id=0):
		pass

	@abstractmethod
	def EthStopTraffic(self):
		pass

	@abstractmethod	
	def Clear_register(self, register_name, mul=0x8):
		pass

	@abstractmethod	
	def GetPRC(self):
		pass

	@abstractmethod	
	def GetPTC(self):
		pass

	@abstractmethod	
	def read_register(self, register_name, mul = 0x8, size = 0xffffffff):
		pass

	@abstractmethod	
	def ClearMACstat(self):
		pass

	@abstractmethod	
	def GetCurrentThroughput(self, packet_size=512):
		pass
	
	@abstractmethod	
	def RestartAn(self, Location = "Ext_Phy"): 
		pass
		# def RestartAn(self, Location = "AQ"):cvl

	@abstractmethod	
	def Reset(self, reset_type = 'pfr'):
		pass
	# def GetMacLinkStatus(self, *bits,**options):fvl
	# def GetMacLinkStatus(self, Location = "AQ"): cvl+cpk