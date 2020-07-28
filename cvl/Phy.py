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


class Phy(cvl):
    def __init__(self):
        pass 

    
if __name__=='__main__':
    cvl = dict()
    phy = PhyType(cvl)
