

from mevDefines import mevDefines
class mev(mevDefines):

    def SetPhyConfig(self, **kwargs):
        '''
            Sets various PHY configuration parameters of a port
        '''
        arg_dict = kwargs.get('arg_dict')
        phy_type_0 = arg_dict['phy_type_0']
        phy_type_1 = arg_dict['phy_type_1']
        phy_type_2 = arg_dict['phy_type_2']
        phy_type_3 = arg_dict['phy_type_3']
        pause = arg_dict['pause']
        asm_dir = arg_dict['asm_dir']
        low_power_mode = arg_dict['low_power_mode']
        enable_link = arg_dict['enable_link']
        enable_automatic_link_update = arg_dict['enable_automatic_link_update']
        lesm_enable = arg_dict['lesm_enable']
        auto_fec_enable = arg_dict['auto_fec_enable']
        lplu = arg_dict['lplu']
        ability_no_fec = arg_dict['ability_no_fec']
        ability_10g_kr_fec = arg_dict['ability_10g_kr_fec']
        request_10g_kr_fec = arg_dict['request_10g_kr_fec']
        request_25g_kr_fec = arg_dict['request_25g_kr_fec']
        request_rs_fec_528 = arg_dict['request_rs_fec_528']
        request_rs_fec_544 = arg_dict['request_rs_fec_544']
        
        

    
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


