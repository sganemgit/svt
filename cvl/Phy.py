try:
    import readline
except ImportError:
    print("Module readline not available.")
else:
    import rlcompleter
    readline.parse_and_bind("tab: complete")

Phys = {'p100G_AUI4':['RS_544'],
        'p100G_AUI2':['RS_544'],
        'p100G_CAUI4':['RS_528','NO_FEC']}

def Set(self):
    print self._phy_type
    print self.__main__
    #self._cvl.SetPhyConfiguration(self._phy_type,

class PhyType:
    def __init__(self, cvl):
        self._cvl = 'cvl class'
        for phy,fecs in Phys.iteritems():
            self.__dict__[phy] = Fec(cvl,phy)

class Fec:
    def Set(self):
        print self.__main__
        print self.phy_type
        #self._cvl.SetPhyConfiguration(self._phy_type,

    def __init__(self, cvl, phy_type):
        self._cvl = cvl
        self.phy_type = phy_type
        print Phys[phy_type]
        for fec in Phys[phy_type]:
            self.__dict__[fec] = Set


if __name__=='__main__':
    cvl = dict()
    phy = PhyType(cvl)
