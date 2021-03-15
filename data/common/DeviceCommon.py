
from devices.common.IEEE_802_3.IEEE_802_3 import IEEE_802_3 
from devices.common.PCIe.PCIe import PCIe
from devices.common.SFF.SFF import SFF

class DeviceCommon(IEEE_802_3, PCIe, SFF):
	pass
