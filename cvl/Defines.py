import sys
import os
###################
link_stable = True
Return_list = [0]
debug_mode = False
start_logger_flag = False


# from PRTMAC_LINKSTA 0x001E47A0
Mac_link_speed_dict = {0:"10M",1:"100M",2:"1G",3:"2.5G",4:"5G",5:"10G",6:"20G",7:"25G",8:"40G",9:"50G",10:"100G",11:"200G"}
Phy_link_speed_dict = {0:"N/A",1:"100M",2:"1G",3:"2.5G",4:"5G",5:"10G",6:"20G",7:"25G",8:"40G",9:"50G",10:"100G"}


#TODO check if this dicts relevant for CVL_eth
Mac_link_statistic_dict = {}
Phy_link_statistic_dict = {}

########### AQ Dic ######

## AQ 0x600 get PHY Ability ####

get_Ability_Phy_Type_dict = {83:"400G-AUI8",82:"400G-AUI8-AOC-ACC",81:"400GBase-DR4",80:"400GBase-LR8",79:"400GBase-FR8",78:"200G-AUI8",77:"200G-AUI8-AOC-ACC",76:"200G-AUI4",75:"200G-AUI4-AOC-ACC",74:"200GBase-KR4-PAM4",73:"200GBase-DR4",72:"200GBase-LR4",71:"200GBase-FR4",70:"200GBase-SR4",69:"200GBase-CR4-PAM4",68:"100G-AUI2",67:"100G-AUI2-AOC-ACC",66:"100G-CAUI2",65:"100G-CAUI2-AOC-ACC",64:"100GBase-KR2-PAM4",63:"100GBase-DR",62:"100GBase-SR2",61:"100GBase-CP2",60:"100GBase-KR-PAM4",59:"100GBase-CR-PAM4",58:"100G-AUI4",57:"100G-AUI4-AOC-ACC",56:"100G-CAUI4",55:"100G-CAUI4-AOC-ACC",54:"100GBase-KR4",53:"100GBase-LR4",52:"100GBase-SR4",51:"100GBase-CR4",50:"50G-AUI1",49:"50G-AUI1-AOC-ACC" ,48:"50GBase-KR-PAM4",47:"50GBase-LR",46:"50GBase-FR",45:"50GBase-SR",44:"50GBase-CP",43:"50G-AUI2",42:"50G-AUI2-AOC-ACC",41:"50G-LAUI2",40:"50G-LAUI2-AOC-ACC",39:"50GBase-KR2",38:"50GBase-LR2",37:"50GBase-SR2",36:"50GBase-CR2",35:"40G-XLAUI",34:"40G-XLAUI-AOC-ACC",33:"40GBase-KR4",32:"40GBase-LR4",31:"40GBase-SR4",30:"40GBase-CR4",29:"25G-AUI-C2C",28:"25G-AUI-AOC-ACC",27:"25GBase-KR1",26:"25GBase-KR-S",25:"25GBase-KR",24:"25GBase-LR",23:"25GBase-SR",22:"25GBase-CR1",21:"25GBase-CR-S",20:"25GBase-CR",19:"25GBase-T",18:"10G-SFI-C2C",17:"10G-SFI-AOC-ACC",16:"10GBase-KR-CR1",15:"10GBase-LR",14:"10GBase-SR",13:"10G-SFI-DA",12:"10GBase-T",11:"5GBase-KR",10:"5GBase-T",9:"2.5GBase-KX",8:"2.5GBase-X",7:"2.5GBase-T",6:"1G-SGMII",5:"1000Base-KX",4:"1000Base-LX",3:"1000Base-SX",2:"1000Base-T",1:"100M-SGMII",0:"100Base-TX"}
get_Ability_EEE_dict = {10:"EEEen100GBase-KR2-PAM4",9:"EEEen100GBase-KR4",8:"EEEen50GBase-KR-PAM4",7:"EEEen50GBase-KR2",6:"EEEen40GBase-KR4",5:"EEEen25GBase-KR",4:"EEEen10GBase-KR",3:"EEEen1000Base-KX",2:"EEEen10GBase-T",1:"EEEen1000Base-T",0:"EEEen100Base-TX"}
get_Ability_FEC_dict = {7:"25G_KR_FEC_abil",6:"25G_RS_528_FEC_abil",5:"Reserved",4:"25G_RS_544_FEC_req",3:"25G_KR_FEC_req",2:"25G_RS_528_FEC_req",1:"10G_KR_FEC_req",0:"10G_KR_FEC_abil"}







