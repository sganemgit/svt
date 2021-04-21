
# @author Shady Ganem <shady.ganem@intel.com>

class InstrumentFactory:

    @classmethod
    def CreateIntec(cls, device_type):
        index = 0
        if instrument is None:
            return None
        from intec.InTEC import InTEC
        return InTEC(index, device_type)

    @classmethod
    def create_instruments_from_setup(cls, instruments):
        try:
            instrument_dict = dict()
            for instrument, attrib in instruments.items():
                if attrib['name'] == 'intec':
                    from core.instruments.intec.InTEC import InTEC
                    instrument_dict[instrument] = InTEC(int(attrib["index"]))
                else:
                    return None
            return instrument_dict
        except Exception as e:
            #TODO gracefully handle exceptions. flow must keep running if this fails
            raise e