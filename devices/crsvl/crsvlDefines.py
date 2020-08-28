from crsvlBase import crsvlBase

class crsvlDefines(crsvlBase):

    link_stable = True
    Return_list = [0]
    debug_mode = False

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



    ########### AQ Dic ######

    ## AQ 0x601 Set PHY config ####

    Set_PhyType_dict = {31:'empty',30:'20GBASE-KR2',29:'1000BASE-T-OPTICAL',28:'1000BASE-LX',27:'1000BASE-SX',26:'40GBASE-LR4',25:'40GBASE-SR4',24:'40GBASE-CR4',23:'10GBASE-CR1',22:'10GBASE-SFP+Cu',21:'10GBASE-LR',20:'10GBASE-SR',19:'10GBASE-T',18:'1000BASE-T',17:'100BASE-T',16:'empty',15:'empty',14:'empty',13:'empty',12:'empty',11:'10GBASE-CR1',10:'40GBASE-CR4',9:'XLPPI',8:'XLAUI',7:'SFI',6:'XFI',5:'XAUI',4:'40GBASE-KR4',3:'10GBASE-KR',2:'10GBASE-KX4',1:'1000BASE-KX',0:'SGMII'}

    #set_Ability_Link_dict = {23:'40G-KR4',22:'EEE 10GBASE-KR',21:'EEE 10GBASE-KX4',20:'EEE 1000BASE-KX',19:'EEE 10GBASE-T',18:'EEE  1000BASE-T',17:'EEE 100BASE-TX',16:'empty',15:'empty',14:'empty',13:'Enable Atomic Link',12:'Enable AN',11:'Enable Link',10:'Low power',9:'Rx link pause',8:'Tx link puse',7:'empty',6:'25G',5:'20G',4:'40G',3:'10G',2:'1G',1:'100M',0:'empty'}


    #phy types names must comlie with ieee 802.3
    get_Ability_PhyTypeExtension_dict = {0 : '25GBase-KR',
                                         1 : '25GBase-CR',
                                         2 : '25GBase-SR',
                                         3 : '25GBase-LR',
                                         4 : '25G-AOC',
                                         5 : '25G-ACC',
                                         6 : '2.5GBase-T',
                                         7 : '5GBase-T'}

    get_Ability_PhyType_dict = {31:'empty',30:'20GBASE-KR2',29:'1000BASE-T-OPTICAL',28:'1000BASE-LX',27:'1000BASE-SX',26:'40GBASE-LR4',25:'40GBASE-SR4',24:'40GBASE-CR4',23:'10GBASE-CR1',22:'10GBASE-SFP+Cu',21:'10GBASE-LR',20:'10GBASE-SR',19:'10GBASE-T',18:'1000BASE-T',17:'empty',16:'empty',15:'empty',14:'empty',13:'empty',12:'empty',11:'10GBASE-CR1',10:'40GBASE-CR4',9:'XLPPI',8:'XLAUI',7:'SFI',6:'XFI',5:'XAUI',4:'40GBASE-KR4',3:'10GBASE-KR',2:'10GBASE-KX4',1:'1000BASE-KX',0:'SGMII'}

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
