
# @author Shady Ganem <shady.ganem@intel.com>

class InstrumentFactory:

    @classmethod
    def CreateIntec(device_type):
        if instrument is None:
            return None
        from intec.InTEC import InTEC
        return InTEC(device_type)

