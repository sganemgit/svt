

class PortOptionsStructure:
    def __init__(self):
        self.pmd_count = 0 
        self.max_pmd_speed = 0
        self.adaptive_nvm_global_super = 0
        self.adaptive_nvm_phy_configuration_id = 0

    @classmethod
    def GetPortOptionsStructureByList(cls, option_list):
        port_option = cls()
        port_option.pmd_count = option_list[0] & 0xf
        speed = option_list[1] & 0xf
        if speed == 0:
            port_option.max_pmd_speed = '100M'
        elif speed == 1:
            port_option.max_pmd_speed = '1G'
        elif speed == 3:
            port_option.max_pmd_speed = '5G'
        elif speed == 4:
            port_option.max_pmd_speed = '10G'
        elif speed == 5:
            port_option.max_pmd_speed = '25G'
        elif speed == 6:
            port_option.max_pmd_speed = '50G'
        elif speed == 7:
            port_option.max_pmd_speed = '100G'
        else:
            port_option.max_pmd_speed = 'N/A'
        port_option.adaptive_nvm_global_super = option_list[3] << 8 | option_list[2]
        port_option.adaptive_nvm_phy_configuration_id = option_list[5] << 8 | option_list[4]
        return port_option
        
