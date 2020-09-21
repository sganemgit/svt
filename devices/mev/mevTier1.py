
from mevDefines import mevDefines

class mevTier1(mevDefines):
        
    def SetPhyConfig(self, args, debug = False):
        '''
            Sets various PHY configuration parameters of a por
        '''
        print("SetPHyconfig")
        buffer = list()

        buffer.append(args['port_number'])


    def SetMacConfig(self, **kwargs):
        '''
            Set various MAC configuration parameters supported on a specific port
        '''
        arg_dict = kwargs.get('arg_dict')

    def LinkSetupAndRestartAn(Self, **kwargs):
        '''
            Sets up the link and restarts link auto-negotioation
            This command needs to be executed for other set link parameters to take effect on the link
        '''
        arg_dict = kwargs.get('arg_dict')

    def GetPhyCapabilities(self, **kwargs):
        '''
            Get various PHY capabilites supported by a port
        '''
        arg_dict = kwargs.get('arg_dict')

    def GetLinkStatus(self, **kwargs):
        '''
            Get the current status of a port
        '''
        arg_dict = kwargs.get('arg_dict')

    def SetPhyLoopback(self, **kwargs):
        '''
            sets the PHY to a loopback mode
        '''
        arg_dict = kwargs.get('arg_dict')

    def SetMacLoopback(self, **kwargs):
        '''
            sets the MAC to a loopback mode
        '''
        arg_dict = kwargs.get('arg_dict')

    def SetPhyDebug(self, **kwargs):
        '''
            resets the PHY, enables/disables the ENI link Manager
        '''
        arg_dict = kwargs.get('arg_dict')

    def GetPhyDebug(self, **kwargs):
        '''
            returns the state of the ENI link manger
        '''
        arg_dict = kwargs.get('arg_dict')



