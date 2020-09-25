
#--------------------------------------------
# @author Shady Ganem <shady.ganem@intel.com>
#--------------------------------------------

import sys
import time
from core.utilities.BitManipulation import *
from core.structs.AqDescriptor import AqDescriptor
from cpkTier1 import *

class cpk(cpkTier1):
    '''
    	This class contains all the methods to interface with a cvl pf
    '''
