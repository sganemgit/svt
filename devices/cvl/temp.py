def get_all_phy_types(phy_caps,index_of_dword):
        '''
            Call this funtion to decode the PHY capabilities in decimal to a list of PHY types
        '''
        netlist_defines = Netlist_Defines()
        list_of_phy_types = []
        if index_of_dword == 0:
            if (phy_caps >> netlist_defines.PHY_INDEX_100BASE_TX) & 1:
                list_of_phy_types.append('100BASE-TX')
            if (phy_caps >> netlist_defines.PHY_INDEX_100M_SGMII) & 1:
                list_of_phy_types.append('100M-SGMII')
            if (phy_caps >> netlist_defines.PHY_INDEX_1000BASE_T) & 1:
                list_of_phy_types.append('1000BASE-T')
            if (phy_caps >> netlist_defines.PHY_INDEX_1000BASE_SX) & 1:
                list_of_phy_types.append('1000BASE-SX')
            if (phy_caps >> netlist_defines.PHY_INDEX_1000BASE_LX) & 1:
                list_of_phy_types.append('1000BASE-LX')
            if (phy_caps >> netlist_defines.PHY_INDEX_1G_SGMII) & 1:
                list_of_phy_types.append('1G-SGMII')
            if (phy_caps >> netlist_defines.PHY_INDEX_2P5GBASE_T) & 1:
                list_of_phy_types.append('2P5GBASE-T')
            if (phy_caps >> netlist_defines.PHY_INDEX_2P5GBASE_X) & 1:
                list_of_phy_types.append('2P5GBASE-X')
            if (phy_caps >> netlist_defines.PHY_INDEX_2P5GBASE_KX) & 1:
                list_of_phy_types.append('2P5GBASE-KX')
            if (phy_caps >> netlist_defines.PHY_INDEX_5GBASE_T) & 1:
                list_of_phy_types.append('5GBASE-T')
            if (phy_caps >> netlist_defines.PHY_INDEX_5GBASE_KR) & 1:
                list_of_phy_types.append('5GBASE-KR')
            if (phy_caps >> netlist_defines.PHY_INDEX_10GBASE_T) & 1:
                list_of_phy_types.append('10GBASE-T')
            if (phy_caps >> netlist_defines.PHY_INDEX_10G_SFI_DA) & 1:
                list_of_phy_types.append('10G-SFI-DA')
            if (phy_caps >> netlist_defines.PHY_INDEX_10GBASE_SR) & 1:
                list_of_phy_types.append('10GBASE-SR')
            if (phy_caps >> netlist_defines.PHY_INDEX_10GBASE_LR) & 1:
                list_of_phy_types.append('10GBASE-LR')
            if (phy_caps >> netlist_defines.PHY_INDEX_10GBASE_KR_CR1) & 1:
                list_of_phy_types.append('10GBASE-KR/CR1')
            if (phy_caps >> netlist_defines.PHY_INDEX_10G_SFI_AOC_ACC) & 1:
                list_of_phy_types.append('10G-SFI-C2M')
            if (phy_caps >> netlist_defines.PHY_INDEX_10G_SFI_C2C) & 1:
                list_of_phy_types.append('10G-SFI-C2C')
            if (phy_caps >> netlist_defines.PHY_INDEX_25GBASE_T) & 1:
                list_of_phy_types.append('25GBASE-T')
            if (phy_caps >> netlist_defines.PHY_INDEX_25GBASE_CR) & 1:
                list_of_phy_types.append('25GBASE-CR')
            if (phy_caps >> netlist_defines.PHY_INDEX_25GBASE_CR_S) & 1:
                list_of_phy_types.append('25GBASE-CR-S')
            if (phy_caps >> netlist_defines.PHY_INDEX_25GBASE_CR1) & 1:
                list_of_phy_types.append('25GBASE-CR1')
            if (phy_caps >> netlist_defines.PHY_INDEX_25GBASE_SR) & 1:
                list_of_phy_types.append('25GBASE-SR')
            if (phy_caps >> netlist_defines.PHY_INDEX_25GBASE_LR) & 1:
                list_of_phy_types.append('25GBASE-LR')
            if (phy_caps >> netlist_defines.PHY_INDEX_25GBASE_KR) & 1:
                list_of_phy_types.append('25GBASE-KR')
            if (phy_caps >> netlist_defines.PHY_INDEX_25GBASE_KR_S) & 1:
                list_of_phy_types.append('25GBASE-KR_S')
            if (phy_caps >> netlist_defines.PHY_INDEX_25GBASE_KR1) & 1:
                list_of_phy_types.append('25GBASE-KR1')
            if (phy_caps >> netlist_defines.PHY_INDEX_25G_AUI_AOC_ACC) & 1:
                list_of_phy_types.append('25G-AUI-C2M')
            if (phy_caps >> netlist_defines.PHY_INDEX_25G_AUI_C2C) & 1:
                list_of_phy_types.append('25G-AUI-C2C')
            if (phy_caps >> netlist_defines.PHY_INDEX_40GBASE_CR4) & 1:
                list_of_phy_types.append('40GBASE-CR4')
            if (phy_caps >> netlist_defines.PHY_INDEX_40GBASE_SR4) & 1:
                list_of_phy_types.append('40GBASE-SR4')
            return list_of_phy_types 
        if index_of_dword == 1:
            if (phy_caps >> (netlist_defines.PHY_INDEX_40GBASE_LR4 - 32)) & 1:
                list_of_phy_types.append('40GBASE-LR4')
            if (phy_caps >> (netlist_defines.PHY_INDEX_40GBASE_KR4 - 32)) & 1:
                list_of_phy_types.append('40GBASE-KR4')
            if (phy_caps >> (netlist_defines.PHY_INDEX_40G_XLAUI_AOC_ACC - 32)) & 1:
                list_of_phy_types.append('40G-XLAUI-C2M')
            if (phy_caps >> (netlist_defines.PHY_INDEX_40G_XLAUI - 32)) & 1:
                list_of_phy_types.append('40G-XLAUI')
            if (phy_caps >> (netlist_defines.PHY_INDEX_50GBASE_CR2 - 32)) & 1:
                list_of_phy_types.append('50GBAE-CR2')
            if (phy_caps >> (netlist_defines.PHY_INDEX_50GBASE_KR2 - 32)) & 1:
                list_of_phy_types.append('50GBAE-KR2')        
            if (phy_caps >> (netlist_defines.PHY_INDEX_50G_LAUI2_AOC_ACC - 32)) & 1:
                list_of_phy_types.append('50G-LAUI2-C2M')
            if (phy_caps >> (netlist_defines.PHY_INDEX_50G_LAUI2 - 32)) & 1:
                list_of_phy_types.append('50G-LAUI2')
            if (phy_caps >> (netlist_defines.PHY_INDEX_50G_AUI2_AOC_ACC - 32)) & 1:
                list_of_phy_types.append('50G-AUI2-C2M')
            if (phy_caps >> (netlist_defines.PHY_INDEX_50G_AUI2 - 32)) & 1:
                list_of_phy_types.append('50G-AUI2') 
            if (phy_caps >> (netlist_defines.PHY_INDEX_50GBASE_CR_PAM4 - 32)) & 1:
                list_of_phy_types.append('50GBASE-CR-PAM4')
            if (phy_caps >> (netlist_defines.PHY_INDEX_50GBASE_SR - 32)) & 1:
                list_of_phy_types.append('50GBASE-SR')
            if (phy_caps >> (netlist_defines.PHY_INDEX_50GBASE_FR - 32)) & 1:
                list_of_phy_types.append('50GBASE-FR')
            if (phy_caps >> (netlist_defines.PHY_INDEX_50GBASE_LR - 32)) & 1:
                list_of_phy_types.append('50GBASE-LR')
            if (phy_caps >> (netlist_defines.PHY_INDEX_50GBASE_KR_PAM4 - 32)) & 1:
                list_of_phy_types.append('50GBASE-KR-PAM4')
            if (phy_caps >> (netlist_defines.PHY_INDEX_50G_AUI1_AOC_ACC - 32)) & 1:
                list_of_phy_types.append('50G-AUI1-C2M')
            if (phy_caps >> (netlist_defines.PHY_INDEX_50G_AUI1 - 32)) & 1:
                list_of_phy_types.append('50G-AUI1') 
            if (phy_caps >> (netlist_defines.PHY_INDEX_100GBASE_CR4 - 32)) & 1:
                list_of_phy_types.append('100GBASE-CR4')
            if (phy_caps >> (netlist_defines.PHY_INDEX_100GBASE_SR4 - 32)) & 1:
                list_of_phy_types.append('100GBASE-SR4')
            if (phy_caps >> (netlist_defines.PHY_INDEX_100GBASE_LR4 - 32)) & 1:
                list_of_phy_types.append('100GBASE-LR4')
            if (phy_caps >> (netlist_defines.PHY_INDEX_100GBASE_KR4 - 32)) & 1:
                list_of_phy_types.append('100GBASE-KR4')
            if (phy_caps >> (netlist_defines.PHY_INDEX_100G_CAUI4_AOC_ACC - 32)) & 1:
                list_of_phy_types.append('100G-CAUI4-C2M')
            if (phy_caps >> (netlist_defines.PHY_INDEX_100G_CAUI4 - 32)) & 1:
                list_of_phy_types.append('100G-CAUI4')  
            if (phy_caps >> (netlist_defines.PHY_INDEX_100G_AUI4_AOC_ACC - 32)) & 1:
                list_of_phy_types.append('100G-AUI4-C2M')
            if (phy_caps >> (netlist_defines.PHY_INDEX_100G_AUI4 - 32)) & 1:
                list_of_phy_types.append('100G-AUI4')
            if (phy_caps >> (netlist_defines.PHY_INDEX_100GBASE_KR4_PAM4 - 32)) & 1:
                list_of_phy_types.append('100GBASE-KR4-PAM4')
            if (phy_caps >> (netlist_defines.PHY_INDEX_100GBASE_CP2 - 32)) & 1:
                list_of_phy_types.append('100GBASE-CP2')
            if (phy_caps >> (netlist_defines.PHY_INDEX_100GBASE_SR2 - 32)) & 1:
                list_of_phy_types.append('100GBASE-SR2') 
            if (phy_caps >> (netlist_defines.PHY_INDEX_100GBASE_DR - 32)) & 1:
                list_of_phy_types.append('100GBASE-DR')
            return list_of_phy_types    
        if index_of_dword == 2:
            if (phy_caps >> (netlist_defines.PHY_INDEX_100GBASE_KR2_PAM4 - 64)) & 1:
                list_of_phy_types.append('100GBASE-KR2-PAM4')
            if (phy_caps >> (netlist_defines.PHY_INDEX_100G_AUI2_AOC_ACC - 64)) & 1:
                list_of_phy_types.append('100G-AUI2-C2M') 
            if (phy_caps >> (netlist_defines.PHY_INDEX_100G_AUI2 - 64)) & 1:
                list_of_phy_types.append('100G-AUI2')
            if (phy_caps >> (netlist_defines.PHY_INDEX_200GBASE_CR4_PAM4 - 64)) & 1:
                list_of_phy_types.append('200GBASE-CR4-PAM4')
            if (phy_caps >> (netlist_defines.PHY_INDEX_200GBASE_SR4 - 64)) & 1:
                list_of_phy_types.append('200GBASE-SR4')
            if (phy_caps >> (netlist_defines.PHY_INDEX_200GBASE_FR4 - 64)) & 1:
                list_of_phy_types.append('200GBASE-FR4')
            if (phy_caps >> (netlist_defines.PHY_INDEX_200GBASE_LR4 - 64)) & 1:
                list_of_phy_types.append('200GBASE-LR4')
            if (phy_caps >> (netlist_defines.PHY_INDEX_200GBASE_DR4 - 64)) & 1:
                list_of_phy_types.append('200GBASE-DR4')
            if (phy_caps >> (netlist_defines.PHY_INDEX_200GBASE_KR4_PAM4 - 64)) & 1:
                list_of_phy_types.append('200GBASE-KR4-PAM4')
            if (phy_caps >> (netlist_defines.PHY_INDEX_200G_AUI4_AOC_ACC - 64)) & 1:
                list_of_phy_types.append('200G-AUI4-C2M') 
            if (phy_caps >> (netlist_defines.PHY_INDEX_200G_AUI4 - 64)) & 1:
                list_of_phy_types.append('200G-AUI4')
            if (phy_caps >> (netlist_defines.PHY_INDEX_200G_AUI8_AOC_ACC - 64)) & 1:
                list_of_phy_types.append('200G-AUI8-C2M') 
            if (phy_caps >> (netlist_defines.PHY_INDEX_200G_AUI8 - 64)) & 1:
                list_of_phy_types.append('200G-AUI8')
            if (phy_caps >> (netlist_defines.PHY_INDEX_400GBASE_FR8 - 64)) & 1:
                list_of_phy_types.append('400GBASE-FR8')
            if (phy_caps >> (netlist_defines.PHY_INDEX_400GBASE_LR8 - 64)) & 1:
                list_of_phy_types.append('400GBASE-LR8')
            if (phy_caps >> (netlist_defines.PHY_INDEX_400GBASE_DR4 - 64)) & 1:
                list_of_phy_types.append('400GBASE-DR4')
            if (phy_caps >> (netlist_defines.PHY_INDEX_400G_AUI8_AOC_ACC - 64)) & 1:
                list_of_phy_types.append('400G-AUI8-C2M') 
            if (phy_caps >> (netlist_defines.PHY_INDEX_400G_AUI8 - 64)) & 1:
                list_of_phy_types.append('400G-AUI8')
            return list_of_phy_types
        if index_of_dword == 3:
            return list_of_phy_types
        




