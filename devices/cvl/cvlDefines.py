
#--------------------------------------------
# @author Shady Ganem <shady.ganem@intel.com>
#--------------------------------------------

import sys
import os

from devices.cvl.cvlBase import cvlBase


class cvlDefines(cvlBase):
    # list should hold the high values before the low
    reg_dict = {"PTC64": [0x00380B84, 0x00380B80],
                "PTC127": [0x00380BC4, 0x00380BC0],
                "PTC255": [0x00380C04, 0x00380C00],
                "PTC511": [0x00380C44, 0x00380C40],
                "PTC1023": [0x00380C84, 0x00380C80],
                "PTC1522": [0x00380CC4, 0x00380CC0],
                "PTC9522": [0x00380D04, 0x00380D00],
                "PRC64": [0x00380904, 0x00380900],
                "PRC127": [0x00380944, 0x00380940],
                "PRC255": [0x00380984, 0x00380980],
                "PRC511": [0x003809C4, 0x003809C0],
                "PRC1023": [0x00380A04, 0x00380A00],
                "PRC1522": [0x00380A44, 0x00380A40],
                "PRC9522": [0x00380A84, 0x00380A80],
                "CRCERRS": [0x00380104, 0x00380100],
                "ILLERRC": [0x003801C4, 0x003801C0],
                "ERRBC": [0x00380184, 0x00380180],
                "MLFC": [0x00380044, 0x00380040],
                "MRFC":  [0x00380084, 0x00380080],
                "RLEC": [0x00380144, 0x00380140],
                "RUC": [0x00380204, 0x00380200],
                "RFC": [0x00380AC4, 0x00380AC0],
                "ROC": [0x00380244, 0x00380240],
                "RJC": [0x00380B04, 0x00380B00],
                "MSPDC": [0x003800C4, 0x003800C0],
                "LDPC": [0x003800C4, 0x000AC280], 
                "GLPRT_PXOFFRXC": [0x00380500],
                "PRTMAC_LINK_DOWN_COUNTER[PRT]": [0x001E47C0]}

    reset_type_dict = {"globr": "GLOBAL", "pfr": "PF", "corer": "CORE", "empr": "EMP", "flr": "FL", "pcir": "PCI",
                       "bmer": "BME", "vfr": "VF_SW", "vflr": "VFLR"}

    fec_dict = {"400G-AUI8": ['25G_RS_544_FEC'],
                "400G-AUI8-AOC-ACC":['25G_RS_544_FEC'],
                "400GBase-DR4":['25G_RS_544_FEC'],
                "400GBase-LR8":['25G_RS_544_FEC'],
                "400GBase-FR8":['25G_RS_544_FEC'],
                "200G-AUI8":['25G_RS_544_FEC'],
                "200G-AUI8-AOC-ACC":['25G_RS_544_FEC'],
                "200G-AUI4":['25G_RS_544_FEC'],
                "200G-AUI4-AOC-ACC":['25G_RS_544_FEC'],
                "200GBase-KR4-PAM4":['25G_RS_544_FEC'],
                "200GBase-DR4":['25G_RS_544_FEC'],
                "200GBase-LR4":['25G_RS_544_FEC'],
                "200GBase-FR4":['25G_RS_544_FEC'],
                "200GBase-SR4":['25G_RS_544_FEC'],
                "200GBase-CR4-PAM4":['25G_RS_544_FEC'],
                "100G-AUI2":['25G_RS_544_FEC'],
                "100G-AUI2-AOC-ACC":['25G_RS_544_FEC'],
                "100G-CAUI2":['25G_RS_544_FEC'],
                "100G-CAUI2-AOC-ACC":['25G_RS_544_FEC'],
                "100GBase-KR2-PAM4":['25G_RS_544_FEC'],
                "100GBase-DR":['25G_RS_528_FEC'],
                "100GBase-SR2":['25G_RS_544_FEC'],
                "100GBase-CP2":['25G_RS_544_FEC'],
                "100GBase-KR-PAM4":['25G_RS_544_FEC'],
                "100GBase-CR-PAM4":['25G_RS_544_FEC'],
                "100G-AUI4":['25G_RS_544_FEC'],
                "100G-AUI4-AOC-ACC":['25G_RS_544_FEC'],
                "100G-CAUI4":['NO_FEC','25G_RS_528_FEC'],
                "100G-CAUI4-AOC-ACC":['NO_FEC','25G_RS_528_FEC'],
                "100GBase-KR4":['25G_RS_528_FEC'],
                "100GBase-LR4":['NO_FEC'],
                "100GBase-SR4":['25G_RS_528_FEC'],
                "100GBase-CR4":['25G_RS_528_FEC'],
                "50G-AUI1":['25G_RS_544_FEC'],
                "50G-AUI1-AOC-ACC":['25G_RS_544_FEC'],
                "50GBase-KR-PAM4":['25G_RS_544_FEC'],
                "50GBase-LR":['25G_RS_544_FEC'],
                "50GBase-FR":['25G_RS_544_FEC'],
                "50GBase-SR":['25G_RS_544_FEC'],
                "50GBase-CP":['25G_RS_544_FEC'],
                "50G-AUI2":['25G_RS_544_FEC'],
                "50G-AUI2-AOC-ACC":['25G_RS_544_FEC'],
                "50G-LAUI2":['NO_FEC'],
                "50G-LAUI2-AOC-ACC":['NO_FEC'],
                "50GBase-KR2":['NO_FEC','25G_KR_FEC','25G_RS_528_FEC'],
                "50GBase-LR2":['25G_RS_528_FEC'],
                "50GBase-SR2":['25G_RS_528_FEC'],
                "50GBase-CR2":['NO_FEC','25G_KR_FEC','25G_RS_528_FEC'],
                "40G-XLAUI":['NO_FEC'],
                "40G-XLAUI-AOC-ACC":['NO_FEC'],
                "40GBase-KR4":['NO_FEC','10G_KR_FEC'],
                "40GBase-LR4":['NO_FEC'],
                "40GBase-SR4":['NO_FEC'],
                "40GBase-CR4":['NO_FEC','10G_KR_FEC'],
                "25G-AUI-C2C":['NO_FEC','25G_KR_FEC','25G_RS_528_FEC'],
                "25G-AUI-AOC-ACC":['NO_FEC','25G_KR_FEC','25G_RS_528_FEC'],
                "25GBase-KR1":['NO_FEC','25G_KR_FEC','25G_RS_528_FEC'],
                "25GBase-KR-S":['NO_FEC','25G_KR_FEC'],
                "25GBase-KR":['NO_FEC','25G_KR_FEC','25G_RS_528_FEC'],
                "25GBase-LR":['25G_RS_528_FEC'],
                "25GBase-SR":['25G_RS_528_FEC'],
                "25GBase-CR1":['NO_FEC','25G_KR_FEC','25G_RS_528_FEC'],
                "25GBase-CR-S":['NO_FEC','25G_KR_FEC'],
                "25GBase-CR":['NO_FEC','25G_KR_FEC','25G_RS_528_FEC'],
                "25GBase-T":['NO_FEC'],
                "10G-SFI-C2C":['NO_FEC'],
                "10G-SFI-AOC-ACC":['NO_FEC'],
                "10GBase-KR-CR1":['NO_FEC','10G_KR_FEC'],
                "10GBase-LR":['NO_FEC'],
                "10GBase-SR":['NO_FEC'],
                "10G-SFI-DA":['NO_FEC'],
                "10GBase-T":['NO_FEC'],
                "5GBase-KR":['NO_FEC'],
                "5GBase-T":['NO_FEC'],
                "2.5GBase-KX":['NO_FEC'],
                "2.5GBase-X":['NO_FEC'],
                "2.5GBase-T":['NO_FEC'],
                "1G-SGMII":['NO_FEC'],
                "1000Base-KX":['NO_FEC'],
                "1000Base-LX":['NO_FEC'],
                "1000Base-SX":['NO_FEC'],
                "1000Base-T":['NO_FEC'],
                "100Base-TX":['NO_FEC'],
                "100M-SGMII":['NO_FEC']}

    force_phy_types_list = ['10GBase-SR',
                            '10GBase-LR',
                            '10G-SFI-AOC-ACC',
                            '10G-SFI-C2C',
                            '10G-SFI-DA',
                            '25G-AUI-AOC-ACC',
                            '25G-AUI-C2C',
                            '25GBase-SR',
                            '25GBase-LR',
                            '50G-AUI2',
                            '50G-AUI2-AOC-ACC',
                            '50G-LAUI2',
                            '50G-LAUI2-AOC-ACC',
                            '50GBase-SR',
                            '50GBase-LR',
                            '50GBase-FR',
                            '50G-AUI1',
                            '50G-AUI1-AOC-ACC',
                            '50GBase-CP',
                            '100GBase-CP2',
                            '100GBase-LR4',
                            '100GBase-SR4',
                            '100G-AUI4',
                            '100G-AUI4-AOC-ACC',
                            '100G-CAUI4',
                            '100G-CAUI4-AOC-ACC',
                            '100GBase-SR2',
                            '100G-AUI2',
                            '100G-AUI2-AOC-ACC']


    link_stable = True
    Return_list = [0]
    debug_mode = False
    start_logger_flag = False


    # from PRTMAC_LINKSTA 0x001E47A0
    Mac_link_speed_dict = {0:"10M",
                           1:"100M",
                           2:"1G",
                           3:"2.5G",
                           4:"5G",
                           5:"10G",
                           6:"20G",
                           7:"25G",
                           8:"40G",
                           9:"50G",
                           10:"100G",
                           11:"200G"}

    Phy_link_speed_dict = {0:"N/A",
                           1:"100M",
                           2:"1G",
                           3:"2.5G",
                           4:"5G",
                           5:"10G",
                           6:"20G",
                           7:"25G",
                           8:"40G",
                           9:"50G",
                           10:"100G"}


    #TODO check if this dicts are relevant
    Mac_link_statistic_dict = {}
    Phy_link_statistic_dict = {}

    suppoted_module_technologies_dict = {0: "sfp + Cu Passive",
                                         1: "sfp + Cu Active",
                                         4: "10G BASE-SR",
                                         5: "10G BASE-LR",
                                         6: "10G BASE-LRM",
                                         7: "10G BASE-ER"}
    ########### AQ Dic ######

    ## AQ 0x600 get PHY Ability ####

    get_Ability_Phy_Type_dict = {83:"400G-AUI8",
                                 82:"400G-AUI8-AOC-ACC",
                                 81:"400GBase-DR4",
                                 80:"400GBase-LR8",
                                 79:"400GBase-FR8",
                                 78:"200G-AUI8",
                                 77:"200G-AUI8-AOC-ACC",
                                 76:"200G-AUI4",
                                 75:"200G-AUI4-AOC-ACC",
                                 74:"200GBase-KR4-PAM4",
                                 73:"200GBase-DR4",
                                 72:"200GBase-LR4",
                                 71:"200GBase-FR4",
                                 70:"200GBase-SR4",
                                 69:"200GBase-CR4-PAM4",
                                 68:"100G-AUI2",
                                 67:"100G-AUI2-AOC-ACC",
                                 66:"100G-CAUI2",
                                 65:"100G-CAUI2-AOC-ACC",
                                 64:"100GBase-KR2-PAM4",
                                 63:"100GBase-DR",
                                 62:"100GBase-SR2",
                                 61:"100GBase-CP2",
                                 60:"100GBase-KR-PAM4",
                                 59:"100GBase-CR-PAM4",
                                 58:"100G-AUI4",
                                 57:"100G-AUI4-AOC-ACC",
                                 56:"100G-CAUI4",
                                 55:"100G-CAUI4-AOC-ACC",
                                 54:"100GBase-KR4",
                                 53:"100GBase-LR4",
                                 52:"100GBase-SR4",
                                 51:"100GBase-CR4",
                                 50:"50G-AUI1",
                                 49:"50G-AUI1-AOC-ACC",
                                 48:"50GBase-KR-PAM4",
                                 47:"50GBase-LR",
                                 46:"50GBase-FR",
                                 45:"50GBase-SR",
                                 44:"50GBase-CP",
                                 43:"50G-AUI2",
                                 42:"50G-AUI2-AOC-ACC",
                                 41:"50G-LAUI2",
                                 40:"50G-LAUI2-AOC-ACC",
                                 39:"50GBase-KR2",
                                 38:"50GBase-LR2",
                                 37:"50GBase-SR2",
                                 36:"50GBase-CR2",
                                 35:"40G-XLAUI",
                                 34:"40G-XLAUI-AOC-ACC",
                                 33:"40GBase-KR4",
                                 32:"40GBase-LR4",
                                 31:"40GBase-SR4",
                                 30:"40GBase-CR4",
                                 29:"25G-AUI-C2C",
                                 28:"25G-AUI-AOC-ACC",
                                 27:"25GBase-KR1",
                                 26:"25GBase-KR-S",
                                 25:"25GBase-KR",
                                 24:"25GBase-LR",
                                 23:"25GBase-SR",
                                 22:"25GBase-CR1",
                                 21:"25GBase-CR-S",
                                 20:"25GBase-CR",
                                 19:"25GBase-T",
                                 18:"10G-SFI-C2C",
                                 17:"10G-SFI-AOC-ACC",
                                 16:"10GBase-KR-CR1",
                                 15:"10GBase-LR",
                                 14:"10GBase-SR",
                                 13:"10G-SFI-DA",
                                 12:"10GBase-T",
                                 11:"5GBase-KR",
                                 10:"5GBase-T",
                                 9:"2.5GBase-KX",
                                 8:"2.5GBase-X",
                                 7:"2.5GBase-T",
                                 6:"1G-SGMII",
                                 5:"1000Base-KX",
                                 4:"1000Base-LX",
                                 3:"1000Base-SX",
                                 2:"1000Base-T",
                                 1:"100M-SGMII",
                                 0:"100Base-TX"}

    get_Ability_EEE_dict = {10:"EEEen100GBase-KR2-PAM4",
                            9:"EEEen100GBase-KR4",
                            8:"EEEen50GBase-KR-PAM4",
                            7:"EEEen50GBase-KR2",
                            6:"EEEen40GBase-KR4",
                            5:"EEEen25GBase-KR",
                            4:"EEEen10GBase-KR",
                            3:"EEEen1000Base-KX",
                            2:"EEEen10GBase-T",
                            1:"EEEen1000Base-T",
                            0:"EEEen100Base-TX"}

    get_Ability_FEC_dict = {7:"25G_KR_FEC_abil",
                            6:"25G_RS_528_FEC_abil",
                            5:"Reserved",
                            4:"25G_RS_544_FEC_req",
                            3:"25G_KR_FEC_req",
                            2:"25G_RS_528_FEC_req",
                            1:"10G_KR_FEC_req",
                            0:"10G_KR_FEC_abil"}

    ## AQ 0x601 Set PHY config ####

    set_Ability_PhyType_dict = {"400G-AUI8":83,
                                "400G-AUI8-AOC-ACC":82,
                                "400GBase-DR4":81,
                                "400GBase-LR8":80,
                                "400GBase-FR8":79,
                                "200G-AUI8":78,
                                "200G-AUI8-AOC-ACC":77,
                                "200G-AUI4":76,
                                "200G-AUI4-AOC-ACC":75,
                                "200GBase-KR4-PAM4":74,
                                "200GBase-DR4":73,
                                "200GBase-LR4":72,
                                "200GBase-FR4":71,
                                "200GBase-SR4":70,
                                "200GBase-CR4-PAM4":69,
                                "100G-AUI2":68,
                                "100G-AUI2-AOC-ACC":67,
                                "100G-CAUI2":66,
                                "100G-CAUI2-AOC-ACC":65,
                                "100GBase-KR2-PAM4":64,
                                "100GBase-DR":63,
                                "100GBase-SR2":62,
                                "100GBase-CP2":61,
                                "100GBase-KR-PAM4":60,
                                "100GBase-CR-PAM4":59,
                                "100G-AUI4":58,
                                "100G-AUI4-AOC-ACC":57,
                                "100G-CAUI4":56,
                                "100G-CAUI4-AOC-ACC":55,
                                "100GBase-KR4":54,
                                "100GBase-LR4":53,
                                "100GBase-SR4":52,
                                "100GBase-CR4":51,
                                "50G-AUI1":50,
                                "50G-AUI1-AOC-ACC":49,
                                "50GBase-KR-PAM4":48,
                                "50GBase-LR":47,
                                "50GBase-FR":46,
                                "50GBase-SR":45,
                                "50GBase-CP":44,
                                "50G-AUI2":43,
                                "50G-AUI2-AOC-ACC":42,
                                "50G-LAUI2":41,
                                "50G-LAUI2-AOC-ACC":40,
                                "50GBase-KR2":39,
                                "50GBase-LR2":38,
                                "50GBase-SR2":37,
                                "50GBase-CR2":36,
                                "40G-XLAUI":35,
                                "40G-XLAUI-AOC-ACC":34,
                                "40GBase-KR4":33,
                                "40GBase-LR4":32,
                                "40GBase-SR4":31,
                                "40GBase-CR4":30,
                                "25G-AUI-C2C":29,
                                "25G-AUI-AOC-ACC":28,
                                "25GBase-KR1":27,
                                "25GBase-KR-S":26,
                                "25GBase-KR":25,
                                "25GBase-LR":24,
                                "25GBase-SR":23,
                                "25GBase-CR1":22,
                                "25GBase-CR-S":21,
                                "25GBase-CR":20,
                                "25GBase-T":19,
                                "10G-SFI-C2C":18,
                                "10G-SFI-AOC-ACC":17,
                                "10GBase-KR-CR1":16,
                                "10GBase-LR":15,
                                "10GBase-SR":14,
                                "10G-SFI-DA":13,
                                "10GBase-T":12,
                                "5GBase-KR":11,
                                "5GBase-T":10,
                                "2.5GBase-KX":9,
                                "2.5GBase-X":8,
                                "2.5GBase-T":7,
                                "1G-SGMII":6,
                                "1000Base-KX":5,
                                "1000Base-LX":4,
                                "1000Base-SX":3,
                                "1000Base-T":2,
                                "100M-SGMII":1,
                                "100Base-TX":0}
    #set_Ability_PhyType_dict = {83:"400G-AUI8",82:"400G-AUI8-AOC-ACC",81:"400GBase-DR4",80:"400GBase-LR8",79:"400GBase-FR8",78:"200G-AUI8",77:"200G-AUI8-AOC-ACC",76:"200G-AUI4",75:"200G-AUI4-AOC-ACC",74:"200GBase-KR4-PAM4",73:"200GBase-DR4",72:"200GBase-LR4",71:"200GBase-FR4",70:"200GBase-SR4",69:"200GBase-CR4-PAM4",68:"100G-AUI2",67:"100G-AUI2-AOC-ACC",66:"100G-CAUI2",65:"100G-CAUI2-AOC-ACC",64:"100GBase-KR2-PAM4",63:"100GBase-DR",62:"100GBase-SR2",61:"100GBase-CP2",60:"100GBase-KR-PAM4",59:"100GBase-CR-PAM4",58:"100G-AUI4",57:"100G-AUI4-AOC-ACC",56:"100G-CAUI4",55:"100G-CAUI4-AOC-ACC",54:"100GBase-KR4",53:"100GBase-LR4",52:"100GBase-SR4",51:"100GBase-CR4",50:"50G-AUI1",49:"50G-AUI1-AOC-ACC" ,48:"50GBase-KR-PAM4",47:"50GBase-LR",46:"50GBase-FR",45:"50GBase-SR",44:"50GBase-CP",43:"50G-AUI2",42:"50G-AUI2-AOC-ACC",41:"50G-LAUI2",40:"50G-LAUI2-AOC-ACC",39:"50GBase-KR2",38:"50GBase-LR2",37:"50GBase-SR2",36:"50GBase-CR2",35:"40G-XLAUI",34:"40G-XLAUI-AOC-ACC",33:"40GBase-KR4",32:"40GBase-LR4",31:"40GBase-SR4",30:"40GBase-CR4",29:"25G-AUI-C2C",28:"25G-AUI-AOC-ACC",27:"25GBase-KR1",26:"25GBase-KR-S",25:"25GBase-KR",24:"25GBase-LR",23:"25GBase-SR",22:"25GBase-CR1",21:"25GBase-CR-S",20:"25GBase-CR",19:"25GBase-T",18:"10G-SFI-C2C",17:"10G-SFI-AOC-ACC",16:"10GBase-KR-CR1",15:"10GBase-LR",14:"10GBase-SR",13:"10G-SFI-DA",12:"10GBase-T",11:"5GBase-KR",10:"5GBase-T",9:"2.5GBase-KX",8:"2.5GBase-X",7:"2.5GBase-T",6:"1G-SGMII",5:"1000Base-KX",4:"1000Base-LX",3:"1000Base-SX",2:"1000Base-T",1:"100M-SGMII",0:"100Base-TX"}

    set_Ability_EEE_dict = {"EEEen100GBase-KR2-PAM4":10,
                            "EEEen100GBase-KR4":9,
                            "EEEen50GBase-KR-PAM4":8,
                            "EEEen50GBase-KR2":7,
                            "EEEen40GBase-KR4":6,
                            "EEEen25GBase-KR":5,
                            "EEEen10GBase-KR":4,
                            "EEEen1000Base-KX":3,
                            "EEEen10GBase-T":2,
                            "EEEen1000Base-T":1,
                            "EEEen100Base-TX":0}

    set_Ability_FEC_dict = {"25GkrFECab":7,"25GrsFEC528ab":6,"Reserved":5,"25GrsFEC544req":4,"25GkrFECreq":3,"25GrsFEC528req":2,"10GkrFECreq":1,"10GkrFECen":0}

    ## AQ 0x607 Get link status response ####

    Get_Speed_Status_dict = {0:"10M",
                             1:"100M",
                             2:"1G",
                             3:"2.5G",
                             4:"5G",
                             5:"10G",
                             6:"20G",
                             7:"25G",
                             8:"40G",
                             9:"50G",
                             10:"100G",
                             11:"200G"}

    Get_Phy_Type_Status_dict = {84:"N/A",83:"400G-AUI8",82:"400G-AUI8-AOC-ACC",81:"400GBase-DR4",80:"400GBase-LR8",79:"400GBase-FR8",78:"200G-AUI8",77:"200G-AUI8-AOC-ACC",76:"200G-AUI4",75:"200G-AUI4-AOC-ACC",74:"200GBase-KR4-PAM4",73:"200GBase-DR4",72:"200GBase-LR4",71:"200GBase-FR4",70:"200GBase-SR4",69:"200GBase-CR4-PAM4",68:"100G-AUI2",67:"100G-AUI2-AOC-ACC",66:"100G-CAUI2",65:"100G-CAUI2-AOC-ACC",64:"100GBase-KR2-PAM4",63:"100GBase-DR",62:"100GBase-SR2",61:"100GBase-CP2",60:"100GBase-KR-PAM4",59:"100GBase-CR-PAM4",58:"100G-AUI4",57:"100G-AUI4-AOC-ACC",56:"100G-CAUI4",55:"100G-CAUI4-AOC-ACC",54:"100GBase-KR4",53:"100GBase-LR4",52:"100GBase-SR4",51:"100GBase-CR4",50:"50G-AUI1",49:"50G-AUI1-AOC-ACC" ,48:"50GBase-KR-PAM4",47:"50GBase-LR",46:"50GBase-FR",45:"50GBase-SR",44:"50GBase-CP",43:"50G-AUI2",42:"50G-AUI2-AOC-ACC",41:"50G-LAUI2",40:"50G-LAUI2-AOC-ACC",39:"50GBase-KR2",38:"50GBase-LR2",37:"50GBase-SR2",36:"50GBase-CR2",35:"40G-XLAUI",34:"40G-XLAUI-AOC-ACC",33:"40GBase-KR4",32:"40GBase-LR4",31:"40GBase-SR4",30:"40GBase-CR4",29:"25G-AUI-C2C",28:"25G-AUI-AOC-ACC",27:"25GBase-KR1",26:"25GBase-KR-S",25:"25GBase-KR",24:"25GBase-LR",23:"25GBase-SR",22:"25GBase-CR1",21:"25GBase-CR-S",20:"25GBase-CR",19:"25GBase-T",18:"10G-SFI-C2C",17:"10G-SFI-AOC-ACC",16:"10GBase-KR-CR1",15:"10GBase-LR",14:"10GBase-SR",13:"10G-SFI-DA",12:"10GBase-T",11:"5GBase-KR",10:"5GBase-T",9:"2.5GBase-KX",8:"2.5GBase-X",7:"2.5GBase-T",6:"1G-SGMII",5:"1000Base-KX",4:"1000Base-LX",3:"1000Base-SX",2:"1000Base-T",1:"100M-SGMII",0:"100Base-TX"}

    get_Link_Status1_dict = {7:'Signal Detect',6:'Media Available',5:'External port link Up',4:'Remote fault',3:'Receiver link fault',2:'Transmitter link fault',1:'Phy has Detect a link Fault',0:'Link Up'}
    get_Link_Status2_dict = {7:'QualifiedModule',6:'Link_Pause_Status_TX',5:'Link_Pause_Status_TX',4:'Low_Power_state',3:'FEC_Enabled',2:'Parallel_detection_ Fault',1:'LP_AN_Ability',0:'AN_Completed'}
    get_FEC_Status_dict = {0:'10G_KR_FEC',1:'25G_KR_FEC',2:'25G_RS_528_FEC',3:'25G_RS_544_FEC'}

    ## GetPhyLinkStatus Mapping
    quad_for_2_ports_dict = {0:0,1:1}# key=pf : value=quad
    quad_for_4_ports_dict = {0:0,1:0,2:1,3:1}# key=pf : value=quad
    quad_for_4_ports_mux_dict = {0:0,1:1,2:0,3:1}# key=pf : value=quad
    quad_for_8_ports_dict = {0:0,1:0,2:0,3:0,4:1,5:1,6:1,7:1}# key=pf : value=quad
    pmd_num_for_2_ports_dict = {0:0,1:0}# key=pf,value=pmd_num according the netlist
    pmd_num_for_4_ports_dict = {0:0,1:1,2:0,3:1}# key=pf,value=pmd_num according the netlist
    pmd_num_for_4_ports_mux_dict = {0:0,1:0,2:1,3:1}# key=MAC number,value=pmd_num according the netlist
    pmd_num_for_8_ports_dict = {0:0,1:0,2:1,3:1,4:2,5:2,6:3,7:3}# key=pf,value=pmd_num according the netlist

    # GetPhyTuningParams proclib
    Phy_tuning_params_dict = {"RxFFE_pre2" : 0x1000, "RxFFE_pre1" : 0x1100, "RxFFE_post1" : 0x1200, "RxFFE_Bflf" : 0x1300, "RxFFE_Bfhf" : 0x1400, "CTLE_HF" : 0x2000, "CTLE_LF" : 0x2100, "CTLE_DC" : 0x2200, "CTLE_BW" : 0x2300, "CTLE_gs1" : 0x2400, "CTLE_gs2" : 0x2500, "DFE_GAIN" : 0x3000, "DFE_GAIN2" : 0x3100, "DFE_2" : 0x3200, "DFE_3" : 0x3300, "DFE_4" : 0x3400, "DFE_5" : 0x3500, "DFE_6" : 0x3600, "DFE_7" : 0x3700, "DFE_8" : 0x3800, "DFE_9" : 0x3900, "DFE_A" : 0x3A00, "DFE_B" : 0x3B00, "DFE_C" : 0x3C00, "Eye height_thle" : 0x4000, "Eye height_thme" : 0x4100, "Eye height_thue" : 0x4200, "Eye height_thlo" : 0x4300, "Eye height_thmo" : 0x4400, "Eye height_thuo" : 0x4500}

    Serdes_mapping_per_pf_2_ports = {0:0,1:4}# key=pf : value=serdes number according CVL port mapping 3.4.2.3.2
    Serdes_mapping_per_pf_4_ports = {0:0,1:1,2:4,3:5}# key=pf : value=serdes number according CVL port mapping 3.4.2.3.2
    Serdes_mapping_per_pf_4_ports_mux = {0:0,1:1,2:2,3:3} # key=pf : value=serdes number according CVL port mapping 3.4.2.3.2
    Serdes_mapping_per_pf_8_ports = {0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7}# key=pf : value=serdes number according CVL port mapping 3.4.2.3.2

    NRZ_100G_phytype_list = ['100G-AUI4','100G-AUI4-AOC/ACC','100G-CAUI4','100G-CAUI4-AOC/ACC','100GBase-KR4','100GBase-LR4','100GBase-SR4','100GBase-CR4']
    PAM4_100G_phytype_list = ['100GBase-KR2-PAM4','100GBase-DR','100GBase-SR2','100GBase-CP2','100GBase-KP-PAM4']
    NRZ_50G_phytype_list = ['50G-AUI2','50G-AUI2-AOC/ACC','50G-LAUI2','50G-LAUI2-AOC/ACC','50GBase-KR2','50GBase-CR2']

    serdeses_per_portnum_2_dict = {0:[0,1],1:[4,5]}
    serdeses_per_portnum_4_dict = {0:[0,1,2,3],1:[4,5,6,7]}


    #print cvl info
    MTIP_10_25_40_50_PCS_Quad_0_Addr_Dict = {0:0x40,1:0x41,2:0x42,3:0x43}# PCS number according to pmd num
    MTIP_10_25_40_50_PCS_Quad_1_Addr_Dict = {0:0x50,1:0x51,2:0x52,3:0x53}# PCS number according to pmd num
    MTIP_100_PCS_Addr_Dict = {0:0x31,1:0x32}# PCS number according to quad num

    MTIP_FEC_PCS_addr_dict = {0:0x33,1:0x34}# PCS number according to quad num

    # advenced pcs info
    pcs_link_status_2_dict = {5: "100GBase-R capable", 4: "40GBase-R capable", 3: "10GBase-T capable", 2: "10GBase-W capable", 1: "10GBase-X capable", 0: "10GBase-R capable"}

    # PM PSTO 
    PRT_AN_TRACKING = {31:'',30:'',29:'',28:'',27:'',26:'',25:'',24:'AN Process Started',23:'',22:'',21:'',20:'Nextpage EEE Recent',19:'Basepage RX Flag',18:'NP RX',17:'',16:'',15:'CONS 25/50 #2',14:'CONS 25/50 #1',13:'EEE',12:'NP SENT',11:'',10:'',9:'CONS 25/50 #2',8:'CONS 25/50 #1',7:'EEE',6:'',5:'NP SUPPORTED',4:'',3:'',2:'CONS 25/50 #2',1:'CONS 25/50 #1',0:'EEE'}
    PRT_AN_HCD_OUTPUT_dict = {24:'PHY Type Index bit 1', 31:'PHY Type Index bit 8', 30:'PHY Type Index bit 7', 29:'PHY Type Index bit 6', 28:'PHY Type Index bit 5', 27:'PHY Type Index bit 4', 26:'PHY Type Index bit 3', 25:'PHY Type Index bit 2', 24:'PHY Type Index bit 1', 23:'KR-S/CR-S', 22:'Consortium', 20:'EEE', 17:'FEC Select bit 2', 16:'FEC Select bit 2', 15:'FEC Select bit 1', 12:'Backplane Link', 11:'Reserved', 10:'Reserved', 9:'100GBase-CR2/KR2', 8:'50GBase-CR/KR', 7:'50GBase-CR2 / KR2', 6:'25GBase-CR / KR', 5:'100GBase-CR4', 4:'100GBase-KR4', 3:'Reserved', 2:'Reserved', 1:'10GBase-KR', 0:'1000Base-KX'}# 32 temp until we can to translte more that 1 bit
    FEC_select_dict = {7:'reserved',6:'reserved',5:'reserved',4:'reserved',3:'RS-FEC 528',2:'RS-FEC 544',1:'BaseR-FEC',0:'No FEC'}
    PRT_AN_LP_NP_dict = {16:'EEEen100GBase-KR2-PAM4', 15:'EEEen100GBase-KR4', 14:'EEEen50GBase-KR-PAM4', 13:'EEEen50GBase-KR2', 12:'Reserved', 11:'EEEen25GBase-KR', 10:'EEEen10GBase-KR', 9:'EEEen1000Base-KX', 7:'requests Clause 74 FEC', 6:'requests Clause 91 FEC', 5:'advertises Clause 74 FEC ability', 4:'advertises Clause 91 FEC ability', 3:'50GBase-CR2', 2:'50GBase-KR2', 1:'25GBase-CR1', 0:'25GBase-KR1'}
    PRT_AN_LP_BP_dict = {21:'Pause - C1', 20:'Pause - C0', 19:'NP', 18:'10 Gb/s per lane FEC requested', 17:'10 Gb/s per lane FEC ability', 16:'25G BASE-R FEC requested', 15:'25G RS-FEC requested', 14:'100GBASE-KR2/CR2', 13:'50GBASE-KR/CR', 12:'5GBASE-KR', 11:'2.5GBASE-KX', 10:'25GBASE-KR/CR', 9:'25GBASE-KR-S/CR-S', 8:'100GBASE-CR4', 7:'100GBASE-KR4', 6:'100GBASE-KP4', 5:'100GBASE-CR10', 4:'40GBASE-CR4', 3:'40GBASE-KR4', 2:'10GBASE-KR', 1:'10GBASE-KX4', 0:'1000Base-KX'}
    PRT_AN_LOCAL_NP_dict = {16:'EEEen100GBase-KR2-PAM4', 15:'EEEen100GBase-KR4', 14:'EEEen50GBase-KR-PAM4', 13:'EEEen50GBase-KR2', 12:'Reserved', 11:'EEEen25GBase-KR', 10:'EEEen10GBase-KR', 9:'EEEen1000Base-KX', 7:'requests Clause 74 FEC', 6:'requests Clause 91 FEC', 5:'advertises Clause 74 FEC ability', 4:'advertises Clause 91 FEC ability', 3:'50GBase-CR2', 2:'50GBase-KR2', 1:'25GBase-CR1', 0:'25GBase-KR1'}
    PRT_AN_LOCAL_BP_dict = {21:'Pause - C1', 20:'Pause - C0', 19:'NP', 18:'10 Gb/s per lane FEC requested', 17:'10 Gb/s per lane FEC ability', 16:'25G BASE-R FEC requested', 15:'25G RS-FEC requested', 14:'100GBASE-KR2/CR2', 13:'50GBASE-KR/CR', 12:'5GBASE-KR', 11:'2.5GBASE-KX', 10:'25GBASE-KR/CR', 9:'25GBASE-KR-S/CR-S', 8:'100GBASE-CR4', 7:'100GBASE-KR4', 6:'100GBASE-KP4', 5:'100GBASE-CR10', 4:'40GBASE-CR4', 3:'40GBASE-KR4', 2:'10GBASE-KR', 1:'10GBASE-KX4', 0:'1000Base-KX'}
    PRT_STATE_MACHINE_AN = {0x28:'AutonegTOP when WAIT_FOR_INT after serdes configuration done',0x14:'AutonegTOP when Determine link mode starts',0xA:'AutonegTOP when WAIT_FOR_INT / Interrupt Handling starts',5:'AutonegTOP when Config PHY for AN starts',1:'AutonegTOP before Init PHY'}
    PRT_STATE_MACHINE_FM = {0x1E:'exit set_pmd_link_up once called from other activity',0x14:'Wait for link up indication',0xA:'Setup SOW done, wait for signal OK ',1:'ForcedModeTOP'}