## AQ 0x601 Set PHY config ####

set_Ability_PhyType_dict = {"400G-AUI8":83,"400G-AUI8-AOC-ACC":82,"400GBase-DR4":81,"400GBase-LR8":80,"400GBase-FR8":79,"200G-AUI8":78,"200G-AUI8-AOC-ACC":77,"200G-AUI4":76,"200G-AUI4-AOC-ACC":75,"200GBase-KR4-PAM4":74,"200GBase-DR4":73,"200GBase-LR4":72,"200GBase-FR4":71,"200GBase-SR4":70,"200GBase-CR4-PAM4":69,"100G-AUI2":68,"100G-AUI2-AOC-ACC":67,"100G-CAUI2":66,"100G-CAUI2-AOC-ACC":65,"100GBase-KR2-PAM4":64,"100GBase-DR":63,"100GBase-SR2":62,"100GBase-CP2":61,"100GBase-KR-PAM4":60,"100GBase-CR-PAM4":59,"100G-AUI4":58,"100G-AUI4-AOC-ACC":57,"100G-CAUI4":56,"100G-CAUI4-AOC-ACC":55,"100GBase-KR4":54,"100GBase-LR4":53,"100GBase-SR4":52,"100GBase-CR4":51,"50G-AUI1":50,"50G-AUI1-AOC-ACC":49,"50GBase-KR-PAM4":48,"50GBase-LR":47,"50GBase-FR":46,"50GBase-SR":45,"50GBase-CP":44,"50G-AUI2":43,"50G-AUI2-AOC-ACC":42,"50G-LAUI2":41,"50G-LAUI2-AOC-ACC":40,"50GBase-KR2":39,"50GBase-LR2":38,"50GBase-SR2":37,"50GBase-CR2":36,"40G-XLAUI":35,"40G-XLAUI-AOC-ACC":34,"40GBase-KR4":33,"40GBase-LR4":32,"40GBase-SR4":31,"40GBase-CR4":30,"25G-AUI-C2C":29,"25G-AUI-AOC-ACC":28,"25GBase-KR1":27,"25GBase-KR-S":26,"25GBase-KR":25,"25GBase-LR":24,"25GBase-SR":23,"25GBase-CR1":22,"25GBase-CR-S":21,"25GBase-CR":20,"25GBase-T":19,"10G-SFI-C2C":18,"10G-SFI-AOC-ACC":17,"10GBase-KR-CR1":16,"10GBase-LR":15,"10GBase-SR":14,"10G-SFI-DA":13,"10GBase-T":12,"5GBase-KR":11,"5GBase-T":10,"2.5GBase-KX":9,"2.5GBase-X":8,"2.5GBase-T":7,"1G-SGMII":6,"1000Base-KX":5,"1000Base-LX":4,"1000Base-SX":3,"1000Base-T":2,"100M-SGMII":1,"100Base-TX":0}
#set_Ability_PhyType_dict = {83:"400G-AUI8",82:"400G-AUI8-AOC-ACC",81:"400GBase-DR4",80:"400GBase-LR8",79:"400GBase-FR8",78:"200G-AUI8",77:"200G-AUI8-AOC-ACC",76:"200G-AUI4",75:"200G-AUI4-AOC-ACC",74:"200GBase-KR4-PAM4",73:"200GBase-DR4",72:"200GBase-LR4",71:"200GBase-FR4",70:"200GBase-SR4",69:"200GBase-CR4-PAM4",68:"100G-AUI2",67:"100G-AUI2-AOC-ACC",66:"100G-CAUI2",65:"100G-CAUI2-AOC-ACC",64:"100GBase-KR2-PAM4",63:"100GBase-DR",62:"100GBase-SR2",61:"100GBase-CP2",60:"100GBase-KR-PAM4",59:"100GBase-CR-PAM4",58:"100G-AUI4",57:"100G-AUI4-AOC-ACC",56:"100G-CAUI4",55:"100G-CAUI4-AOC-ACC",54:"100GBase-KR4",53:"100GBase-LR4",52:"100GBase-SR4",51:"100GBase-CR4",50:"50G-AUI1",49:"50G-AUI1-AOC-ACC" ,48:"50GBase-KR-PAM4",47:"50GBase-LR",46:"50GBase-FR",45:"50GBase-SR",44:"50GBase-CP",43:"50G-AUI2",42:"50G-AUI2-AOC-ACC",41:"50G-LAUI2",40:"50G-LAUI2-AOC-ACC",39:"50GBase-KR2",38:"50GBase-LR2",37:"50GBase-SR2",36:"50GBase-CR2",35:"40G-XLAUI",34:"40G-XLAUI-AOC-ACC",33:"40GBase-KR4",32:"40GBase-LR4",31:"40GBase-SR4",30:"40GBase-CR4",29:"25G-AUI-C2C",28:"25G-AUI-AOC-ACC",27:"25GBase-KR1",26:"25GBase-KR-S",25:"25GBase-KR",24:"25GBase-LR",23:"25GBase-SR",22:"25GBase-CR1",21:"25GBase-CR-S",20:"25GBase-CR",19:"25GBase-T",18:"10G-SFI-C2C",17:"10G-SFI-AOC-ACC",16:"10GBase-KR-CR1",15:"10GBase-LR",14:"10GBase-SR",13:"10G-SFI-DA",12:"10GBase-T",11:"5GBase-KR",10:"5GBase-T",9:"2.5GBase-KX",8:"2.5GBase-X",7:"2.5GBase-T",6:"1G-SGMII",5:"1000Base-KX",4:"1000Base-LX",3:"1000Base-SX",2:"1000Base-T",1:"100M-SGMII",0:"100Base-TX"}