class Netlist_Defines:
    def __init__(self):
        self.netlist_defines()

    def netlist_defines(self):
        #Netlist Header Section defines
        self.MODULE_LENGTH_WORD_OFFSET = 0
        self.NODE_COUNT_WORD_OFFSET = 1
        self.NETLIST_MAP_VER_WORD_OFFSET = 2
        self.NETLIST_CRC_WORD_OFFSET = 2
        self.NETLIST_VER_WORD_OFFSET = 3
        self.HDR_NODE_HANDLE_START_WORD_OFFSET = 4
        self.NODE_BLOCK_START_WORD_OFFSET = 5
        self.HDR_NODE_HANDLE_INTERVAL = 2
        self.NODE_BLOCK_INTERVAL = 2
        self.NETLIST_MAP_VER_FIELD_OFFSET = 8
        
        #Node Header Section defines
        #Word offsets
        self.NODE_TYPE_WORD_OFFSET = 0
        self.NODE_SECTION_LENGTH_WORD_OFFSET = 0
        self.NODE_HANDLE_WORD_OFFSET = 1
        self.NODE_ADDRESS_WORD_OFFSET = 2
        self.NODE_PART_NUMBER_WORD_OFFSET = 3
        self.NODE_OPTIONS_WORD_OFFSET = 3
        self.NODE_IO_POINTER_WORD_OFFSET = 4
        self.NODE_PORT_OPTION_POINTER_WORD_OFFSET = 5
        self.NODE_LINE_ANALOG_POINTER_WORD_OFFSET = 6
        self.NODE_HOST_ANALOG_POINTER_WORD_OFFSET = 7
        #Field offsets
        self.NODE_TYPE_FIELD_OFFSET = 12
        self.NODE_ADDRESS_TYPE_FIELD_OFFSET = 12
        self.NODE_BUS_TYPE_FIELD_OFFSET = 10
        self.PART_NUMBER_FIELD_OFFSET = 8
        self.MODULE_QUALIFICATION_ENABLE_FIELD_OFFSET = 3
        self.INNERMOST_PHY_FIELD_OFFSET = 2
        self.CONFLICT_RESOLUTION_FIELD_OFFSET = 1
        self.IO_COUNT_FIELD_OFFSET = 12
        self.PORT_OPTION_COUNT_FIELD_OFFSET = 12
        self.LINE_LANE_COUNT_FIELD_OFFSET = 12
        self.HOST_LANE_COUNT_FIELD_OFFSET = 12
        
        #Node IO Section defines
        #Word offsets
        self.DRIVING_NODE_HANDLE_WORD_OFFSET = 0
        self.IO_TYPE_DRIVING_INTERFACE_WORD_OFFSET = 1
        #Intervals
        self.DRIVING_NODE_HANDLE_INTERVAL = 2
        self.IO_TYPE_DRIVING_INTERVACE_INTERVAL = 2
        #Field offsets
        self.DRIVING_IO_NUMBER_FIELD_OFFSET = 10
        self.DRIVEN_FIELD_OFFSET = 15
        self.VALUE_FIELD_OFFSET = 14
        self.POLARITY_FIELD_OFFSET = 13
        self.INTERRUPT_FIELD_OFFSET = 11
        self.INTERFACE_SPEED_FIELD_OFFSET = 8
        self.IO_TYPE_FIELD_OFFSET = 5
        
        #Node Port Option Pointer Section
        self.PORT_OPTION_POINTER_WORD_OFFSET = 0
        self.PORT_OPTION_POINTER_INTERVAL = 1
        
        #Node Port Option Header Section
        self.ANVM_GLOBAL_SUPERFEATURE_CONFIGID_WORD_OFFSET = 0
        self.ANVM_PHY_CONFIGID_WORD_OFFSET = 1
        self.MINIMUM_SKU_WORD_OFFSET = 2
        self.PMD_COUNT_CAPS_POINTER_WORD_OFFSET = 4
        self.PHY_CAPABILITIES_WORD_OFFSET = 5
        self.PHY_CAPABILITIES_INTERVAL = 1
        self.REQUIRED_LANE_SPEED_FIELD_OFFSET = 7
        self.SWITCH_QUAD1_BANDWIDTH_FIELD_OFFSET = 4
        self.SWITCH_NIC_QUAD0_BANDWIDTH_FIELD_OFFSET = 2
        self.PMD_COUNT_FIELD_OFFSET = 12
        
        #Node PHY Capabilities Section
        self.ANVM_PORT_CONFIGID_WORD_OFFSET = 0
        self.ANVM_FUNCTION_CONFIGID_WORD_OFFSET = 1
        self.ANVM_PORT_FUNCTION_FEATURE_ID_WORD_OFFSET = 2
        self.PMD_WIDTH_WORD_OFFSET = 3
        self.LINK_OPTIONS_0_WORD_OFFSET = 4
        self.LINK_OPTIONS_1_WORD_OFFSET = 5
        self.EEE_OPTIONS_0_WORD_OFFSET = 6
        self.EEE_OPTIONS_1_WORD_OFFSET = 7
        self.HOST_PMD_CAPABILITIES_0_WORD_OFFSET = 8
        self.HOST_PMD_CAPABILITIES_1_WORD_OFFSET = 9
        self.HOST_PMD_CAPABILITIES_2_WORD_OFFSET = 10
        self.HOST_PMD_CAPABILITIES_3_WORD_OFFSET = 11
        self.LINE_PMD_CAPABILITIES_0_WORD_OFFSET = 12
        self.LINE_PMD_CAPABILITIES_1_WORD_OFFSET = 13
        self.LINE_PMD_CAPABILITIES_2_WORD_OFFSET = 14
        self.LINE_PMD_CAPABILITIES_3_WORD_OFFSET = 15
        self.LINE_PMD_CAPABILITIES_4_WORD_OFFSET = 16
        self.LINE_PMD_CAPABILITIES_5_WORD_OFFSET = 17
        self.LINE_PMD_CAPABILITIES_6_WORD_OFFSET = 18
        self.LINE_PMD_CAPABILITIES_7_WORD_OFFSET = 19
        #ANVM Per Port / Function fields
        self.PORT_FEATURE_ID_FIELD_OFFSET = 8
        #PMD Width Fields
        self.HOST_PMD_WIDTH_FIELD_OFFSET = 12
        self.HOST_PMD_LANE_0_FIELD_OFFSET = 8
        self.LINE_PMD_WIDTH_FIELD_OFFSET = 4
        self.LINE_PMD_LANE_0_FIELD_OFFSET = 0
        #PHY type index
        self.PHY_INDEX_100BASE_TX = 0
        self.PHY_INDEX_100M_SGMII = 1
        self.PHY_INDEX_1000BASE_T = 2
        self.PHY_INDEX_1000BASE_SX = 3
        self.PHY_INDEX_1000BASE_LX = 4
        self.PHY_INDEX_1000BASE_KX = 5
        self.PHY_INDEX_1G_SGMII = 6
        self.PHY_INDEX_2P5GBASE_T = 7
        self.PHY_INDEX_2P5GBASE_X = 8
        self.PHY_INDEX_2P5GBASE_KX = 9
        self.PHY_INDEX_5GBASE_T = 10
        self.PHY_INDEX_5GBASE_KR = 11
        self.PHY_INDEX_10GBASE_T = 12
        self.PHY_INDEX_10G_SFI_DA = 13
        self.PHY_INDEX_10GBASE_SR = 14
        self.PHY_INDEX_10GBASE_LR = 15
        self.PHY_INDEX_10GBASE_KR_CR1 = 16
        self.PHY_INDEX_10G_SFI_AOC_ACC = 17
        self.PHY_INDEX_10G_SFI_C2C = 18
        self.PHY_INDEX_25GBASE_T = 19
        self.PHY_INDEX_25GBASE_CR = 20
        self.PHY_INDEX_25GBASE_CR_S = 21
        self.PHY_INDEX_25GBASE_CR1 = 22
        self.PHY_INDEX_25GBASE_SR = 23
        self.PHY_INDEX_25GBASE_LR = 24
        self.PHY_INDEX_25GBASE_KR = 25
        self.PHY_INDEX_25GBASE_KR_S = 26
        self.PHY_INDEX_25GBASE_KR1 = 27
        self.PHY_INDEX_25G_AUI_AOC_ACC = 28
        self.PHY_INDEX_25G_AUI_C2C = 29
        self.PHY_INDEX_40GBASE_CR4 = 30
        self.PHY_INDEX_40GBASE_SR4 = 31
        self.PHY_INDEX_40GBASE_LR4 = 32
        self.PHY_INDEX_40GBASE_KR4 = 33
        self.PHY_INDEX_40G_XLAUI_AOC_ACC = 34
        self.PHY_INDEX_40G_XLAUI = 35
        self.PHY_INDEX_50GBASE_CR2 = 36
        self.PHY_INDEX_50GBASE_KR2 = 39
        self.PHY_INDEX_50G_LAUI2_AOC_ACC = 40
        self.PHY_INDEX_50G_LAUI2 = 41
        self.PHY_INDEX_50G_AUI2_AOC_ACC = 42
        self.PHY_INDEX_50G_AUI2 = 43
        self.PHY_INDEX_50GBASE_CR_PAM4 = 44
        self.PHY_INDEX_50GBASE_SR = 45
        self.PHY_INDEX_50GBASE_FR = 46
        self.PHY_INDEX_50GBASE_LR = 47
        self.PHY_INDEX_50GBASE_KR_PAM4 = 48
        self.PHY_INDEX_50G_AUI1_AOC_ACC = 49
        self.PHY_INDEX_50G_AUI1 = 50
        self.PHY_INDEX_100GBASE_CR4 = 51
        self.PHY_INDEX_100GBASE_SR4 = 52
        self.PHY_INDEX_100GBASE_LR4 = 53
        self.PHY_INDEX_100GBASE_KR4 = 54
        self.PHY_INDEX_100G_CAUI4_AOC_ACC = 55
        self.PHY_INDEX_100G_CAUI4 = 56
        self.PHY_INDEX_100G_AUI4_AOC_ACC = 57
        self.PHY_INDEX_100G_AUI4 = 58
        self.PHY_INDEX_100GBASE_KR4_PAM4 = 60
        self.PHY_INDEX_100GBASE_CP2 = 61
        self.PHY_INDEX_100GBASE_SR2 = 62
        self.PHY_INDEX_100GBASE_DR = 63
        self.PHY_INDEX_100GBASE_KR2_PAM4 = 64
        self.PHY_INDEX_100G_AUI2_AOC_ACC = 67
        self.PHY_INDEX_100G_AUI2 = 68
        self.PHY_INDEX_200GBASE_CR4_PAM4 = 69
        self.PHY_INDEX_200GBASE_SR4 = 70
        self.PHY_INDEX_200GBASE_FR4 = 71
        self.PHY_INDEX_200GBASE_LR4 = 72
        self.PHY_INDEX_200GBASE_DR4 = 73
        self.PHY_INDEX_200GBASE_KR4_PAM4 = 74
        self.PHY_INDEX_200G_AUI4_AOC_ACC = 75
        self.PHY_INDEX_200G_AUI4 = 76
        self.PHY_INDEX_200G_AUI8_AOC_ACC = 77
        self.PHY_INDEX_200G_AUI8 = 78
        self.PHY_INDEX_400GBASE_FR8 = 79
        self.PHY_INDEX_400GBASE_LR8 = 80
        self.PHY_INDEX_400GBASE_DR4 = 81
        self.PHY_INDEX_400G_AUI8_AOC_ACC = 82
        self.PHY_INDEX_400G_AUI8 = 83