class cvl_structs:

	def SbIosfMassageStruct(self):
		Massage = {}
		Massage['dest'] = 0
		Massage['source'] = 0
		Massage['opcode'] = 0
		Massage['Tag'] = 0
		Massage['Bar'] = 0
		Massage['addrlen'] = 0
		Massage['EH'] = 0
		Massage['exphdrid'] = 0
		Massage['EH_2ndDW'] = 0
		Massage['sai'] = 0
		Massage['rs'] = 0
		Massage['fbe'] = 0
		Massage['Sbe'] = 0
		Massage['Fid'] = 0
		Massage['address'] = 0
		Massage['address_4thDW'] = 0
		return Massage

#TODO implement a new calss that holds these values as class member and not as instance members
class AqOpCodes:
    def __init__(self):
        #General Admin Commands
        self.get_version = 0x0001
        self.get_err_reason = 0x0005
        #Diagnostic and Debug Admin commands
        #Defined in CPK HAS Section 16.3
        self.config_fw_logging = 0xFF09
        self.get_fw_log = 0xFF11
        #Link Configuration Admin command OpCodes
        #Defined in CPK HAS Section 3.4.5
        self.set_phy_config = 0x0601
        self.set_mac_config = 0x0603
        self.setup_link = 0x0605
        self.get_phy_abilities = 0x0600
        self.get_link_status = 0x0607
        self.set_event_mask = 0x0613
        self.set_phy_loopback = 0x0619
        self.set_mac_loopback = 0x0620
        self.set_phy_debug = 0x0622
        #Link Topology Admin command OpCodes
        #Defined in CPK HAS Section 3.5.10
        self.get_link_topology_handle = 0x06E0
        self.get_link_topology_pin = 0x06E1
        self.read_i2c = 0x06E2
        self.write_i2c = 0x06E3
        self.read_mdio = 0x06E4
        self.write_mdio = 0x06E5
        self.set_gpio_by_function = 0x06E6
        self.get_gpio_by_function = 0x06E7
        self.set_gpio = 0x06EC
        self.get_gpio = 0x06ED
        self.set_led = 0x06E8
        self.set_port_id_led = 0x06E9
        self.get_port_options = 0x06EA
        self.set_port_option = 0x06EB
        #DNL Debug Admin command Opcodes
        #Defined in CPK HAS Appendix C Section 2
        self.dnl_get_status = 0x0680
        self.dnl_run = 0x0681
        self.dnl_call = 0x0682
        self.dnl_read_sto = 0x0683
        self.dnl_write_sto = 0x0684
        self.dnl_set_breakpoints = 0x0686
        self.dnl_read_log = 0x0687