set_Ability_EEE_dict = {"EEEen100GBase-KR2-PAM4":10,"EEEen100GBase-KR4":9,"EEEen50GBase-KR-PAM4":8,"EEEen50GBase-KR2":7,"EEEen40GBase-KR4":6,"EEEen25GBase-KR":5,"EEEen10GBase-KR":4,"EEEen1000Base-KX":3,"EEEen10GBase-T":2,"EEEen1000Base-T":1,"EEEen100Base-TX":0}
set_Ability_FEC_dict = {"25GkrFECab":7,"25GrsFEC528ab":6,"Reserved":5,"25GrsFEC544req":4,"25GkrFECreq":3,"25GrsFEC528req":2,"10GkrFECreq":1,"10GkrFECen":0}

## AQ 0x607 Get link status response ####

Get_Speed_Status_dict = {0:"10M",1:"100M",2:"1G",3:"2.5G",4:"5G",5:"10G",6:"20G",7:"25G",8:"40G",9:"50G",10:"100G",11:"200G"}
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



		
class AqOpCodes():
    set_phy_loopback = 0x0619
    get_link_status = 0x0607

class LM_Validation:
    '''
        This class will contain many of the smaller helper functions needed by LM Validation
        It will also read in information from the setup and support directory of the LM Validation
        deployment, this way the code can be run on many machines with minimal setup issues.
    '''

    def __init__(self, dbg_en=False):
        self.debug_on = dbg_en #Enable this for debug prints, disable this to remove them.
        self._debug('Initializing Helper Class')
        #self.env_key = 'LM_Validation' #DEPRICATED, no longer using environment variables to build paths
        ## Setup file that contains general setup configuration info
        self.setup_fn = 'lm_setup.txt'
        #self.support_path = os.getenv(self.env_key) #DEPRICATED, no longer using environment variables to build paths
        if sys.platform == 'win32': ##Path where the support files live, location depends on Windows or Linux system
            self.support_path = 'C:\\performance\\proclibs\\cpk\\a0\\support'
        elif sys.platform == 'linux2':
            usr = os.getlogin()
            self.support_path = '/home/' + usr + '/performance/proclibs/cpk/a0/support'
        #self.support_path = os.getenv(self.env_key) #DEPRICATED, no longer using environment variables to build paths
        #self._check_environment_variable() #DEPRICATED, no longer using environment variables to build paths
        ## Dictionary of information collected from the setup_fn
        self.setup = self.GetSetupInfo()
        ## Version of the validation code
        self.validation_version = self.setup['version']
        self.project = self.setup['project']
        self.target = self.setup['target']
        self.test_environment = self.setup['test_environment']
        self.activity_id_file = self.setup['act_id_file']
        self.cookbook_file = self.setup['cookbook']
        self.sven_header_file = self.setup['sven_header_file']
        #self.test_case_location = self.setup['test_case_location']
        self.activity_ids = self.ImportActIDs()
        self.opcodes = AqOpCodes()
        self._import_tests()
        self._import_media()
        self.netlist_defines = Netlist_Defines()
        self._debug('Successfully initialized helper class')
    
    def _check_environment_variable(self):
        '''
        This function verifies that the environment variables have been set as expected
        DEPRICATED:  Not used to simplify integration with standard performance environment
        '''
        win_sup_path = 'C:\\performance\\proclibs\\cpk\\a0\\support'
        linux_sup_path = '/home/laduser/performance/proclibs/cpk/a0/support'
        if sys.platform == 'win32':
            if self.support_path != win_sup_path:
                self._debug('Environment Variable not set correctly')
                self._debug('Set a system environment variable named LM_Validation')
                self._debug(self.support_path)
                self._debug('The value should be C:\\performance\\proclibs\\cpk\\a0\\support\\')
            else:
                return
        elif sys.platform == 'linux2':
            if self.support_path != linux_sup_path:
                self._debug('Environment Variable not set correctly')
                self._debug('Set a system environment variable named LM_Validation')
                self._debug(self.support_path)
                self._debug('The value should be /home/laduser/performance/proclibs/cpk/a0/support')
            else:
                return
    
    def GetSetupInfo(self):
        '''
        Function to parse in the information from the setup file (performance\proclibs\cpk\a0\support\lm_setup.txt)
        '''
        self._debug('Getting Setup Information')
        setup_file = os.path.join(self.support_path, self.setup_fn)
        f = open(setup_file, 'r')
        setup_contents = f.read()
        l = setup_contents.split('\n')
        keys = []
        values = []
        dict = {}
        for item in l:
            try:
                keys.append(item.split('=')[0])
            except:
                pass
            try:
                values.append(item.split('=')[1])
            except:
                pass
        for index, item in enumerate(keys):
            try:
                dict[item] = values[index]
            except:
                pass
        return dict
        
    def ImportActIDs(self):
        '''
        Function to read in the XML metadata file generated by the DNL compiler
        and return a dictionary of {'activity name': activity_id} key value pairs.
        input:
            metadata_xml -- Filepath to the xml file that should be parsed
        return:
            activity_ids -- dict{'string' : int} of activity names and activity IDs
        '''
        tree = ET.parse(os.path.join(self.support_path, self.activity_id_file))
        root = tree.getroot()
        iter = 0
        activity_ids = {}
        for child in root:
            id_name = root[iter][0].text
            id_num = int(root[iter][1].text)
            activity_ids[id_name] = id_num
            iter += 1
            
        return activity_ids
    
    def GetActivityID(self,act_name):
        '''
        This function returns the activity ID of the provided activity name from
        target XML compiler output
        inputs:
            act_name -- String name of the activity
            compiler_xml -- filepath of the target XML from the compiler output
        return:
            activity_id -- integer representing the Activity ID of the requested DNL Activity
        '''
        act_ids = self.ImportActIDs()
        return act_ids[act_name]

    def _get_cookbook(self):
        '''
        returns the filepath to the cookbook.xml
        '''
        return os.path.join(self.support_path, self.cookbook_file)

    def _import_tests(self):
        '''
            This function will import the tests.json file contents
        '''
        self._debug('Importing Test Info')
        if (self.test_environment == 'development'):
            self.test = json.load(open(os.path.join(self.support_path, 'dev_test.json')))
        elif (self.test_environment == 'demo'):
            self.test = json.load(open(os.path.join(self.support_path, 'demo.json')))
        elif (self.test_environment == 'bat.json'):
            self.test = json.load(open(os.path.join(self.support_path, 'bat.json')))
        elif (self.test_environment == 'cpk'):
            self.test = json.load(open(os.path.join(self.support_path, 'master_test.json'))) #TODO:  Change master to cpk_test.json
        elif (self.test_environment == 'cvl'):
            self.test = json.load(open(os.path.join(self.support_path, 'cvl_test.json')))
        else:
            self._debug('Unknown test environment')
        self._debug('Successfully imported test info')
        
    def _import_media(self):
        '''
            This function will import the media.json file contents
        '''
        self._debug('Importing Media Info')
        self.media = json.load(open(os.path.join(self.support_path, 'media.json')))
        self._debug('Successfully imported media Info')
        
    def _get_test(self,id):
        '''
            This function will return the inputs & returns for a given test id
        '''
        inputs, returns = self.test[str(id)]['inputs'], self.test[str(id)]['returns']
        if inputs:
            for key in inputs.keys():
                inputs[key] = int(inputs[key])
        if returns:
            for key in returns.keys():
                returns[key] = int(returns[key])
        return inputs, returns
        
    def _get_media_info(self,sn):
        '''
            This function will return the media info of a given media serial number
                input:
                    sn - type(int | str) serial number of the media
                return:
                    media_info -- type(dict)
                        supported_fec_modes(list of dicts)
                            {'fec_mode' : 'mode'}
                        supported_link_modes(list of dicts)
                            {'link_mode' : str}
                        'description' : 'str'
                        'type' : 'str
                        'manufacturer_pn' : 'str'
                        'serial' : 'str'
        '''
        return self.media[str(sn)]
    
    def _get_test_type(self,id):
        '''
            This function will return the Admin command or Activity type stored in the 
            Test Case 'Activity' field
        '''
        return str(self.test[str(id)]['activity'])
    
    def _si_runtime_data(self,stats):
        '''
        input(1)
            dict -- response from the test scripts
                caches
                iosf transactions
                mdio clocks
                i2c clocks
                
                execution runtime
        returns(1)
            estimated execution time in silicon
        '''
        fpga_cache_scalar = 0.001/(1.0/(8333333.0)*(5.0+64.0*6.0)*8.0) #Matches Excel
        fpga_cache = stats['cache']*(1.0/(fpga_cache_scalar*1000.0)) #Matches Excel
        fpga_iosf = stats['iosf']*(1.0/(1000.0*1000.0)) #Matches Excel
        fpga_mdio = stats['mdio']*(1.0/(500.0*1000.0)) #Matches Excel
        fpga_i2c = stats['i2c']*(1.0/(100.0*1000.0)) #Matches Excel
        fpga_cpu_time = (stats['runtime']/1000000.0) - fpga_cache - fpga_iosf - fpga_mdio - fpga_i2c #Matches Excel
        
        si_cache_scalar = 0.001/(1.0/50000000.0*(5.0+64.0*6.0)*8.0/4.0) #Mostly matches Excel
        si_cache = stats['cache']*(1.0/(si_cache_scalar*1000.0)) #Matches Excel
        si_iosf = stats['iosf']*(1.0/(320000.0*1000.0)) #Matches Excel mostly
        si_cpu_time = 1000.0 * ((fpga_cpu_time) * 1000.0/320000.0) # Matches Excel
        si_mdio = stats['mdio']*(1.0/(2400.0*1000.0)) # Matches Excel
        si_i2c = stats['i2c']*(1.0/(400.0*1000.0)) # Matches Excel
        si_execution_time = (1000.0 * ((fpga_cpu_time) * 1000.0/320000.0 +si_mdio+si_i2c+si_iosf+si_cache))
        if self.target == 'silicon':
            si_execution_time = stats['runtime']/1000.0 # For internal clock time of 1us
            #si_execution_time = stats['runtime']/1000000.0 # For internal clock time of 1ns
            return format(si_execution_time, '.3f')
        return format(si_execution_time, '.3f')

    def _import_link_partners(self):
        '''
        Call this function to load the information stored in the link_partners.json file
        '''
        self._debug('Importing Link Partner information')
        self.link_partners = json.load(open(os.path.join(self.support_path, 'link_partners.json')))
        self._debug('Successfully imported link partner information')
    
    def _get_lp_info(self,lp):
        '''
        Call this function with the link partner ID string to get the valid link modes, fec modes and aux technologies
        Valid ID Strings can be retrieved by getting the keys of self.link_partners
        Returns(3):
            List of valid link modes
            List of valid FEC modes
            List of valid auxiliary technologies
        '''
        link_modes = []
        fec_modes = []
        aux_tech = []
        device_type = self.link_partners[lp]['device_type']
        for item in self.link_partners[lp]['supported_link_modes']:
            link_modes.append(item['link_mode'])
        for item in self.link_partners[lp]['supported_fec_modes']:
            fec_modes.append(item['fec_mode'])
        for item in self.link_partners[lp]['auxiliary_technologies']:
            aux_tech.append(item)
            
        return link_modes, fec_modes, aux_tech
    
    def _generate_logfile(self,type='normal'):
        '''
        Called to generate a log file and get the name for writing to it later
        '''
        current_timestamp = time.strftime("%Y%m%d_%H%M%S")
        if type == 'normal':
            if not os.path.exists(os.path.join(self.support_path, 'logs')):
                if not os.path.isdir(os.path.join(self.support_path, 'logs')):
                    os.makedirs(os.path.join(self.support_path, 'logs'))
            log_name = 'logs/log_' + current_timestamp + '.log'
            log_path = os.path.join(self.support_path, log_name)
            log_file = open(log_path, 'a+')
            log_file.write('New log file created at ' + current_timestamp + '\n')
            log_file.close()
        elif type == 'SVEN':
            if not os.path.exists(os.path.join(self.support_path, 'sven_logs')):
                if not os.path.isdir(os.path.join(self.support_path, 'sven_logs')):
                    os.makedirs(os.path.join(self.support_path, 'sven_logs'))
            log_name = 'sven_logs/sven_log_' + current_timestamp + '.log'
            log_path = os.path.join(self.support_path, log_name)
            log_file = open(log_path,'ab')
            header = open(os.path.join(self.support_path,self.sven_header_file), 'rb').read()
            log_file.write(header)
            log_file.close()
        else:
            _debug('No valid log type detected')
            return
        return log_path

    def _write_to_log(self,value,log_path):
        '''
            Call this helper function when you want to write the a log file in ./logs/log.txt
        '''
        l = [] # empty list to type checking
        #current_timestamp = time.strftime("%Y%m%d_%H%M%S")
        #log_name = 'logs/log_' + current_timestamp + '.txt'
        #log_path = os.path.join(self.support_path, 'logs/log.txt')
        log_file = open(log_path, 'a+')
        if (type(value) == type(l)):
            for item in value:
                log_file.write(str(item))
                log_file.write('\n')
        else:
            log_file.write(str(value))
            log_file.write('\n')
        log_file.close()
        
    def _write_to_sven_log(self, data, inputfilepath):
        l = []
        log_file = open(inputfilepath, 'ab')
        if (type(data) == type(l)):
            for item in data:
                self._debug(item)
                log_file.write(chr(int(item)))
        else:
            print 'Expected list of values'
        log_file.close()

    def _debug(self, string):
        '''
            If the state of self.debug_on = True, when this is called, it will print whatever string it was passed
        '''
        if self.debug_on:
            print string

    def _get_all_phy_types(self,phy_caps,index_of_dword):
        '''
            Call this funtion to decode the PHY capabilities in decimal to a list of PHY types
        '''
        list_of_phy_types = []
        if index_of_dword == 0:
            if (phy_caps >> self.netlist_defines.PHY_INDEX_100BASE_TX) & 1:
                list_of_phy_types.append('100BASE-TX')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_100M_SGMII) & 1:
                list_of_phy_types.append('100M-SGMII')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_1000BASE_T) & 1:
                list_of_phy_types.append('1000BASE-T')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_1000BASE_SX) & 1:
                list_of_phy_types.append('1000BASE-SX')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_1000BASE_LX) & 1:
                list_of_phy_types.append('1000BASE-LX')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_1000BASE_KX) & 1:
                list_of_phy_types.append('1000BASE-KX')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_1G_SGMII) & 1:
                list_of_phy_types.append('1G-SGMII')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_2P5GBASE_T) & 1:
                list_of_phy_types.append('2P5GBASE-T')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_2P5GBASE_X) & 1:
                list_of_phy_types.append('2P5GBASE-X')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_2P5GBASE_KX) & 1:
                list_of_phy_types.append('2P5GBASE-KX')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_5GBASE_T) & 1:
                list_of_phy_types.append('5GBASE-T')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_5GBASE_KR) & 1:
                list_of_phy_types.append('5GBASE-KR')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_10GBASE_T) & 1:
                list_of_phy_types.append('10GBASE-T')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_10G_SFI_DA) & 1:
                list_of_phy_types.append('10G-SFI-DA')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_10GBASE_SR) & 1:
                list_of_phy_types.append('10GBASE-SR')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_10GBASE_LR) & 1:
                list_of_phy_types.append('10GBASE-LR')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_10GBASE_KR_CR1) & 1:
                list_of_phy_types.append('10GBASE-KR/CR1')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_10G_SFI_AOC_ACC) & 1:
                list_of_phy_types.append('10G-SFI-C2M')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_10G_SFI_C2C) & 1:
                list_of_phy_types.append('10G-SFI-C2C')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_25GBASE_T) & 1:
                list_of_phy_types.append('25GBASE-T')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_25GBASE_CR) & 1:
                list_of_phy_types.append('25GBASE-CR')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_25GBASE_CR_S) & 1:
                list_of_phy_types.append('25GBASE-CR-S')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_25GBASE_CR1) & 1:
                list_of_phy_types.append('25GBASE-CR1')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_25GBASE_SR) & 1:
                list_of_phy_types.append('25GBASE-SR')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_25GBASE_LR) & 1:
                list_of_phy_types.append('25GBASE-LR')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_25GBASE_KR) & 1:
                list_of_phy_types.append('25GBASE-KR')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_25GBASE_KR_S) & 1:
                list_of_phy_types.append('25GBASE-KR_S')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_25GBASE_KR1) & 1:
                list_of_phy_types.append('25GBASE-KR1')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_25G_AUI_AOC_ACC) & 1:
                list_of_phy_types.append('25G-AUI-C2M')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_25G_AUI_C2C) & 1:
                list_of_phy_types.append('25G-AUI-C2C')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_40GBASE_CR4) & 1:
                list_of_phy_types.append('40GBASE-CR4')
            if (phy_caps >> self.netlist_defines.PHY_INDEX_40GBASE_SR4) & 1:
                list_of_phy_types.append('40GBASE-SR4')
            return list_of_phy_types 
        if index_of_dword == 1:
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_40GBASE_LR4 - 32)) & 1:
                list_of_phy_types.append('40GBASE-LR4')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_40GBASE_KR4 - 32)) & 1:
                list_of_phy_types.append('40GBASE-KR4')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_40G_XLAUI_AOC_ACC - 32)) & 1:
                list_of_phy_types.append('40G-XLAUI-C2M')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_40G_XLAUI - 32)) & 1:
                list_of_phy_types.append('40G-XLAUI')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_50GBASE_CR2 - 32)) & 1:
                list_of_phy_types.append('50GBASE-CR2')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_50GBASE_KR2 - 32)) & 1:
                list_of_phy_types.append('50GBASE-KR2')        
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_50G_LAUI2_AOC_ACC - 32)) & 1:
                list_of_phy_types.append('50G-LAUI2-C2M')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_50G_LAUI2 - 32)) & 1:
                list_of_phy_types.append('50G-LAUI2')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_50G_AUI2_AOC_ACC - 32)) & 1:
                list_of_phy_types.append('50G-AUI2-C2M')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_50G_AUI2 - 32)) & 1:
                list_of_phy_types.append('50G-AUI2') 
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_50GBASE_CR_PAM4 - 32)) & 1:
                list_of_phy_types.append('50GBASE-CR-PAM4')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_50GBASE_SR - 32)) & 1:
                list_of_phy_types.append('50GBASE-SR')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_50GBASE_FR - 32)) & 1:
                list_of_phy_types.append('50GBASE-FR')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_50GBASE_LR - 32)) & 1:
                list_of_phy_types.append('50GBASE-LR')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_50GBASE_KR_PAM4 - 32)) & 1:
                list_of_phy_types.append('50GBASE-KR-PAM4')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_50G_AUI1_AOC_ACC - 32)) & 1:
                list_of_phy_types.append('50G-AUI1-C2M')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_50G_AUI1 - 32)) & 1:
                list_of_phy_types.append('50G-AUI1') 
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_100GBASE_CR4 - 32)) & 1:
                list_of_phy_types.append('100GBASE-CR4')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_100GBASE_SR4 - 32)) & 1:
                list_of_phy_types.append('100GBASE-SR4')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_100GBASE_LR4 - 32)) & 1:
                list_of_phy_types.append('100GBASE-LR4')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_100GBASE_KR4 - 32)) & 1:
                list_of_phy_types.append('100GBASE-KR4')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_100G_CAUI4_AOC_ACC - 32)) & 1:
                list_of_phy_types.append('100G-CAUI4-C2M')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_100G_CAUI4 - 32)) & 1:
                list_of_phy_types.append('100G-CAUI4')  
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_100G_AUI4_AOC_ACC - 32)) & 1:
                list_of_phy_types.append('100G-AUI4-C2M')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_100G_AUI4 - 32)) & 1:
                list_of_phy_types.append('100G-AUI4')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_100GBASE_KR4_PAM4 - 32)) & 1:
                list_of_phy_types.append('100GBASE-KR4-PAM4')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_100GBASE_CP2 - 32)) & 1:
                list_of_phy_types.append('100GBASE-CP2')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_100GBASE_SR2 - 32)) & 1:
                list_of_phy_types.append('100GBASE-SR2') 
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_100GBASE_DR - 32)) & 1:
                list_of_phy_types.append('100GBASE-DR')
            return list_of_phy_types    
        if index_of_dword == 2:
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_100GBASE_KR2_PAM4 - 64)) & 1:
                list_of_phy_types.append('100GBASE-KR2-PAM4')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_100G_AUI2_AOC_ACC - 64)) & 1:
                list_of_phy_types.append('100G-AUI2-C2M') 
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_100G_AUI2 - 64)) & 1:
                list_of_phy_types.append('100G-AUI2')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_200GBASE_CR4_PAM4 - 64)) & 1:
                list_of_phy_types.append('200GBASE-CR4-PAM4')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_200GBASE_SR4 - 64)) & 1:
                list_of_phy_types.append('200GBASE-SR4')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_200GBASE_FR4 - 64)) & 1:
                list_of_phy_types.append('200GBASE-FR4')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_200GBASE_LR4 - 64)) & 1:
                list_of_phy_types.append('200GBASE-LR4')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_200GBASE_DR4 - 64)) & 1:
                list_of_phy_types.append('200GBASE-DR4')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_200GBASE_KR4_PAM4 - 64)) & 1:
                list_of_phy_types.append('200GBASE-KR4-PAM4')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_200G_AUI4_AOC_ACC - 64)) & 1:
                list_of_phy_types.append('200G-AUI4-C2M') 
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_200G_AUI4 - 64)) & 1:
                list_of_phy_types.append('200G-AUI4')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_200G_AUI8_AOC_ACC - 64)) & 1:
                list_of_phy_types.append('200G-AUI8-C2M') 
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_200G_AUI8 - 64)) & 1:
                list_of_phy_types.append('200G-AUI8')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_400GBASE_FR8 - 64)) & 1:
                list_of_phy_types.append('400GBASE-FR8')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_400GBASE_LR8 - 64)) & 1:
                list_of_phy_types.append('400GBASE-LR8')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_400GBASE_DR4 - 64)) & 1:
                list_of_phy_types.append('400GBASE-DR4')
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_400G_AUI8_AOC_ACC - 64)) & 1:
                list_of_phy_types.append('400G-AUI8-C2M') 
            if (phy_caps >> (self.netlist_defines.PHY_INDEX_400G_AUI8 - 64)) & 1:
                list_of_phy_types.append('400G-AUI8')
            return list_of_phy_types
        if index_of_dword == 3:
            return list_of_phy_types

    def _to_unsigned(self, value):
        if value >= 0:
            return value
        else:
            return value + 2**8


