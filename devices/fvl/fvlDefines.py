from fvlBase import fvlBase
from devices.common.DeviceCommon import DeviceCommon

class fvlDefines(fvlBase, DeviceCommon):

    link_stable = True
    Return_list = [0]
    debug_mode = False

     #list should hold the high values before the low
    reg_dict = {"PTC64": [0x003006a4, 0x003006a0],
                "PTC127": [0x003006c4, 0x003006c0],
                "PTC255": [0x003006e4, 0x003006e0],
                "PTC511": [0x00300704, 0x00300700],
                "PTC1023": [0x00300724, 0x00300720],
                "PTC1522": [0x00300744, 0x00300740],
                "PTC9522": [0x00300764, 0x00300760],
                "PRC64": [0x00300484, 0x00300480],
                "PRC127": [0x003004a4, 0x003004a0],
                "PRC255": [0x003004c4, 0x003004c0],
                "PRC511": [0x003004e4, 0x003004e0],
                "PRC1023": [0x00300504, 0x00300500],
                "PRC1522": [0x00300524, 0x00300520],
                "PRC9522": [0x00300544, 0x00300540],
                "CRCERRS": [0x00300080],
                "ILLERRC": [0x003000e0],
                "ERRBC": [0x003000c0],
                "MLFC": [0x00300020],
                "MRFC":  [0x00300040],
                "RLEC": [0x003000a0],
                "RUC": [0x00300100],
                "RFC": [0x00300560],
                "ROC": [0x00300120],
                "RJC": [0x00300580],
                "MSPDC": [0x00300060],
                "FVL_LDPC": [0x00300620]
               }




    phy_speed_to_bit_dict = {'2.5G' : 0,
                             '100M' : 1,
                             '1G'   : 2,
                             '10G'  : 3,
                             '40G'  : 4,
                             '20G'  : 5,
                             '25G'  : 6,
                             '5G'   : 7}

    Mac_link_speed_dict = {0:"100M",1:"1G",2:"10G",3:"40G",4:"20G"}

    Phy_link_speed_dict = {0:"N/A",2:"100M", 4:"1G", 6:"10G", 1:"2.5G", 3:"5G"}# according register 1E.400D in BCM data sheet

    Phy_link_speed_fvl_dict = {0:"2.5G",1:"100M",2:"1G",3:"10G",4:"40G",5:"20G",6:"25G",7:"5G"}

    Phy_Master_Slave_status_dict = {0:"Slave",1:"Master"}

    Phy_Address_dict = {0:0, 1:2, 2:1, 3:3}

    Set_PhyType_dict = {31:'empty',
                        30:'20GBASE-KR2',
                        29:'1000BASE-T-OPTICAL',
                        28:'1000BASE-LX',
                        27:'1000BASE-SX',
                        26:'40GBASE-LR4',
                        25:'40GBASE-SR4',
                        24:'40GBASE-CR4',
                        23:'10GBASE-CR1',
                        22:'10GBASE-SFP+Cu',
                        21:'10GBASE-LR',
                        20:'10GBASE-SR',
                        19:'10GBASE-T',
                        18:'1000BASE-T',
                        17:'100BASE-T',
                        16:'empty',
                        15:'empty',
                        14:'empty',
                        13:'empty',
                        12:'empty',
                        11:'10GBASE-CR1',
                        10:'40GBASE-CR4',
                        9:'XLPPI',
                        8:'XLAUI',
                        7:'SFI',
                        6:'XFI',
                        5:'XAUI',
                        4:'40GBASE-KR4',
                        3:'10GBASE-KR',
                        2:'10GBASE-KX4',
                        1:'1000BASE-KX',
                        0:'SGMII'}

    Phytype_to_speed_dict = {'20GBASE-KR2':'20G',
                             '1000BASE-T-OPTICAL': '1G',
                             '1000BASE-LX':'1G',
                             '1000BASE-SX':'1G',
                             '40GBASE-LR4':'40G',
                             '40GBASE-SR4':'40G',
                             '40GBASE-CR4':'40G',
                             '10GBASE-CR1':'10G',
                             '10GBASE-SFP+Cu':'10G',
                             '10GBASE-LR':'10G',
                             '10GBASE-SR':'10G',
                             '10GBASE-T':'10G',
                             '1000BASE-T':'1G',
                             '100BASE-T':'100M',
                             '10GBASE-CR1':'10G',
                             '40GBASE-CR4':'40G',
                             'XLPPI':'10G',
                             'XLAUI':'10G',
                             'SFI':'10G',
                             'XFI':'10G',
                             'XAUI':'10G',
                             '40GBASE-KR4':'40G',
                             '10GBASE-KR':'10G',
                             '10GBASE-KX4':'10G',
                             '1000BASE-KX':'1G',
                             'SGMII':'1G',
                             '2.5GBase-T':'2.5G',
                             '5GBase-T':'5G'}

    #phy types names must comlie with ieee 802.3
    get_Ability_PhyTypeExtension_dict = {0 : '25GBase-KR',
                                         1 : '25GBase-CR',
                                         2 : '25GBase-SR',
                                         3 : '25GBase-LR',
                                         4 : '25G-AOC',
                                         5 : '25G-ACC',
                                         6 : '2.5GBase-T',
                                         7 : '5GBase-T'}

    get_Ability_PhyType_dict = {31:'empty',
                                30:'20GBASE-KR2',
                                29:'1000BASE-T-OPTICAL',
                                28:'1000BASE-LX',
                                27:'1000BASE-SX',
                                26:'40GBASE-LR4',
                                25:'40GBASE-SR4',
                                24:'40GBASE-CR4',
                                23:'10GBASE-CR1',
                                22:'10GBASE-SFP+Cu',
                                21:'10GBASE-LR',
                                20:'10GBASE-SR',
                                19:'10GBASE-T',
                                18:'1000BASE-T',
                                17:'1000Base-TX',
                                16:'reserved',
                                15:'reserved',
                                14:'reserved',
                                13:'reserved',
                                12:'reserved',
                                11:'10GBASE-CR1',
                                10:'40GBASE-CR4',
                                9:'XLPPI',
                                8:'XLAUI',
                                7:'SFI',
                                6:'XFI',
                                5:'XAUI',
                                4:'40GBASE-KR4',
                                3:'10GBASE-KR',
                                2:'10GBASE-KX4',
                                1:'1000BASE-KX',
                                0:'SGMII'}

    get_Ability_speed_dict = {7:'5G',
                              6:'25G',
                              5:'20G',
                              4:'40G',
                              3:'10G',
                              2:'1G',
                              1:'100M',
                              0:'2.5G'}

    get_Ability_EEE_dict = {7:'EEE 40G-KR4',6:'EEE 10GBASE-KR',5:'EEE 10GBASE-KX4',4:'EEE 1000BASE-KX',3:'EEE 10GBASE-T',2:'EEE  1000BASE-T',1:'EEE 100BASE-TX',0:'empty'}


    ## AQ 0x607 Get link status response ####

    get_Phy_Type_Status_dict = {30:'20GBASE-KR2',29:'1000BASE-T Optical',28:'1000BASE-LX',27:'1000BASE-SX',26:'40GBASE-LR4',24:'40GBASE-CR4',23:'40GBASE-CR4',22:'10GBASE-CR1',21:'10GBASE-SFP+Cu',20:'10GBASE-LR',19:'10GBASE-SR',18:'10GBASE-T',17:'1000BASE-T',17:'100BASE-TX',13:'SQSFP+ Active Direct Attach',12:'SFP+ Active Direct Attach',11:'10GBASE-CR1',10:'40GBASE-CR4',9:'XLPPI',8:'XLAUI',7:'SFI',6:'XFI',5:'XAUI',4:'40GBASE-KR4',3:'10GBASE-KR',2:'10GBASE-KX4',1:'1000BASE-KX',0:'SGMII'}

    get_Speed_Status_dict = {7:'empty',6:'25G',5:'20G',4:'40G',3:'10G',2:'1G',1:'100M',0:'empty'}
