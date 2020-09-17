
#--------------------------------------------
# @author Shady Ganem <shady.ganem@intel.com>
#--------------------------------------------


class AqDescriptor(object):
    """ This class represents AQ command descriptor. 
        Each field represents relevant bytes in descriptor.
            flags:        bytes 0-1
            opcode:       bytes 2-3                 
            datalen:      bytes 4-5
            retval:       bytes 6-7            
            cookie_high:  bytes 8-11
            cookie_low:   bytes 12-15
            param0:       bytes 16-19
            param1:       bytes 20-23
            addr_high:    bytes 24-27
            addr_low:     bytes 28-31 
    """
    
    def __init__(self):
        self.opcode = 0
        self.flags = 0
        self.param0 = 0
        self.param1 = 0
        self.cookie_high = 0
        self.cookie_low = 0
        self.addr_high = 0
        self.addr_low = 0
        self.retval = 0
        self.datalen = 0
