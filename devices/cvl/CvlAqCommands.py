from core.structs.AqDescriptor import AqDescriptor

class LLDP_AQC:
    @classmethod
    def GetLldpMibAqDescriptor(cls):
        aq_desc = AqDescriptor()
        aq_desc.flags = 0x0
        aq_desc.opcode = 0x0A00
