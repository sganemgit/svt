
import sys
import time
from core.utilities.BitManipulation import *
from core.utilities.SvtDecorator import *
from core.structs.AqDescriptor import AqDescriptor
from cpkTier1 import *

class cpk(cpkTier1):
    '''
    	This class contains all the methods to interface with a cvl pf
    '''    
    def info(self, advance = False, Location = "AQ"):
        '''
            This function print cpk info
            argument:
                Advance - True/False. if true print more info.
                Location - AQ/REG
            return:
                None
        '''
        fw_info = self.driver.get_fw_info()
        ret_string = "#"*80 +"\n"
        ret_string += "Device info: \n"
        ret_string += "-"*13 +"\n"
        ret_string += "Device Name : CPK\n"
        ret_string += "Device Number : {}\n".format(self.driver.device_number())
        ret_string += "Port Number : {}\n".format(self.driver.port_number())
        ret_string += "Current MAC link status : {}\n".format('N/A')
        ret_string += "Current MAC link Speed : {}\n".format('N/A')
        ret_string += "Current Phy Type : {}\n".format('N/A')
        ret_string += "Current FEC Type : {}\n".format('N/A')
        ret_string += "Current PCIe link speed : {}\n".format('N/A')
        ret_string += "Current PCIe link Width : {}\n".format('N/A')
        ret_string += "FW version : {}\n".format(fw_info['FW build'])
        ret_string += "FW build  : {}\n".format(fw_info['FW version'])
        ret_string += "#"*80 +"\n"
        return ret_string

###############################################################################
#                        Register reading section                             #
###############################################################################

    def read_register(self, register_name, mul = 0x8, size = 0xffffffff):
       '''
            This function reads CVL register
            :param register_name: Defined in reg_dict in cvlDefines
            :return: int
       '''
       reg_data = 0
       for addr in self.reg_dict[register_name]:
           reg_addr = calculate_port_offset(addr, mul, self.driver.port_number())
           temp_data = self.driver.read_csr(reg_addr)
           reg_data = ((reg_data & size) << 32) | temp_data
       return reg_data

    def GetPTC(self):
        '''
            This function reads all PTC CVL register
                Total Packets Transmitted Counter (13.2.2.24.59 - 13.2.2.24.72)
                return: dict--
                        'GetPTC64'
                        'GetPTC127'
                        'GetPTC255'
                        'GetPTC511'
                        'GetPTC1023'
                        'GetPTC1522'
                        'GetPTC9522'
                        'TotalPTC' - sum of all PTC registers
        '''
        PTC_registers_list = ["PTC64", "PTC127", "PTC255", "PTC511", "PTC1023", "PTC1522", "PTC9522"]
        PTC_Dict = {}
        PTC_Dict['TotalPTC'] = 0
        for reg in PTC_registers_list:
            PTC_Dict[reg] = self.read_register(reg)
            PTC_Dict['TotalPTC'] = PTC_Dict['TotalPTC'] + self.read_register(reg)
        return PTC_Dict

    def GetPRC(self):
        '''
            This function reads all PRC CVL registers
            Total Packets Received Counter (13.2.2.24.45-13.2.2.24.58)
            return: dict--
                        'PRC64'
                        'PRC127'
                        'PRC255'
                        'PRC511'
                        'PRC1023'
                        'PRC1522'
                        'PRC9522'
                        'TotalPRC' - sum of all PRC registers
        '''
        PRC_registers_list = ["PRC64", "PRC127", "PRC255", "PRC511", "PRC1023", "PRC1522", "PRC9522"]
        PRC_Dict = dict()
        PRC_Dict['TotalPRC'] = 0
        for reg in PRC_registers_list:
            PRC_Dict[reg] = self.read_register(reg)
            PRC_Dict['TotalPRC'] = PRC_Dict['TotalPRC'] + self.read_register(reg)
        return PRC_Dict

    def GetPRCByPacketSize(self, Packet_size):
        '''This function return PRC according to packet size
            input: packet size (int)
            return: PRC (int)
        '''
        if Packet_size <= 64:
            return self.read_register("PRC64")
        elif (Packet_size >= 65) and (Packet_size <= 127):
            return self.read_register("PRC127")
        elif (Packet_size >= 128) and (Packet_size <= 255):
            return self.read_register("PRC255")
        elif (Packet_size >= 256) and (Packet_size <= 511):
            return self.read_register("PRC511")
        elif (Packet_size >= 512) and (Packet_size <= 1023):
            return self.read_register("PRC1023")
        elif (Packet_size >= 1024) and (Packet_size <= 1522):
            return self.read_register("PRC1522")
        elif (Packet_size >= 1523) and (Packet_size <= 9522):
            return self.read_register("PRC9522")

    def GetPTCByPacketSize(self, Packet_size):
        '''This function return PTC according to packet size
            input: packet size (int)
            return: PTC (int)
        '''
        if Packet_size <= 64:
            return self.read_register("PTC64")
        elif (Packet_size >= 65) and (Packet_size <= 127):
            return self.read_register("PTC127")
        elif (Packet_size >= 128) and (Packet_size <= 255):
            return self.read_register("PTC255")
        elif (Packet_size >= 256) and (Packet_size <= 511):
            return self.read_register("PTC511")
        elif (Packet_size >= 512) and (Packet_size <= 1023):
            return self.read_register("PTC1023")
        elif (Packet_size >= 1024) and (Packet_size <= 1522):
            return self.read_register("PTC1522")
        elif (Packet_size >= 1523) and (Packet_size <= 9522):
            return self.read_register("PTC9522")

    def GetTrafficStats(self):
        '''This function returns a dictionary contains all PRC and PTC registers:
            input: none
            return: dict --
                'TotalPacketRecieve' : dict that contain all PRC CVL registers and total PRC
                'TotalPacketTransmite' : dict that contain all PTC CVL registers and total PTC
        '''
        MacStatistics = {}
        MacStatistics['TotalPacketRecieve'] = self.GetPRC()
        MacStatistics['TotalPacketTransmite'] = self.GetPTC()
        return MacStatistics

    def GetLinkDownCounter(self):
        '''
            This function counts the number link drop, clear by globr (13.2.2.4.80)
            return: number of link drop
        '''
        reg_data = self.read_register("PRTMAC_LINK_DOWN_COUNTER[PRT]", mul=0x4)
        Link_drop_counter = get_bits_slice_value(reg_data, 0, 15)
        return Link_drop_counter

    def GetMacCounters(self):
        counters_list = ["MSPDC", "CRCERRS", "ILLERRC", "ERRBC", "MLFC", "MRFC", "RLEC", "RUC", "RFC", "ROC", "RJC"]
        counter_dict = dict()
        counter_dict['LDPC'] = self.read_register("LDPC", mul=0x4, size=0xffff)
        for reg in counters_list:
            counter_dict[reg] = self.read_register(reg, size=0xffff)
        counter_dict['link Down Counter'] = self.GetLinkDownCounter()
        return counter_dict

    def Clear_register(self, register_name, mul=0x8):
        ''' 
            This function clears CVL register
            :param register_name: Defined in reg_dict in cvlDefines
        '''
        for addr in self.reg_dict[register_name]:
            reg_addr = calculate_port_offset(addr, mul, self.driver.port_number())
            self.driver.write_csr(reg_addr, 0xffffffff)

    def ClearMACstat(self):
        '''
            This function clears following MAC statistics registers.
            clear: PTC, PRC, CRCERRS, ILLERRC, ERRBC, MLFC, MRFC, RLEC, RUC, RFC, ROC, RJC, MSPDC, LDPC.
            (12.2.2.19)
        '''
        for reg in self.reg_dict:
            self.Clear_register(register_name=reg, mul=0x4) if reg == "LDPC" else self.Clear_register(register_name=reg)


###############################################################################
#                       Traffic Section                                       #
###############################################################################

    def EthStartTraffic(self, packet_size = 512, number_of_packets =None):
        '''
            This function starts Tx and Rx.
            argument: packet size - Default is 512
            return: None
        '''
        driver = self.driver
        driver.start_rx()
        time.sleep(2)
        driver.start_tx(packet_size = packet_size, number_of_packets =number_of_packets)

    def EthStartRx(self):
        '''
            This function starts Tx and Rx.
            argument: packet size - Default is 512
            return: None
        '''
        self.driver.start_rx()
    
    def EthStartTx(self, packet_size = 512, number_of_packets =None):
        '''
            This function starts Tx and Rx.
            argument: packet size - Default is 512
            return: None
        '''
        if number_of_packets:
            self.driver.start_tx(packet_size=packet_size, number_of_packets=number_of_packets, tx_limit_type='PACKET_COUNT')
        else: 
            self.driver.start_tx(packet_size=packet_size)

    def EthStopRx(self, ring_id=0):
        '''
            This function stops Tx and Rx.
            argument: None
            return: None
        '''
        driver = self.driver
        driver.stop_rx(ring_id=ring_id)
    
    def EthStopTx(self, ring_id=0):
        '''
            This function stops Tx and Rx.
            argument: None
            return: None
        '''
        self.driver.stop_tx(ring_id=ring_id)

    def EthStopTraffic(self):
        '''
            This function stops Tx and Rx.
            argument: None
            return: None
        '''
        driver = self.driver
        driver.stop_tx()
        time.sleep(3)
        driver.stop_rx()

    def GetCurrentThroughput(self, packet_size=512):
        '''
            This function returns current Throughput
            argument: packet size - Default is 512
            return: Transmit throughput
        '''
        driver = self.driver
        samp_time = 3
        start_PTC = self.GetPTC()['TotalPTC']
        start_time = curr_time = time.time()
        while ((curr_time - start_time) < samp_time):
            curr_time = time.time()
        end_PTC = self.GetPTC()['TotalPTC']
        return int((end_PTC - start_PTC)*8*packet_size/(curr_time - start_time))

    def GetRXThroughput(self, packet_size=512, samp_time = 3):
        '''This function returns current RX Throughput
            input:
                packet_size (int) - Default packet size is 512
                samp_time (int) - Defult sample time is 3 sec
            return:
                RX throughput (int)
        '''
        driver = self.driver
        start_PRC = self.GetPRC()[ConvertPacketSizeToPRC(packet_size)]
        start_time = curr_time = time.time()
        while ((curr_time - start_time) < samp_time):
            curr_time = time.time()
        end_PRC = self.GetPRC()[ConvertPacketSizeToPRC(packet_size)]
        return int((end_PRC - start_PRC)*8*packet_size/(curr_time - start_time))

    def GetTXThroughput(self, packet_size = 512, samp_time = 3):
        '''This function returns current TX Throughput
            input:
                packet_size (int) - Default packet size is 512
                samp_time (int) - Defult sample time is 3 sec
            return:
                TX throughput (int)
        '''
        driver = self.driver
        start_PTC = self.GetPTC()[ConvertPacketSizeToPTC(packet_size)]
        start_time = curr_time = time.time()
        while ((curr_time - start_time) < samp_time):
            curr_time = time.time()
        end_PTC = self.GetPTC()[ConvertPacketSizeToPTC(packet_size)]
        return int((end_PTC - start_PTC)*8*packet_size/(curr_time - start_time))

    def GetMacLinkStatus(self, Location = "AQ"):
        '''
            This function returns the link status.
            argument: read by AQ/REG
            return: True/false
        '''
        if Location == "REG":
            LinkStatus = self._GetMacLinkStatusReg()
        elif Location == "AQ":
            LinkStatus = self._GetMacLinkStatusAq()
        else:
            raise RuntimeError("Error GetMacLinkStatus: Error Location, please insert location REG/AQ") 
        return LinkStatus

    def _GetMacLinkStatusReg(self):
        '''
            This function returns the link status (13.2.2.4.78).
            PRTMAC_LINKSTA 0x001E47A0
                argument: None
                return: True/false
        '''
        reg_addr = calculate_port_offset(0x001E47A0, 0x4, self.driver.port_number())
        reg_data = self.driver.read_csr(reg_addr)
        LinkStatus = get_bit_value(reg_data, 30)
        return LinkStatus

    def _GetMacLinkStatusAq(self):
        '''This function returns the link status using Get link status AQ.
                argument: None
                return: True/false
        '''
        gls = {}
        gls['port'] = 0 #not relevant for CVL according to CVL Spec
        gls['cmd_flag'] = 1
        status, data = self.aq.GetLinkStatus(gls)

        if status:
            raise RuntimeError("Error _GetMacLinkStatusAQ: Admin command was not successful")

        return  data['link_sts']

    def GetLinkStatusFields(self):
        gls = dict()
        gls['port'] = 0 
        gls['cmd_flag'] = 1
        result = self.aq.GetLinkStatus(gls)

        if not result[0]:
            data = result[1]
        else:
            raise RuntimeError("Error {}: Admin command was not successful".format(self.aq.GetLinkStatusFields.__name__))

        for key, val in data.items():
            print("{} : {}".format(key, val))

        
    def GetCurrentLinkSpeed(self, Location = "AQ"):
        '''
            This function return Mac Link Speed.
            argument: "REG" / "AQ"
            return: 
                '10M' / '100M' / '1G' / '2.5G' / '5G' / '10G' / '20G' / '25G' / '40G' / '50G' / '100G' / '200G'
        '''
        if Location == "REG":
            LinkSpeed = self._GetCurrentLinkSpeedReg()
        elif Location == "AQ":
            LinkSpeed = self._GetCurrentLinkSpeedAq()
        else:
            raise RuntimeError("Error GetMacLinkSpeed: Error Location, please insert location REG/AQ")  
        return LinkSpeed

    def _GetCurrentLinkSpeedReg(self):
        '''
            This function returns the link speed (13.2.2.4.78).
            PRTMAC_LINKSTA 0x001E47A0
               argument: none
               return: link speed in str, for exmp: "40G"
        '''
        driver = self.driver
        reg_addr = calculate_port_offset(0x001E47A0, 0x4, driver.port_number())
        reg_data = driver.read_csr(reg_addr)
        LinkSpeed = get_bits_slice_value(reg_data,26,29)
        return self.Mac_link_speed_dict[LinkSpeed]

    def _GetCurrentLinkSpeedAq(self):
        '''
            This function return Mac Link Speed using Get link status AQ.
            return:
                '10M' / '100M' / '1G' / '2.5G' / '5G' / '10G' / '20G' / '25G' / '40G' / '50G' / '100G' / '200G'
        '''
        
        gls = {"port": 0, "cmd_flag": 1}
        status, data = self.aq.GetLinkStatus(gls)

        if status:
            raise RuntimeError("Error _GetCurrentLinkSpeedAq: Admin command was not successful")

        current_link_speed = data['current_link_speed']
        for key, val in self.Get_Speed_Status_dict.items():
            mask = 1 << key
            if current_link_speed & mask:
                return val
        else: 
            return None

    def RestartAn(self, Location = "AQ"):
        '''
            This function performs restart autoneg
            argument: "REG" / "AQ"
            return: None
        '''
        if Location == "REG":
            self._RestartAnReg()
        elif Location == "AQ":
            self._RestartAnAq()
        else:
            raise RuntimeError("Error RestartAn: Error Location, please insert location REG/AQ")

    def _RestartAnReg(self):
        '''
            This function performs restart autoneg
            This function is for debug only because Restart AN by REG is not implimented
        '''
        raise RuntimeError("Restart AN by REG is not implimented")

    def _RestartAnAq(self):
        '''
            This function performs restart autoneg by AQ
        '''
        args = {}
        args['port'] = 0 #not relevant for CVL according to CVL Spec
        args['restart'] = 1 #to restart the link
        args['enable'] = 1 #to enable the link
        status = self.SetupLink(args)

        if status[0]:
            error_msg = 'Error _RestartAnAq: Admin command was not successful, retval {}'.format(status[1])
            raise RuntimeError(error_msg)

    def Reset(self, reset_type = 'pfr'):
        '''
            This function performs resets
            argument: reset_type (string) - "globr" , "pfr" , "corer", "empr", "flr", "pcir", "bmer", "vfr", "vflr"
            return: None
        '''
        if reset_type in self.reset_type_dict:
            self.driver.device_reset(self.reset_type_dict[reset_type])
        else:
            print("could not identify reset type")

    def GetCurrentModuleInfo(self):
        '''
            This method retrieves the current module info based on the "current module type" field from GetPhyAbilities
            @input: None
            @output: dict
                    Module_ID - int
                    supported_tecknologies - list
                    GBE_compliance_code - int
        '''
        get_abils = dict()
        get_abils['port'] = 0 #not relevant for CVL according to CVL Spec
        get_abils['rep_qual_mod'] = 0
        get_abils['rep_mode'] = 1
        
        result = self.GetPhyAbilities(get_abils)
        
        if not result[0]: 
            data = result[1]
        else:
            raise RuntimeError("Error _GetPhyTypeAbilitiesAq: Admin command was not successful")  
        
        module_type_info_dict = dict()    
        current_module_type = data['current_module_type']

        module_type_info_dict['Module_ID'] = current_module_type & 0xFF

        byte1 = (current_module_type >> 8) & 0xFF
        supported_tecknologies_list = list()
        for key, val in self.suppoted_module_technologies_dict.items():
            mask = 1 << key
            if byte1 & mask: 
                supported_tecknologies_list.append(val)

        module_type_info_dict['supported_tecknologies'] = supported_tecknologies_list

        module_type_info_dict['GBE_compliance_code'] = (current_module_type >> 16) & 0xFF
        return module_type_info_dict

    def GetPhyType(self, Location = "AQ"):
        '''
            This function return Phy type
            input: Location = "AQ"
            return: phy type (str)
        '''
        if Location == "REG":
            Phy_Type = self._GetPhyTypeReg()
        elif Location == "AQ":
            Phy_Type = self._GetPhyTypeAq()
        else:
            raise RuntimeError("Error GetPhyType: Error Location, please insert location REG/AQ")
        return Phy_Type

    def _GetPhyTypeReg(self):
        '''
            This function return Phy type.
            for debug only because GetPhyType by REG is not implimented.
        '''
        raise RuntimeError("Get Phy type by Reg is not implemented")

    def _GetPhyTypeAq(self):
        '''
            This function return Phy type using Get link status AQ.
            return: Phy type in str
        '''
        gls = {}
        gls['port'] = 0 #not relevant for CVL according to CVL Spec
        gls['cmd_flag'] = 1
        status, data = self.aq.GetLinkStatus(gls)
        if status:
            raise RuntimeError("Error _GetPhyTypeAq: Admin command was not successful")  

        phy_type = data['phy_type'] 
        if self.Get_Phy_Type_Status_dict:
            for i in range(len(self.Get_Phy_Type_Status_dict)):
                if ((phy_type >> i) & 0x1):
                    return self.Get_Phy_Type_Status_dict[i]
        else:
            raise RuntimeError("Error _GetPhyTypeAq: Get_Phy_Type_Status_dict is not defined")

    def GetCurrentFECStatus(self, Location = "AQ"):
        '''
            This function return the current FEC status
            argument:
                Location = "REG" / "AQ"
        '''
        if Location == "REG":
            self._GetCurrentFECStatusReg()
        elif Location == "AQ":
            FEC_Type = self._GetCurrentFECStatusAq()
        else:
            raise RuntimeError("Err GetCurrentFECStatus: Error Location, please insert location REG/AQ")
        return FEC_Type

    def _GetCurrentFECStatusReg(self):
        '''
            This function returns the FEC status using register.
            for debug only because GetCurrentFecStatus by REG is not implimented.
            return: None
        '''
        raise RuntimeError("Get current FEC status by Reg is not implimented")

    def _GetCurrentFECStatusAq(self):
        '''
            This function returns the FEC status using Get link status AQ.
            return: FEC type by str
        '''
        link_speed = self.GetPhyLinkSpeed()

        if self.GetPhyType() == 'N/A':
            return 'N/A'
        gls = {}
        gls['port'] = 0 #not relevant for CVL according to CVL Spec
        gls['cmd_flag'] = 1
        status, data = self.aq.GetLinkStatus(gls)

        if status:
            raise RuntimeError("Error _GetCurrentFECStatusAq: Admin command was not successful")

        FEC_list = ['10G_KR_FEC','25G_KR_FEC','25G_RS_528_FEC','25G_RS_544_FEC']
        if link_speed == '10G':
            if data['10g_kr_fec']:
                return FEC_list[0]
            else:
                return 'NO_FEC'
        else:
            if data['25g_kr_fec']:
                return FEC_list[1]
            elif data['25g_rs_528']:
                return FEC_list[2]
            elif data['rs_544']:
                return FEC_list[3]
            else:
                return 'NO_FEC'

    def GetCurrentModuleComplianceEnforcement(self):
        '''
            CPK DCR 102
        '''
        get_abils = {}
        get_abils['port'] = 0 #not relevant for CVL according to CVL Spec
        get_abils['rep_qual_mod'] = 0
        get_abils['rep_mode'] = 0 
        
        status, data = self.GetPhyAbilities(get_abils)
        
        if status:
            raise RuntimeError("Error _GetPhyTypeAbilitiesAq: Admin command was not successful")  
        
        if data['module_compliance_enforcement'] & 0x1:
            return 'strict'
        else:
            return 'lenient'
         
    def GetPhyTypeAbilities(self, rep_mode = 0, Location = "AQ"):
        '''
            This function return list of phy types
            argument:
                rep_mode = int[2 bits] -- 00b reports capabilities without media, 01b reports capabilities including media, 10b reports latest SW configuration request
                Location = "REG" / "AQ"
        '''
        if Location == "REG":
            self._GetPhyTypeAbilitiesReg()
        elif Location == "AQ":
            phy_type_list = self._GetPhyTypeAbilitiesAq(rep_mode)
        else:
            raise RuntimeError("Err GetPhyTypeAbilities: Error Location, please insert location REG/AQ")
        return phy_type_list

    def _GetPhyTypeAbilitiesReg(self):
        '''
            This function return list of phy types
            for debug only because reset by AQ is not implimented.
        '''
        raise RuntimeError("Get Phy Type Abilities by Reg is not implimented")      

    def _GetPhyTypeAbilitiesAq(self, rep_mode):
        '''
            Description: Get various PHY type abilities supported on the port.
            input:
                rep_mode : int[2 bits] -- 00b reports capabilities without media, 01b reports capabilities including media, 10b reports latest SW configuration request
            return:
                phy_type_list - contain phy type abilities by str
        '''
        get_abils = {}
        get_abils['port'] = 0 #not relevant for CVL according to CVL Spec
        get_abils['rep_qual_mod'] = 0
        get_abils['rep_mode'] = rep_mode
        
        status, data = self.GetPhyAbilities(get_abils)
        
        if status:
            raise RuntimeError("Error _GetPhyTypeAbilitiesAq: Admin command was not successful")  
            
        phy_type = data['phy_type']
        
        phy_type_list = list()
        
        for i in range(len(self.get_Ability_Phy_Type_dict)):
            if ((phy_type >> i) & 0x1):
                phy_type_list.append(self.get_Ability_Phy_Type_dict[i])
               
        return phy_type_list

    def GetEEEAbilities(self, rep_mode, Location = "AQ"):
        '''
            This function return list of EEE abilities
            argument:
                rep_mode = int[2 bits] -- 00b reports capabilities without media, 01b reports capabilities including media, 10b reports latest SW configuration request
                Location = "REG" / "AQ" 
     
        '''
        if Location == "REG":
            self._GetEEEAbilitiesReg()
        elif Location == "AQ":
            EEE_list = self._GetEEEAbilitiesAq(rep_mode)
        else:
            raise RuntimeError("Err GetEEEAbilities: Error Location, please insert location REG/AQ")

        return EEE_list 
     
    def _GetEEEAbilitiesReg(self):
        '''
            This function return list of EEE abilities
            for debug only because FecAbilities by REG is not implimented.
        '''
        raise RuntimeError("Get EEE Abilities by Reg is not implimented")   
     
    def _GetEEEAbilitiesAq(self, rep_mode):
        '''
            Description: Get EEE abilities supported on the port.
            input:
                rep_mode : int[2 bits] -- 00b reports capabilities without media, 01b reports capabilities including media, 10b reports latest SW configuration request
            return:
                EEE_list - contain EEE abilities by str
        '''
        get_abils = {}
        get_abils['port'] = 0 #not relevant for CVL according to CVL Spec
        get_abils['rep_qual_mod'] = 0
        get_abils['rep_mode'] = rep_mode
        
        status, data = self.GetPhyAbilities(get_abils) 
        if status:
            raise RuntimeError("Error _GetEEEAbilitiesAq: Admin command was not successful")  
            
        EEE_list = list()
        eee_cap = data['eee_cap']
        for key, val in self.get_Ability_EEE_dict.items():
            mask = 1 << key
            if mask & eee_cap:
                EEE_list.append(val)
        return EEE_list

    def GetFecAbilities(self,rep_mode = 1, Location = "AQ"):
        '''
            This function return list of FEC abilities
            argument:
                rep_mode = int[2 bits] -- 00b reports capabilities without media, 01b reports capabilities including media, 10b reports latest SW configuration request
                Location = "REG" / "AQ" 
            return:
                FEC_list - contain FEC options by str
        '''
        if Location == "REG":
            self._GetFecAbilitiesReg()
        elif Location == "AQ":
            FEC_list = self._GetFecAbilitiesAq(rep_mode)
        else:
            raise RuntimeError("Err GetFecAbilities: Error Location, please insert location REG/AQ")    
       
        return FEC_list

    def _GetFecAbilitiesReg(self):
        '''
            This function return list of FEC abilities
            for debug only because FecAbilities by REG is not implimented.
        '''
        raise RuntimeError("Get FEC Abilities by Reg is not implimented")

    def _GetFecAbilitiesAq(self,rep_mode):
        '''
            Description: Get available FEC options for the link
            input:
                rep_mode : int[2 bits] -- 00b reports capabilities without media, 01b reports capabilities including media, 10b reports latest SW configuration request
            return:
                FEC_list - contain FEC options by str
        '''
        
        get_abils = {}
        get_abils['port'] = 0 #not relevant for CVL according to CVL Spec
        get_abils['rep_qual_mod'] = 0
        get_abils['rep_mode'] = rep_mode
        
        result = self.GetPhyAbilities(get_abils)
        
        if not result[0]: # if Admin command was successful - False
            data = result[1]
        else:
            raise RuntimeError("Error _GetFecAbilitiesAq: Admin command was not successful")  
            
        FEC_list = []
        if data['fec_firecode_10g_abil']:
            FEC_list.append(self.get_Ability_FEC_dict[0])
        
        if data['fec_firecode_10g_req']:
            FEC_list.append(self.get_Ability_FEC_dict[1])
        
        if data['fec_rs528_req']:
            FEC_list.append(self.get_Ability_FEC_dict[2])
            
        if data['fec_firecode_25g_req']:
            FEC_list.append(self.get_Ability_FEC_dict[3])
            
        if data['fec_rs544_req']:
            FEC_list.append(self.get_Ability_FEC_dict[4])
            
        if data['fec_rs528_abil']:
            FEC_list.append(self.get_Ability_FEC_dict[6])
            
        if data['fec_firecode_25g_abil']:
            FEC_list.append(self.get_Ability_FEC_dict[7])
                
        #print FEC_list
        return FEC_list

    def GetPhyLinkSpeed(self, Location = "REG"):
        '''
            This function return Phy Link Speed.
            argument:
                Location = "REG" / "AQ" 
            return: 
                link speed by str - '10M' / '100M' / '1G' / '2.5G' / '5G' / '10G' / '20G' / '25G' / '40G' / '50G' / '100G'
        '''
        if Location == "REG":
            LinkSpeed = self._GetPhyLinkSpeedReg() 
        elif Location == "AQ":
            LinkSpeed = self._GetPhyLinkSpeedAq() 
        else:
            raise RuntimeError("Err GetPhyLinkSpeed: Error Location, please insert location REG/AQ")    
            
        return LinkSpeed    
        
    def _GetPhyLinkSpeedReg(self):
        '''
            This function return Phy Link Speed.
            return: 
                link speed by str - '10M' / '100M' / '1G' / '2.5G' / '5G' / '10G' / '20G' / '25G' / '40G' / '50G' / '100G'
        '''
        driver = self.driver
        reg_addr = calculate_port_offset(0x03001030, 0x100, driver.port_number())
        value = self.ReadEthwRegister(reg_addr)
        return self.Phy_link_speed_dict[int(value,16)]
        
    def _GetPhyLinkSpeedAq(self):
        '''
            This function return Phy Link Speed using Get link status AQ.
            return:
                link speed by str - '10M' / '100M' / '1G' / '2.5G' / '5G' / '10G' / '20G' / '25G' / '40G' / '50G' / '100G' / '200G' 
        '''
        raise RuntimeError("_GetPhyLinkSpeedAq need to be done")

    def GetPhyLinkStatus(self, Location = "AQ"):
        '''
            This function return Phy Link status.
            argument:
                Location = "REG" / "AQ" 
            return: 
                True/False
        '''
        if Location == "REG":
            LinkStatus = self._GetPhyLinkStatusReg() 
        elif Location == "AQ":
            LinkStatus = self._GetPhyLinkStatusAq() 
        else:
            raise RuntimeError("Err GetPhyLinkStatus: Error Location, please insert location REG/AQ")   
            
        return LinkStatus   

    def _GetPhyLinkStatusReg(self):
        '''This function return PCS Link Status
            for debug only because GetPhyLinkStatus by REG is not implimented.
        '''
        raise RuntimeError("Get link status by Reg is not implimented")
        
    def _GetPhyLinkStatusAq(self):
        '''
            This function return PCS Link Status .
            return: true (link up)/false (link down)
        '''
        quad,pmd_num = self._GetQuadAndPmdNumAccordingToPf()
        
        link_speed = self.GetPhyLinkSpeed()
        
        if link_speed == "100M" or link_speed == "1G":
            offset_base = calculate_port_offset(0x03000180, 0x4, pmd_num)
            reg_addr = calculate_port_offset(offset_base, 0x100, quad)  
            value = self.ReadEthwRegister(reg_addr)
            link_speed_from_reg = get_bits_slice_value(int(value,16), 2, 3)
            link_speed_from_reg_dict = {1: "100M", 2: "1G"}
            
            if link_speed == link_speed_from_reg_dict[link_speed_from_reg]:
                link_status = get_bit_value(int(value,16), 0)
            else:
                return 0    
            
        else:
            reg_addr = calculate_port_offset(0x03000108, 0x100, quad)
            value = self.ReadEthwRegister(reg_addr)
            
            if link_speed == "100G":
                link_status = get_bit_value(int(value,16), 8) #according PCS-Status register
            else:
                value = get_bits_slice_value(int(value,16), 0, 3)
                link_status = get_bit_value(value, pmd_num)
        
        return link_status


    def DisableFECRequests(self, rep_mode = 1, Location = "AQ"):
        '''This function diables all feq requests by the device while keeping all other abillities intact 
            argument:
                Location = "REG" / "AQ" 
        '''
        if Location == "REG":
            self._DisableFECRequestsReg() 
        elif Location == "AQ":
            self._DisableFECRequestsAq(rep_mode) 
        else:
            raise RuntimeError("Err DisableFECRequests: Error Location, please insert location REG/AQ") 

    def _DisableFECRequestsReg(self):
        '''This function diables all feq requests by the device while keeping all other abillities intact 
            for debug only because DisableFECRequests by REG is not implimented.
        '''
        raise RuntimeError("Disable fec requests by Reg is not implimented")

    def _DisableFECRequestsAq(self, rep_mode):
        '''this function diables all feq requests by the device while keeping all other abillities intact 
            arguments: none
            return: none 
            level: L2
        '''
        config = {}
        phy_type = 0
        data = self.GetPhyAbilities({'port':0, 'rep_qual_mod':0, 'rep_mode':rep_mode}) ##TODO: check values

        if data[0]:
            error_msg = 'Error DisableFECRequests: _GetPhyAbilities Admin command was not successful, retval {}'.format(data[1])
            raise RuntimeError(error_msg)

        abilities = data[1]
        config['phy_type_0'] = abilities['phy_type_0']
        config['phy_type_1'] = abilities['phy_type_1']
        config['phy_type_2'] = abilities['phy_type_2']
        config['phy_type_3'] = abilities['phy_type_3']

        config['port'] = 0 #not relevant for CVL according to CVL Spec
        config['tx_pause_req'] = abilities['pause_abil']
        config['rx_pause_req'] = abilities['asy_dir_abil']
        config['low_pwr_abil'] = abilities['low_pwr_abil']
        config['en_link'] = 1
        config['en_auto_update'] = 1
        config['lesm_en'] = 0
        config['low_pwr_ctrl'] = abilities['low_pwr_ctrl']
        config['eee_cap_en'] = abilities['eee_cap']
        config['eeer'] = abilities['eeer']
        config['auto_fec_en'] = 1
        
        config['fec_firecode_10g_abil'] = abilities['fec_firecode_10g_abil'] 
        config['fec_firecode_10g_req'] = 0
        config['fec_rs528_req'] = 0
        config['fec_firecode_25g_req'] = 0
        config['fec_rs544_req'] = 0
        config['fec_rs528_abil'] = abilities['fec_rs528_abil']
        config['fec_firecode_25g_abil'] = abilities['fec_firecode_25g_abil']

        status = ()
        status =  self.SetPhyConfig(config)
        
        if status[0]:
            error_msg = 'Error DisableFECRequests: Admin command was not successful, retval {}'.format(status[1])
            raise RuntimeError(error_msg)   

    def DisableLESM(self, rep_mode = 1):
        '''this function diable LESM while keeping all other abillities intact 
            arguments: rep_mode
            return: none 
            level: L2
        '''
        config = {}
        phy_type = 0
        data = self.GetPhyAbilities({'port':0, 'rep_qual_mod':0, 'rep_mode':rep_mode}) ##TODO: check values

        if data[0]:
            error_msg = 'Error DisableLESM: _GetPhyAbilities Admin command was not successful, retval {}'.format(data[1])
            raise RuntimeError(error_msg)

        abilities = data[1]
        config['phy_type_0'] = abilities['phy_type_0']
        config['phy_type_1'] = abilities['phy_type_1']
        config['phy_type_2'] = abilities['phy_type_2']
        config['phy_type_3'] = abilities['phy_type_3']

        config['port'] = 0 #not relevant for CVL according to CVL Spec
        config['tx_pause_req'] = abilities['pause_abil']
        config['rx_pause_req'] = abilities['asy_dir_abil']
        config['low_pwr_abil'] = abilities['low_pwr_abil']
        config['en_link'] = 1
        config['en_auto_update'] = 1
        config['lesm_en'] = 0
        config['low_pwr_ctrl'] = abilities['low_pwr_ctrl']
        config['eee_cap_en'] = abilities['eee_cap']
        config['eeer'] = abilities['eeer']
        config['auto_fec_en'] = 1
        config['fec_firecode_10g_abil'] = abilities['fec_firecode_10g_abil'] 
        config['fec_firecode_10g_req'] = abilities['fec_firecode_10g_req']
        config['fec_rs528_req'] = abilities['fec_rs528_req']
        config['fec_firecode_25g_req'] = abilities['fec_firecode_25g_req']
        config['fec_rs544_req'] = abilities['fec_rs544_req']
        config['fec_rs528_abil'] = abilities['fec_rs528_abil']
        config['fec_firecode_25g_abil'] = abilities['fec_firecode_25g_abil']

        status = ()
        status =  self.SetPhyConfig(config)
        print(status)

        if status[0]:
            error_msg = 'Error DisableLESM: Admin command was not successful, retval {}'.format(status[1])
            raise RuntimeError(error_msg)

    def DisableAN37(self, rep_mode = 0):
        config = {}
        phy_type = 0
        data = self.GetPhyAbilities({'port':0, 'rep_qual_mod':0, 'rep_mode':rep_mode})

        if data[0]:
            error_msg = 'Error DisableAN37: _GetPhyAbilities Admin command was not successful, retval {}'.format(data[1])
            raise RuntimeError(error_msg)

        abilities = data[1]
        config['phy_type_0'] = abilities['phy_type_0']
        config['phy_type_1'] = abilities['phy_type_1']
        config['phy_type_2'] = abilities['phy_type_2']
        config['phy_type_3'] = abilities['phy_type_3']

        config['port'] = 0 #not relevant for CVL according to CVL Spec
        config['tx_pause_req'] = abilities['pause_abil']
        config['rx_pause_req'] = abilities['asy_dir_abil']
        config['low_pwr_abil'] = abilities['low_pwr_abil']
        config['en_link'] = 1
        config['en_auto_update'] = 1
        config['lesm_en'] = abilities['lesm_en']
        config['low_pwr_ctrl'] = abilities['low_pwr_ctrl']
        config['eee_cap_en'] = abilities['eee_cap']
        config['eeer'] = abilities['eeer']
        config['auto_fec_en'] = 1
        config['fec_firecode_10g_abil'] = abilities['fec_firecode_10g_abil'] 
        config['fec_firecode_10g_req'] = abilities['fec_firecode_10g_req']
        config['fec_rs528_req'] = abilities['fec_rs528_req']
        config['fec_firecode_25g_req'] = abilities['fec_firecode_25g_req']
        config['fec_rs544_req'] = abilities['fec_rs544_req']
        config['fec_rs528_abil'] = abilities['fec_rs528_abil']
        config['fec_firecode_25g_abil'] = abilities['fec_firecode_25g_abil']
        config['an_mode'] = 0
        status = ()
        status =  self.SetPhyConfig(config)
        print(status)
        
        if status[0]:
            error_msg = 'Error DisableLESM: Admin command was not successful, retval {}'.format(status[1])
            raise RuntimeError(error_msg)   

    def SetPhyConfiguration(self, PhyType,set_fec,rep_mode = 1,debug = False,Location = 'AQ'):
        '''This function configures the phy and the fec
            arguments: PhyType by string 
                set_fec by string
                rep_mode = takes the values 0,1,2 (defult value is 1)
                Location = "AQ"/"REG"
            return:None 
            level: L3
        '''
        if Location == "REG":
            self._SetPhyConfigurationfigReg(PhyType, set_fec, debug)
        elif Location == "AQ":
            self._SetPhyConfigurationAQ(PhyType, set_fec, rep_mode, debug)
        else:
            raise RuntimeError("Error SetPhyConfiguration: Error Location, please insert location REG/AQ")

    def _SetPhyConfigurationReg(self, PhyType,set_fec,debug):
        '''This function configures the phy and the fec
            for debug only because SetPhyConfiguration by REG is not implimented.
        '''
        raise RuntimeError("SetPhyConfiguration by Reg is not implimented")

    def _SetPhyConfigurationAQ(self, phy_type_list, set_fec,rep_mode,debug):
        '''This function configures the phy and the fec
            arguments:PhyType by string
                      set_fec by string
                      rep_mode
                      Location = "AQ"/"REG"
            retrun: None 
            Level: L1
        '''
        if (type(phy_type_list) == str ):
            tmp_str = phy_type_list
            phy_type_list = []
            phy_type_list.append(tmp_str)
        else:
            pass

        config = {}
        phy_type = 0
        status, data = self.aq.GetPhyAbilities({'port':0, 'rep_qual_mod':0, 'rep_mode':rep_mode}) 
        print(data)
        if status:
            error_msg = 'Error _SetPhyConfigurationAQ: GetPhyAbilities Admin command was not successful, retval {}'.format(data[1])
            raise RuntimeError(error_msg)

        config['port'] = 0 #not relevant for CVL according to CVL Spec
        config['tx_pause_req'] = data['pause_abil']
        config['rx_pause_req'] = data['asy_dir_abil']
        config['low_pwr_abil'] = data['low_pwr_abil']
        config['en_link'] = 1
        config['en_auto_update'] = 1
        config['lesm_en'] = 0
        config['low_pwr_ctrl'] = data['low_pwr_ctrl']
        config['eee_cap_en'] = data['eee_cap']
        config['eeer'] = data['eeer']
        if '50GBase-CR2' in phy_type_list:
            config['auto_fec_en'] = 0
        else:
            config['auto_fec_en'] = 1
        
        for recieved_phy_type in phy_type_list:
            if recieved_phy_type in self.set_Ability_PhyType_dict:
                phy_type = phy_type | (1 << self.set_Ability_PhyType_dict[recieved_phy_type])
            else:
                raise RuntimeError("Error _SetPhyConfigurationAQ: PHY_type is not exist in set_Ability_PhyType_dict") #implement a warning

        config['phy_type_0'] = get_bits_slice_value(phy_type,0,31)
        config['phy_type_1'] = get_bits_slice_value(phy_type,32,63)
        config['phy_type_2'] = get_bits_slice_value(phy_type,64,95)
        config['phy_type_3'] = get_bits_slice_value(phy_type,96,127)

        if set_fec == 'NO_FEC':
            config['fec_firecode_10g_abil'] = 0 #data['fec_firecode_10g_abil'] 
            config['fec_firecode_10g_req'] = 0 
            config['fec_rs528_req'] = 0 
            config['fec_firecode_25g_req'] = 0 
            config['fec_rs544_req'] = 0 
            config['fec_rs528_abil'] = 0 #data['fec_rs528_abil']
            config['fec_firecode_25g_abil'] = 0 #data['fec_firecode_25g_abil']
            
        elif set_fec == '10G_KR_FEC':
            config['fec_firecode_10g_abil'] = data['fec_firecode_10g_abil'] 
            config['fec_firecode_10g_req'] = 1
            config['fec_rs528_req'] = 0 
            config['fec_firecode_25g_req'] = 0 
            config['fec_rs544_req'] = 0 
            config['fec_rs528_abil'] = data['fec_rs528_abil']
            config['fec_firecode_25g_abil'] = data['fec_firecode_25g_abil']
        
        elif set_fec == '25G_KR_FEC':
            config['fec_firecode_10g_abil'] = data['fec_firecode_10g_abil'] 
            config['fec_firecode_10g_req'] = 0 
            config['fec_rs528_req'] = 0 
            config['fec_firecode_25g_req'] = 1 
            config['fec_rs544_req'] = 0 
            config['fec_rs528_abil'] = 0
            config['fec_firecode_25g_abil'] = 0
            
        elif set_fec == '25G_RS_528_FEC':
            config['fec_firecode_10g_abil'] = data['fec_firecode_10g_abil'] 
            config['fec_firecode_10g_req'] = 0 
            config['fec_rs528_req'] = 1
            config['fec_firecode_25g_req'] = 0 
            config['fec_rs544_req'] = 0
            config['fec_rs528_abil'] = data['fec_rs528_abil']
            config['fec_firecode_25g_abil'] = data['fec_firecode_25g_abil']

        elif set_fec == '25G_RS_544_FEC':
            config['fec_firecode_10g_abil'] = data['fec_firecode_10g_abil'] 
            config['fec_firecode_10g_req'] = 0 
            config['fec_rs528_req'] = 0 
            config['fec_firecode_25g_req'] = 0 
            config['fec_rs544_req'] = 1
            config['fec_rs528_abil'] = data['fec_rs528_abil']
            config['fec_firecode_25g_abil'] = data['fec_firecode_25g_abil']
            
        else:
            error_msg = 'Error _SetPhyConfigurationAQ: fec input is not valid. insert NO_FEC/10G_KR_FEC/25G_KR_FEC/25G_RS_528_FEC/25G_RS_544_FEC'
            raise RuntimeError(error_msg)

        status = ()
        status =  self.aq.SetPhyConfig(config)

        if debug == True:
            if status[0] == 0:
                print("Admin command successded") #TODO print admin command message 
            else:
                print("Admin command failed")
                print(config)
        if status[0] :
            error_msg = 'Error _SetPhyConfigurationAQ: _SetPhyConfig Admin command was not successful, retval {}'.format(status[1])
            raise RuntimeError(error_msg)   
        
    def SetPhyType(self, PhyType, rep_mode = 1, Location = "AQ"):
        '''This function sets Phy type
            argument:
                PhyType = str or list(for consortium phy type)
                rep_mode - int[2 bits] -- 00b reports capabilities without media, 01b reports capabilities including media, 10b reports latest SW configuration request
                Location = "AQ"     
            return:
                None
        '''
        if Location == "REG":
            self._SetPhyTypeReg()
        elif Location == "AQ":
            self._SetPhyTypeAq(PhyType, rep_mode)
     
        else:
            raise RuntimeError("Error SetLinkSpeed: Error Location, please insert location REG/AQ")

    def _SetPhyTypeReg(self):
        '''This function configures the phy type
            for debug only because SetPhyType by REG is not implimented.
        '''     
        raise RuntimeError("Set phy type by Reg is not implimented")
            
    def _SetPhyTypeAq(self, phy_type_list, rep_mode = 1):
        '''This function configure the Phy type on link
            argument:
                phy_type_list - list of phy types (list) bit definitions in Section 3.5.3.2.1 of CVL HAS
                rep_mode - int[2 bits] -- 00b reports capabilities without media, 01b reports capabilities including media, 10b reports latest SW configuration request
            return:
                None
        '''
        # for support str and list toghter

        if (type(phy_type_list) == str ):
            tmp_str = phy_type_list
            phy_type_list = []
            phy_type_list.append(tmp_str)
        else:
            pass
        

        config = {}
        phy_type = 0
        
        args = {}
        args['port'] = 0 #not relevant for CVL according to CVL Spec
        args['rep_qual_mod'] = 0 # 1 will report list of qualified modules, 0 will not
        args['rep_mode'] = rep_mode
        result = self.GetPhyAbilities(args) 
        
        if result[0]:
            error_msg = 'Error _SetPhyTypeAq: GetPhyAbilities Admin command was not successful, retval {}'.format(result[1])
            raise RuntimeError(error_msg)
            
        abilities = result[1]
        
        config['port'] = 0 #not relevant for CVL according to CVL Spec

        for recieved_phy_type in phy_type_list:
            if recieved_phy_type in self.set_Ability_PhyType_dict:
                phy_type = phy_type | (1 << self.set_Ability_PhyType_dict[recieved_phy_type])
            else:
                raise RuntimeError("Error _SetPhyTypeAq: PHY_type is not exist in set_Ability_PhyType_dict") 
        
        config['phy_type_0'] = get_bits_slice_value(phy_type,0,31)
        config['phy_type_1'] = get_bits_slice_value(phy_type,32,63)
        config['phy_type_2'] = get_bits_slice_value(phy_type,64,95)
        config['phy_type_3'] = get_bits_slice_value(phy_type,96,127)
        
        config['tx_pause_req'] = abilities['pause_abil']
        config['rx_pause_req'] = abilities['asy_dir_abil']
        config['low_pwr_abil'] = abilities['low_pwr_abil']
        config['en_link'] = 1
        config['en_auto_update'] = 1
        config['lesm_en'] = abilities['lesm_en']
        config['auto_fec_en'] = abilities['auto_fec_en']
        config['low_pwr_ctrl'] = abilities['low_pwr_ctrl']
        config['eee_cap_en'] = abilities['eee_cap']
        config['eeer'] = abilities['eeer']
        config['fec_firecode_10g_abil'] = abilities['fec_firecode_10g_abil']
        config['fec_firecode_10g_req'] = abilities['fec_firecode_10g_req']
        config['fec_rs528_req'] = abilities['fec_rs528_req']
        config['fec_firecode_25g_req'] = abilities['fec_firecode_25g_req']
        config['fec_rs544_req'] = abilities['fec_rs544_req']
        config['fec_rs528_abil'] = abilities['fec_rs528_abil']
        config['fec_firecode_25g_abil'] = abilities['fec_firecode_25g_abil']
        #print config
        status = ()
        status =  self.SetPhyConfig(config)
        print(status)
        
        if status[0]:
            error_msg = 'Error _SetPhyTypeAq: Admin command was not successful, retval {}'.format(status[1])
            raise RuntimeError(error_msg)   
            

    def SetFecSetting(self,set_fec, AmIDut,rep_mode =1 , Location = "AQ"):
        '''This function configure the FEC option for the link
            argument:
                set_fec - 'NO_FEC'/'25G_KR_FEC'/'25G_RS_528_FEC'/'25G_RS_544_FEC' (string) -- Enables or disables FEC Options on the link, bitfield defined in Section 3.4.4.1.3 of CVL HAS
                AmIDut - True/False
                rep_mode - int[2 bits] -- 00b reports capabilities without media, 01b reports capabilities including media, 10b reports latest SW configuration request
                Location = "REG" / "AQ" 
            return: None
        '''
        if Location == "REG":
            self._SetFecSettingReg()
        elif Location == "AQ":
            self._SetFecSettingAq(set_fec, AmIDut, rep_mode)
        else:
            raise RuntimeError("Err SetFecSetting: Error Location, please insert location REG/AQ")  
     
    def _SetFecSettingReg(self):
        '''This function configures the fec option
            for debug only because SetFecSetting by REG is not implimented.
        '''     
        raise RuntimeError("Set FEC by Reg is not implimented") 
     
    def _SetFecSettingAq(self,set_fec, AmIDut, rep_mode):
        '''This function configure the FEC option for the link
            input: 
                set_fec: NO_FEC/25G_KR_FEC/25G_RS_528_FEC/25G_RS_544_FEC (string) -- Enables or disables FEC Options on the link, bitfield defined in Section 3.4.4.1.3 of CVL HAS
        '''
        config = {}

        data = self.GetPhyAbilities({'port':0, 'rep_qual_mod':0, 'rep_mode':rep_mode}) ##TODO: check values
        abilities = data[1]
        
        config['port'] = 0 #not relevant for CVL according to CVL Spec
        
        if AmIDut:
            link_status = self.aq.GetLinkStatus({'port':0, 'cmd_flag':1})
            phy_type = link_status[1]
            
            config['phy_type_0'] = phy_type['phy_type_0']
            config['phy_type_1'] = phy_type['phy_type_1']
            config['phy_type_2'] = phy_type['phy_type_2']
            config['phy_type_3'] = phy_type['phy_type_3']
        
        else:
            config['phy_type_0'] = abilities['phy_type_0']
            config['phy_type_1'] = abilities['phy_type_1']
            config['phy_type_2'] = abilities['phy_type_2']
            config['phy_type_3'] = abilities['phy_type_3']
        
        config['tx_pause_req'] = abilities['pause_abil']
        config['rx_pause_req'] = abilities['asy_dir_abil']
        config['low_pwr_abil'] = abilities['low_pwr_abil']
        config['en_link'] = 1
        config['en_auto_update'] = 1
        config['lesm_en'] = abilities['lesm_en']
        config['auto_fec_en'] = 0 
        config['low_pwr_ctrl'] = abilities['low_pwr_ctrl']
        config['eee_cap_en'] = abilities['eee_cap']
        config['eeer'] = abilities['eeer']
        
        if set_fec == 'NO_FEC':
            config['fec_firecode_10g_abil'] = 0 
            config['fec_firecode_10g_req'] = 0 
            config['fec_rs528_req'] = 0 
            config['fec_firecode_25g_req'] = 0 
            config['fec_rs544_req'] = 0 
            config['fec_rs528_abil'] = 0
            config['fec_firecode_25g_abil'] = 0 
            
        elif set_fec == '10G_KR_FEC':
            config['fec_firecode_10g_abil'] = 1 
            config['fec_firecode_10g_req'] = 1 
            config['fec_rs528_req'] = 0 
            config['fec_firecode_25g_req'] = 0 
            config['fec_rs544_req'] = 0 
            config['fec_rs528_abil'] = 0
            config['fec_firecode_25g_abil'] = 0
        
        elif set_fec == '25G_KR_FEC':
            config['fec_firecode_10g_abil'] = 1 
            config['fec_firecode_10g_req'] = 1 
            config['fec_rs528_req'] = 0 
            config['fec_firecode_25g_req'] = 1 
            config['fec_rs544_req'] = 0 
            config['fec_rs528_abil'] = 0
            config['fec_firecode_25g_abil'] = 1 
            
        elif set_fec == '25G_RS_528_FEC' or set_fec == '25G_RS_544_FEC':
            config['fec_firecode_10g_abil'] = 1 
            config['fec_firecode_10g_req'] = 1 
            config['fec_rs528_req'] = 1 
            config['fec_firecode_25g_req'] = 1 
            config['fec_rs544_req'] = 1 
            config['fec_rs528_abil'] = 1
            config['fec_firecode_25g_abil'] = 1 
            
        else:
            error_msg = 'Error _SetFecSetting: input is not valid. insert NO_FEC/10G_KR_FEC/25G_KR_FEC/25G_RS_528_FEC/25G_RS_544_FEC'
            raise RuntimeError(error_msg)
        #print config
        status = ()
        status =  self.SetPhyConfig(config)
        
        if status[0]:
            error_msg = 'Error _SetFecSetting: Admin command was not successful, retval {}'.format(status[1])
            raise RuntimeError(error_msg)

    def GetPhytuningParams(self,debug = False):
        '''This function returns dict of phy tuning info 
            return: dictinary of opcode 9 from CVL-DFT-D8.*EX
        '''
        Phytuning_per_serdes_dict = {}
        Phytuning_final_dict = {}
        Phytuning_dict = {}
        driver = self.driver
        port_num = driver.port_number()
        #number_of_ports = 2#TOTO add reading driver indication
        current_device_number =  driver.device_number()
        number_of_ports = number_of_ports_dict[current_device_number]
        #print "number_of_ports: ",number_of_ports
        serdes_sel = []

        if number_of_ports == 1:# according pf to mac mapping in cvl spec 3.4.2.3.2
            quad = 0
            serdes_sel.append(0)

        if number_of_ports == 2:        
            phy_type = self.GetPhyType()
            
            if phy_type in NRZ_100G_phytype_list:
                serdes_sel = serdeses_per_portnum_4_dict[port_num] #serdes_sel = [1,2,3,4] for 100G-KR4 

            elif (phy_type in PAM4_100G_phytype_list) or (phy_type in NRZ_50G_phytype_list):
                serdes_sel = serdeses_per_portnum_2_dict[port_num]

            else: #for 50G-PAM4 and others
                serdes_sel.append(Serdes_mapping_per_pf_2_ports[port_num])

        elif number_of_ports == 4:   
            if self.GetMuxStatus():
                serdes_sel.append(Serdes_mapping_per_pf_4_ports_mux[port_num])
            else:
                serdes_sel.append(Serdes_mapping_per_pf_4_ports[port_num])

        elif number_of_ports == 8:        
            serdes_sel.append(Serdes_mapping_per_pf_8_ports[port_num])

        #print 'serdes_sel: ',serdes_sel

        for current_serdes in serdes_sel:
            Phytuning_final_dict[current_serdes] = {}

            for key,val in Phy_tuning_params_dict.iteritems():
                #args opcode,serdes_sel,data_in,debug=False
                ret_val = self.DnlCvlDftTest(0x9, current_serdes, val, debug=False)
                #print key,ret_val
                if ((int(ret_val,16) >> 15) == 1):# negative number
                    ret_val = '-' + hex(2**16 - int(ret_val,16))
                Phytuning_final_dict[current_serdes][key] = ret_val

        if debug:
            for key,val in Phytuning_final_dict.iteritems():
                print(key)
                Phytuning_dict = Phytuning_final_dict[key]
                keylist = Phytuning_dict.keys()
                keylist.sort()
                for k in keylist:
                    #handler.serial_print(str(k) + ': '+ str(Phytuning_dict[k]))
                    print(str(k) + ': '+ str(Phytuning_dict[k]))
                print()

        return Phytuning_final_dict

    def GetMuxStatus(self):
        '''This function return True/False according to signal controlling external mux (bit 2) - cvl spec 13.2.2.1.228
            input: None
            return:
                True - mux in used
                False - mux not in used
        '''
        # driver = self.driver
        reg_data = self.driver.read_csr(0xb81e0)
        mux_status = get_bit_value(reg_data,2)
        return mux_status

    def get_rsfec_corrected_codeword(self, quad= None):
        '''This function returns the rsfec corrected codeword see Section 22.3 of More than IP spec  ver 3.2
            argument:
                quad num according the pf number
            return:
                rsfec corrected codeword counter 32 bit
        '''
        if quad == None:
            quad,pmd_num = self._GetQuadAndPmdNumAccordingToPf()
        counter_low  = int(self.ReadMTIPRegister(self.MTIP_FEC_PCS_addr_dict[quad],2),16)
        counter_high = int(self.ReadMTIPRegister(self.MTIP_FEC_PCS_addr_dict[quad],3),16)
        return (counter_high << 16) | counter_low

    def get_rsfec_uncorrected_codeword(self, quad = None):
        '''This function returns the rsfec uncorrected codeword see Section 22.3 of More than IP spec  ver 3.2
            argument:
                quad num according the pf number
            return:
                rsfec uncorrected codeword counter 32 bit
        '''
        if quad == None :
            quad,pmd_num = self._GetQuadAndPmdNumAccordingToPf()
        counter_low  = int(self.ReadMTIPRegister(self.MTIP_FEC_PCS_addr_dict[quad],4),16)
        counter_high = int(self.ReadMTIPRegister(self.MTIP_FEC_PCS_addr_dict[quad],5),16)
        return (counter_high << 16) | counter_low   

    def get_rsfec_corrected_symbol_lane0(self, quad = None):
        '''This function returns the rsfec corrected symbol in lane 0 see Section 22.3 of More than IP spec  ver 3.2
            argument:
                quad num according the pf number
            return:
                rsfec corrected symbol in lane 0 counter 32 bit
        '''
        if quad == None:
            quad,pmd_num = self._GetQuadAndPmdNumAccordingToPf()
        counter_low  = int(self.ReadMTIPRegister(self.MTIP_FEC_PCS_addr_dict[quad],10),16)
        counter_high = int(self.ReadMTIPRegister(self.MTIP_FEC_PCS_addr_dict[quad],11),16)
        return (counter_high << 16) | counter_low
        
    def get_rsfec_corrected_symbol_lane1(self, quad = None):
        '''This function returns the rsfec corrected symbol in lane 1 see Section 22.3 of More than IP spec  ver 3.2
            argument:
                quad num according the pf number
            return:
                rsfec corrected symbol in lane 1 counter 32 bit
        '''
        if quad == None:
            quad,pmd_num = self._GetQuadAndPmdNumAccordingToPf()
        counter_low  = int(self.ReadMTIPRegister(self.MTIP_FEC_PCS_addr_dict[quad],12),16)
        counter_high = int(self.ReadMTIPRegister(self.MTIP_FEC_PCS_addr_dict[quad],13),16)
        return (counter_high << 16) | counter_low

    def get_rsfec_corrected_symbol_lane2(self, quad = None):
        '''This function returns the rsfec corrected symbol in lane 2 see Section 22.3 of More than IP spec  ver 3.2
            argument:
                quad num according the pf number
            return:
                rsfec corrected symbol in lane 2 counter 32 bit
        '''
        if quad == None:
            quad,pmd_num = self._GetQuadAndPmdNumAccordingToPf()
        counter_low  = int(self.ReadMTIPRegister(self.MTIP_FEC_PCS_addr_dict[quad],14),16)
        counter_high = int(self.ReadMTIPRegister(self.MTIP_FEC_PCS_addr_dict[quad],15),16)
        return (counter_high << 16) | counter_low

    def get_rsfec_corrected_symbol_lane3(self, quad = None):
        '''This function returns the rsfec corrected symbol in lane 3 see Section 22.3 of More than IP spec  ver 3.2
            argument:
                quad num according the pf number
            return:
                rsfec corrected symbol in lane 3 counter 32 bit
        '''
        if quad == None:
            quad,pmd_num = self._GetQuadAndPmdNumAccordingToPf()
        counter_low  = int(self.ReadMTIPRegister(self.MTIP_FEC_PCS_addr_dict[quad],16),16)
        counter_high = int(self.ReadMTIPRegister(self.MTIP_FEC_PCS_addr_dict[quad],17),16)
        return (counter_high << 16) | counter_low   
        
    def GetRSFecCounters(self, quad = None):
        '''This function returns all the rsfec counters
            argument:
                quad num according the pf number
            return: 
                dictinary of all rsfec counters --
                    'RS_FEC_corrected_codeword'
                    'RS_FEC_uncorrected_codeword'
                    'RS_FEC_corrected_symbol_lane0'
                    'RS_FEC_corrected_symbol_lane1'
                    'RS_FEC_corrected_symbol_lane2'
                    'RS_FEC_corrected_symbol_lane3'
        '''
        FEC_Counter_dict = {}
        if quad == None:
            quad,pmd_num = self._GetQuadAndPmdNumAccordingToPf()
        FEC_Counter_dict['RS_FEC_corrected_codeword'] = self.get_rsfec_corrected_codeword(quad)
        FEC_Counter_dict['RS_FEC_uncorrected_codeword'] = self.get_rsfec_uncorrected_codeword(quad)
        FEC_Counter_dict['RS_FEC_corrected_symbol_lane0'] = self.get_rsfec_corrected_symbol_lane0(quad)
        FEC_Counter_dict['RS_FEC_corrected_symbol_lane1'] = self.get_rsfec_corrected_symbol_lane1(quad)
        FEC_Counter_dict['RS_FEC_corrected_symbol_lane2'] = self.get_rsfec_corrected_symbol_lane2(quad)
        FEC_Counter_dict['RS_FEC_corrected_symbol_lane3'] = self.get_rsfec_corrected_symbol_lane3(quad)  
        return FEC_Counter_dict

    def get_kr_fec_corrected(self, quad = None):
        '''This function returns the kr fec corrected counter see Section 13.6.2.1.119 of CVL HAS
            Warning: the reg that is read here is "clear on read" this reg is also read in the proclib get_kr_fec_uncorrected
            argument:
                quad num according the pf number
            return:
                kr fec corrected counter
        '''
        if quad == None:
            quad,pmd_num = self._GetQuadAndPmdNumAccordingToPf()
        reg_addr = calculate_port_offset(0x0300010c, 0x100, quad)
        value = self.ReadEthwRegister(reg_addr)
        return get_bits_slice_value(int(value,16), 6, 11)  

    def get_kr_fec_uncorrected(self,quad = None):
        '''This function returns the kr fec uncorrected counter see Section 13.6.2.1.119 of CVL HAS
            Warning:  the reg that is read here is "clear on read" this reg is also read in the proclib get_kr_fec_corrected
            argument:
                quad num according the pf number
            return:
                kr fec uncorrected counter
        '''
        if quad == None:
            quad,pmd_num = self._GetQuadAndPmdNumAccordingToPf()
        reg_addr = calculate_port_offset(0x0300010c, 0x100, quad)
        value = self.ReadEthwRegister(reg_addr)
        return get_bits_slice_value(int(value,16), 12, 17)

    def GetKRFecCounters(self, quad = None):
        '''This function returns the kr fec corrected counter and uncorrected counter see Section 13.6.2.1.119 of CVL HAS
            argument:
                quad num according the pf number
            return:
                dictinary of kr fec corrected counter and uncorrected counter --
                    'KR_FEC_Corrected_Counter'
                    'KR_FEC_Uncorrected_Counter'
        '''
        FEC_Counter_dict = {}
        if quad == None:
            quad ,pmd_num = self._GetQuadAndPmdNumAccordingToPf()
        FEC_Counter_dict['KR_FEC_Corrected_Counter'] = self.get_kr_fec_corrected(quad)
        FEC_Counter_dict['KR_FEC_Uncorrected_Counter'] = self.get_kr_fec_uncorrected(quad)
        return FEC_Counter_dict

    def GetFECCounter(self,current_fec_stat = None,debug = False):
        '''This function returns all of the fec counters
            argument:
                quad num according the pf number
                debug if true prints the return values
            return:
                dictinary of all fec counters
        '''
        FEC_Counter_dict = {"KR_FEC_Corrected_Counter" : "N/A",
                            "KR_FEC_Uncorrected_Counter" : "N/A",
                            "RS_FEC_corrected_codeword":"N/A",
                            "RS_FEC_uncorrected_codeword":"N/A",
                            "RS_FEC_corrected_symbol_lane0":"N/A",
                            "RS_FEC_corrected_symbol_lane1":"N/A",
                            "RS_FEC_corrected_symbol_lane2":"N/A",
                            "RS_FEC_corrected_symbol_lane3":"N/A"}
        quad,pmd_num = self._GetQuadAndPmdNumAccordingToPf()
        #print "quad ",quad
        if current_fec_stat == None:
            current_fec_stat = self.GetCurrentFECStatus()

        if current_fec_stat == '25G_RS_528_FEC' or current_fec_stat == '25G_RS_544_FEC':
            FEC_Counter_dict.update(self.GetRSFecCounters(quad))
        elif current_fec_stat == '25G_KR_FEC' or current_fec_stat == '10G_KR_FEC':
            FEC_Counter_dict.update(self.GetKRFecCounters(quad))
        elif current_fec_stat == 'NO_FEC' or current_fec_stat == 'N/A':
            pass

        if debug:
            keylist = FEC_Counter_dict.keys()
            keylist.sort()
            for key in keylist:
                print(key,FEC_Counter_dict[key])

        return FEC_Counter_dict

##############################################################################
#                        LoopBack Section                                    #
##############################################################################

    def EnablePCSLoopback(self):
        '''This function enabled phy local loopback at the PCS level.
            input: None
            return: None
        '''
        phy_lpbk_args = {}
        phy_lpbk_args['port'] = 0 #not relevant for CVL according to CVL Spec
        phy_lpbk_args['index'] = 0 #for the outermost PHY
        phy_lpbk_args['enable'] = 1 #loopback enabled
        phy_lpbk_args['type'] = 0 #local loopback
        phy_lpbk_args['level'] = 1 #the loopback is done at the PCS level

        status = self.SetPhyLoopback(phy_lpbk_args)

        if status[0]:
            error_msg = 'Error EnablePCSLoopback: Admin command was not successful, retval {}'.format(status[1])
            raise RuntimeError(error_msg)

    def EnablePMDLoopback(self):
        '''This function enabled phy local loopback at the PMD level.
            input: None
            return: None
        '''
        phy_lpbk_args = {}
        phy_lpbk_args['port'] = 0 #not relevant for CVL according to CVL Spec
        phy_lpbk_args['index'] = 0 #for the outermost PHY
        phy_lpbk_args['enable'] = 1 #loopback enabled
        phy_lpbk_args['type'] = 0 #local loopback
        phy_lpbk_args['level'] = 0 #the loopback is done at the PMD level

        status = self.SetPhyLoopback(phy_lpbk_args)

        if status[0]:
            error_msg = 'Error EnablePMDLoopback: Admin command was not successful, retval {}'.format(status[1])
            raise RuntimeError(error_msg)

    def EnableMACLoopback(self):
        '''This function enables MAC loopback localy
            input: None 
            returnt: None
        '''
        AQ_args = dict()
        AQ_args["loopback mode"] = 1
        status = self.SetMacLoopback(AQ_args)

        if status[0]:
            error_msg = "Error EnableMACLoopback: Admin command was not successful, retval {}".format(status[1])
            raise RuntimeError(error_msg)

    def DisablePCSLoopback(self):
        '''This function disabled phy local loopback at the PCS level.
            input: None
            return: None
        '''
        phy_lpbk_args = {}
        phy_lpbk_args['port'] = 0 #not relevant for CVL according to CVL Spec
        phy_lpbk_args['index'] = 0 #for the outermost PHY
        phy_lpbk_args['enable'] = 0 #loopback disabled
        phy_lpbk_args['type'] = 0 #local loopback
        phy_lpbk_args['level'] = 1 #the loopback is done at the PCS level

        status = self.SetPhyLoopback(phy_lpbk_args)
        if status[0]: 
            error_msg = 'Error DisablePCSLoopback: Admin command was not successful, retval {}'.format(status[1])
            raise RuntimeError(error_msg)

    def DisablePMDLoopback(self):
        '''This function disabled phy local loopback at the PMD level.
            input: None
            return: None
        '''
        phy_lpbk_args = {}
        phy_lpbk_args['port'] = 0 #not relevant for CVL according to CVL Spec
        phy_lpbk_args['index'] = 0 #for the outermost PHY
        phy_lpbk_args['enable'] = 0 #loopback disabled
        phy_lpbk_args['type'] = 0 #local loopback
        phy_lpbk_args['level'] = 0 #the loopback is done at the PMD level
        status = self.SetPhyLoopback(phy_lpbk_args)

        if status[0]: 
            error_msg = 'Error DisablePMDLoopback: Admin command was not successful, retval {}'.format(status[1])
            raise RuntimeError(error_msg)

    def DisableMACLoopback(self):
        ''' This method diables MAC loopback 
            input: None
            return: None
        '''
        AQ_args = dict()
        AQ_args["loopback mode"] = 0
        status = self.SetMacLoopback(AQ_args)

        if status[0]:
            error_msg = "Error DisableMACLoopback: Admin command was not successful, retval{}".format(status[1])
            raise RuntimeError(error_msg)


###############################################################################
#       Work arounds sections                                                 #
###############################################################################

    def Reset_WA(self,reset = "corer",PF = "00"):
        '''This function is a work around for performing resets 
            arguments: string reset = "pfr, corer, globr, empr, flr, pcir, bmer, vfr, vflr" 
                       string PF (physical function) = "00-08"
        '''
        driver = self.driver
        command = "svdt -r cvl:"+PF+" "+reset
        self._ExecuteLinuxCommand(command)


    # all 3 func below is work around for PCIe indication reading
    def _ExecuteLinuxCommand(self, command):
        '''This function execute linux command
            argument: command (str)
            return: output (str)
        '''
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        return output

    def GetPCIECurrentLinkSpeed_WA(self):
        '''This function returns PCIE link speed from linux command.
            argument: None
            return: 'Gen1' / 'Gen2' / 'Gen3' / 'Gen4'
        '''
        driver = self.driver
        dev_info_dict = driver.get_device_info()

        tmp_str = "lspci | grep " + dev_info_dict['dev_id']
        #print tmp_str
        tmp = self._ExecuteLinuxCommand(tmp_str)
        tmp = tmp.split(" ")


        comm = "ls -la /sys/bus/pci/devices | grep " + tmp[0]

        tmp = self._ExecuteLinuxCommand(comm)
        tmp = tmp.split("/")


        domain = tmp[-2].split(":")
        domain = domain[1] + ":" + domain[2]

        comm = "sudo lspci -vvv -s " + domain + " | grep LnkSta"
        tmp = self._ExecuteLinuxCommand(comm)


        if "16GT/s" in tmp:
            #print "Gen4"   
            return "Gen4"
        elif "8GT/s" in tmp:
            #print "Gen3"   
            return "Gen3"
        elif "5GT/s" in tmp:
            #print "Gen2"
            return "Gen2"
        elif "2.5GT/s" in tmp:
            #print "Gen1"   
            return "Gen1"
        else:
            #print "N/A"
            return "N/A"

    def GetPCIECurrentLinkWidth_WA(self):
        '''This function returns PCIE link width from linux command.
            argument: None
            return: 'x1' / 'x2' / 'x4' / 'x16'
        '''
        driver = self.driver
        dev_info_dict = driver.get_device_info()

        tmp_str = "lspci | grep " + dev_info_dict['dev_id']
        #print tmp_str
        tmp = self._ExecuteLinuxCommand(tmp_str)
        tmp = tmp.split(" ")


        comm = "ls -la /sys/bus/pci/devices | grep " + tmp[0]

        tmp = self._ExecuteLinuxCommand(comm)
        tmp = tmp.split("/")


        domain = tmp[-2].split(":")
        domain = domain[1] + ":" + domain[2]

        comm = "sudo lspci -vvv -s " + domain + " | grep LnkSta"
        tmp = self._ExecuteLinuxCommand(comm)


        if "Width x16" in tmp:
            #print "x16"    
            return "x16"
        elif "Width x8" in tmp:
            #print "Gx8"    
            return "x8"
        elif "Width x4" in tmp:
            #print "x4"
            return "x4"
        elif "Width x2" in tmp:
            #print "x2" 
            return "x2"
        elif "Width x1" in tmp:
            #print "x1" 
            return "x1"
        else:
            #print "N/A"
            return "N/A"

    ######################################################################################################
    ###############################          Rotem - debug is needed            ##########################
    ######################################################################################################  

    def SetEEESetting_D(self, set_eee, Location = "AQ"):
        '''This function configure eee for the link.
            argument:
                set_eee: [2 bytes] -- bitfield defined in Section 3.5.7.6.8 of CVL has to enable or disable advertisement of EEE capabilities
                Location = "REG" / "AQ"

        '''
        if Location == "REG":
            self._SetEEESettingReg()
        elif Location == "AQ":
            self._SetEEESettingAq(set_eee)
        else:
            raise RuntimeError("Err SetEEESetting: Error Location, please insert location REG/AQ")  

    def _SetEEESettingReg(self):
        '''This function configure eee for the link.
            for debug only because SetEEESetting_D by REG is not implimented.
        '''
        raise RuntimeError("Set EEE by Reg is not implimented") 
     
    def _SetEEESettingAq_D(self, set_eee):
        '''This function configure eee for the link.
            input: 
                set_eee: [2 bytes] -- bitfield defined in Section 3.5.7.6.8 of CVL has to enable or disable advertisement of EEE capabilities
        '''
        config = {}
        abilities = self.GetPhyAbilities({'port':0, 'rep_qual_mod':0, 'rep_mode':2}) ##TODO: check values
        
        config['port'] = 0 #not relevant for CVL according to CVL Spec
        config['phy_type_0'] = abilities['phy_type_0']
        config['phy_type_1'] = abilities['phy_type_1']
        config['phy_type_2'] = abilities['phy_type_2']
        config['phy_type_3'] = abilities['phy_type_3']
        config['pause_abil'] = abilities['pause_abil']
        config['asy_dir_abil'] = abilities['asy_dir_abil']
        config['low_pwr_abil'] = abilities['low_pwr_abil']
        config['en_link'] = 1
        config['en_auto_update'] = 1
        config['lesm_en'] = abilities['lesm_en']
        config['auto_fec_en'] = abilities['auto_fec_en'] ##TODO: check the value according to spec
        config['low_pwr_ctrl'] = abilities['low_pwr_ctrl']
        
        eee_opt = 0
        if set_eee in set_Ability_EEE_dict:
            eee_opt = 1 << set_Ability_EEE_dict[set_eee]
            config['eee_cap_en'] = eee_opt
        else:
            raise RuntimeError("Error _SetEEESetting: set_eee is not exist in set_Ability_EEE_dict")
        
        config['eeer'] = abilities['eeer']
        config['fec_opt'] = abilities['fec_opt']
        
        status = ()
        status =  self.SetPhyConfig(config)
        
        if status[0]:
            error_msg = 'Error _SetEEESetting: Admin command was not successful, retval {}'.format(status[1])
            raise RuntimeError(error_msg)
        

    def LinkManagementDisable(self):
        '''This function disable firmware's link managment. 
            argument: none
            return: none
        '''

        args = {'port':0, 'index':0, 'cmd_flags':0x10}
        status = self.SetPhyDebug(args)

        if status[0]: 
            error_msg = 'Error LinkManagementDisable: Admin command was not successful, retval {}'.format(status[1])
            raise RuntimeError(error_msg)

    def LinkManagementEnable(self):
        '''This function enable firmware's link managment. 
            argument: none
            return: none
        '''

        args = {'port':0, 'index':0, 'cmd_flags':0}
        status = self.SetPhyDebug(args)

        if status[0]: 
            error_msg = 'Error LinkManagementEnable: Admin command was not successful, retval {}'.format(status[1])
            raise RuntimeError(error_msg)

     
    ######################################################################################################
    ###############################           Debug section             ##################################
    ######################################################################################################
     
    def DebugReadDnlPstores(self, pstores_number_to_read,debug=False):
        '''read PSTO for debug.
            arguments: 
                context - context number
                pstores_number_to_read - PSTO number to read
            return:
                print all pstors
        '''
        pstores = self._DnlReadPstore(self, pstores_number_to_read,debug)
        print("Pstors: ",pstores)
     
    def DebugWriteDnlStore(context, store_type, store_index, value,debug=False):
        '''write PSTO for debug.
            arguments: 
                context - context number
                store_type - 0 for STO, 1 for PSTO
                store_index - offest
                value - value to write
        '''
        _DnlWriteStore(context, store_type, store_index, value,debug)


    ######################################################################################################
    ###############################           DNL section             ####################################
    ######################################################################################################

    def DnlCvlDftTest(self, opcode,serdes_sel,data_in,debug=False):
        '''
            This function run DNL dft test according to the list below (CVL-DFT-DO.8EX file).
             input:
                opcode - dft opcode according to the below list 
                serdes_sel - on which serdes to run the dft test
                data_in - input data (relevant per opcode)
            return:
                output psto list
                                  
            opcode list:
                support working with CVL-DFT-tests define in CVL-DFT-DO.8EX file
                opcode(Hex)          Value
                0                    get_version
                1                    disable tx
                2                    speed selection
                3                    polarity control
                4                    tx eq settings
                5                    select_tx_pattern
                6                    select_rx_pattern
                7                    get_error_counter
                8                    inject error
                9                    get_rx_eq
                A                    set_rx_eq
                B                    rxeq control
                C                    loopback
                D                    kr_training_status
                E                    eye_monitor
                F                    an_state_machine
                10                   get tx eq settings
                11                   get_temperature
        '''
        driver = self.driver
        CVL_DFT_TEST_ACT_IT = 0x1129
        context = driver.port_number()
        sto_0 =  (opcode << 20)| (serdes_sel << 16) | data_in
        sto_1 = 0
        sto_2 = 0
        sto_3 = 0
        ret_val = self._DnlCallActivity(CVL_DFT_TEST_ACT_IT,context, sto_0, sto_1, sto_2, sto_3,debug=False)
        sto_0 = hex(ret_val[0]).replace('L','')
        sto_1 = hex(ret_val[1]).replace('L','')
        sto_2 = hex(ret_val[2]).replace('L','')
        sto_3 = hex(ret_val[3]).replace('L','')

        # check for errors define in CVL-DFT-DO.8EX file
        if int(sto_0,16) == 0xb00fb00f:
            print("ERROR: Invalid DATA_IN")
        elif int(sto_0,16) == 0xbeefbeef:
            print("ERROR: Invalid SERDES_SEL")
        elif int(sto_0,16) == 0xbeefbe0f:
            print("ERROR: Invalid OP_CODE")

        if debug:
            print("sto_0: ",sto_0)
            print("sto_1: ",sto_1)
            print("sto_2: ",sto_2)
            print("sto_3: ",sto_3)
        return sto_0

    def ReadDnlPstore(self, psto_index,debug=False):
        '''
            This function return value from psore.
            argument: psto_index 
            return: value (hex)
        '''
        driver = self.driver
        context = driver.port_number()

        ret_val = self._DnlReadPstore(context,psto_index,debug=False)
        return hex(ret_val)

    def DnlGetPhyInfo(self):
        '''
            This function calls DNL script get_phy_info
            inputs:
                dict --
                    'context' : int
                    'go': int (1 bit) sto3 bit31
                    'node_handle': int (10 bits) sto0 bit9-0  
            returns:
                st -- type(dict)
                    'phy_id': int (32 bits) sto0 bit31-0
                    'phy_fw_l': int (32 bits) sto1 bit31-0
                    'phy_fw_h': int (32 bits) sto2 bit31-0
                    'done': int (1 bit) sto3 bit31              
        '''    
        sto0 = 1
        sto1 = 0
        sto2 = 0   
        sto3 = 1 << 31
       
        #helper = LM_Validation()
        act_id = 0x000E
        status = self._DnlCallActivity(act_id, 0, sto0, sto1, sto2, sto3)
        
        st = {}

        st['phy_id'] = hex(status[0]).replace('L','')
        st['phy_fw_l'] = hex(status[1]).replace('L','')
        st['phy_fw_h'] = hex(status[2]).replace('L','')
        st['done'] = hex(status[3] >> 31).replace('L','') 
        return st
     
#########################################################################################################
######################           Support SECTION               ##########################################
#########################################################################################################
     
    def GetPortNumber(self):
        '''
            This function return port number
            argument: None
            return: port number (int)
        '''
        return self.driver.port_number()

    def ReadCsrRegister(self,offset):
        '''
            This function return CSR register value according to CSR register address.
            argument: offset - CSR register address
            return: value - CSR register value
        '''
        return self.driver.read_csr(offset)
            
    def WriteCsrRegister(self,offset,value):
        '''
            This function write value to CSR register address.
            arguments: 
                offset - CSR register address
                value - value to write
            return: None
        '''
        self.driver.write_csr(offset, value)

    def ReadEthwRegister(self, address):
        '''
            This function support read from ethw.
            supporting read/write via SBiosf to neighbor device.
            arguments: 
                address - address to read in the neighbor device CSRs.
            return: 
                value - return value from the neighbor device.
        ''' 
        return_val = self.NeighborDeviceRead(0x2,0,1, address)
        return return_val

    def WriteEthwRegister(self,address,data):
        '''
            this function support write to ethw.
            supporting read/write via SBiosf to neighbor device.
            arguments: 
                address - address to write in the neighbor device CSRs.
                data - data to write in the neighbor device CSRs.
        ''' 
        self.NeighborDeviceWrite(0x2,1,1, address,data)
        pass

    def ReadMTIPRegister(self, offset,address,debug = False):
        '''
            this function read from MTIP in ethw.
            supporting read/write via SBiosf to neighbor device.
            arguments: 
                offset - according CVL TLM Documents.
                address - address to read according MTIP Spec.
            return: 
                value - return value from the neighbor device.
        ''' 
        addr = offset << 20
        addr  = addr | (address << 2)
        ret_val = self.ReadEthwRegister(addr)
        if debug:
            print("Reading from: ", hex(addr))
            print("return value: ", ret_val)
        return ret_val

    def NeighborDeviceWrite(self,dest,opcode,addrlen,address,data):
        '''
            this function support Neighbor Device Request via AQ (CVL spec B.2.1.2)
            supporting read/write via SBiosf to neighbor device.
            arguments: 
                dest - Neighbor Device address, according Table 3-33, in 3.3.4.1 CVL Spec.
                opcode - read/write etc...  according Table 3-34, in 3.3.4.1 CVL Spec
                addrlen - address length 0: 16 bit, 1: 48 bits. according Table B-8, appandix B.3.1 CVL spec
                address - address to read in the neighbor device CSRs.
                data - data to be written
            return: 
                None
        ''' 
        struct = cvl_structs()
        SbIosfMassageDict = struct.SbIosfMassageStruct()
        buffer = []
     
        # First DW
        buffer.append(SbIosfMassageDict['dest'] | dest)
        buffer.append(SbIosfMassageDict['source'])
        buffer.append(SbIosfMassageDict['opcode'] | opcode)
        Byte4_1stDW = (SbIosfMassageDict['EH'] << 7) | ((SbIosfMassageDict['addrlen'] | addrlen ) << 6) | (SbIosfMassageDict['Bar'] << 3 ) | SbIosfMassageDict['Tag']
        buffer.append(Byte4_1stDW)
     
        # Second DW - Should be ignored according tanya
        # Byte1_2ndDW = (SbIosfMassageDict['EH_2ndDW'] << 7) | SbIosfMassageDict['exphdrid']
        # buffer.append(Byte1_2ndDW)
        # Byte2_2ndDW = SbIosfMassageDict['sai'] & 0xFF
        # buffer.append(Byte2_2ndDW)
        # Byte3_2ndDW = (SbIosfMassageDict['sai'] >> 8) & 0xFF
        # buffer.append(Byte3_2ndDW)
        # Byte4_2ndDW = SbIosfMassageDict['rs'] & 0xF
        # buffer.append(Byte4_2ndDW)
     
        # Third DW
        Byte1_3rdDW =(SbIosfMassageDict['Sbe'] << 4) | (SbIosfMassageDict['fbe'] | 0xF) # the fbe value taken from BDX team
        buffer.append(Byte1_3rdDW)
        buffer.append(SbIosfMassageDict['Fid'])
        Byte3_3rdDW = address & 0xFF
        buffer.append(Byte3_3rdDW)
        Byte4_3rdDW = (address >> 8) & 0xFF
        buffer.append(Byte4_3rdDW)
     
        # four DW
        Byte1_4rdDW = (address >> 16) & 0xFF
        buffer.append(Byte1_4rdDW)
        Byte2_4rdDW = (address >> 24) & 0xFF
        buffer.append(Byte2_4rdDW)
        Byte3_4rdDW = 0
        buffer.append(Byte3_4rdDW)
        Byte4_4rdDW = 0
        buffer.append(Byte4_4rdDW)

        # Addidional DW's for writing
        Byte1_AdDW = data & 0xFF
        buffer.append(Byte1_AdDW)
        Byte2_AdDW = (data >> 8 ) & 0xFF
        buffer.append(Byte2_AdDW)
        Byte3_AdDW = (data >> 16 ) & 0xFF
        buffer.append(Byte3_AdDW)
        Byte4_AdDW = (data >> 24 ) & 0xFF
        buffer.append(Byte4_AdDW)
        return_buffer = self._NeighborDeviceRequestAq(0,buffer)



    def _to_unsigned(self, value):
        '''
            This function convert sign value to unsigned.
            argument: value (sign number)
            return: unsigned value
        '''
        if value >= 0:
            return value
        else:
            return value + 2**8
     
    def SetMdioBit(self, Page,Register,BitNum):
        '''
            This function set MDIO bit.
        '''
        reg_value = self.driver.read_phy_register(Page, Register, self.driver.port_number())
        print(hex(reg_value))
        reg_value = reg_value | (1 << BitNum)
        print(hex(reg_value))
        self.driver.write_phy_register(Page, Register, self.driver.port_number(), reg_value)
     
    def ClearMdioBit(self,Page,Register,BitNum):
        '''
            This function clear MDIO bit.
        '''
        reg_value = self.driver.read_phy_register(Page, Register, self.driver.port_number())
        print(hex(reg_value))
        reg_value = reg_value & ~(1 << BitNum)
        print(hex(reg_value))
        self.driver.write_phy_register(Page, Register, self.driver.port_number(), reg_value)

    def CheckDeviceAliveness(self):
        '''
            This function returns true if the device is alive or false otherwise
            it's done for PCIe issue .
               return: True/false
        '''
        reg_addr = calculate_port_offset(0x001E47A0, 0x4, self.driver.port_number())
        reg_data = self.driver.read_csr(reg_addr)
        if ( reg_data == 0xffffffff or reg_data == 0xdeadbeef):
            return False
        else:
            return True

    def PrintLoopbackStatus(self):
        gls = dict()
        gls["port"] = 0 
        gls["cmd_flag"] = 0
        status, data = self.aq.GetLinkStatus(gls)

        if status:
            raise RuntimeError("Error GetLinkStatusAfterParsing: Admin command was not successful")  

        if data["lcl_lpbk"]:
            print("PHY local loopback enabled")
        else:
            print("PHY local loopback disabled")

        if data["rem_lpbk"]:
            print("PHY remote loopback enabled")
        else:
            print("PHY remote loopback disabled")

        if data["mac_lpbk"]:
            print("MAC local loopback enabled")
        else:
            print("MAC local loopback disabled")

        #TODO print the PHY index that performs the loopback 0 = outermost

    def GetLinkStatusAfterParsing(self):
        '''
            This function return dictionary that contain phy and mac link status and speed, fec mode.
            arguments: None
            return: dict--
                        "PhyType"
                        "MacLinkStatus"
                        "MacLinkSpeed"
                        "EnabeldFEC"
        '''
        return_dict = {}
        gls = {}
        gls['port'] = 0 #not relevant for CVL according to CVL Spec
        gls['cmd_flag'] = 1
     
        result = self.aq.GetLinkStatus(gls)
        
        if not result[0]: # if Admin command was successful - False
            data = result[1]
        else:
            raise RuntimeError("Error GetLinkStatusAfterParsing: Admin command was not successful")  

        #keylist = data.keys()
        # keylist.sort()
        # for key in keylist:
        #    print key,data[key]

        ####### get current phy type  ###############################################
        phy_type = (data['phy_type_3'] << 96 ) | (data['phy_type_2'] << 64 ) | (data['phy_type_1'] << 32 ) | data['phy_type_0']
     
        if self.Get_Phy_Type_Status_dict:
            for i in range(len(self.Get_Phy_Type_Status_dict)):
                if ((phy_type >> i) & 0x1):
                        break
        #print "phy type : ",Get_Phy_Type_Status_dict[i]
        return_dict["PhyType"] = self.Get_Phy_Type_Status_dict[i]



        ####### get Mac Link status  ###############################################
        status = data['link_sts']
        if status == 1:
            status = "Up"
        else:
            status = "Down"
        #print "MacLinkStatus: ",status
        return_dict["MacLinkStatus"] = status



        ####### get Mac Link status  ##############################################
        link_speed = 'N/A'
        current_link_speed = data['current_link_speed']

        if self.Get_Speed_Status_dict:
            for key, val in self.Get_Speed_Status_dict.items():
                mask = 1 << key
                if current_link_speed & mask:
                    link_speed= val

            # if data['link_speed_10m']:
            #     link_speed = self.Get_Speed_Status_dict[0]
                
            # elif data['link_speed_100m']:
            #     link_speed = self.Get_Speed_Status_dict[1]
                
            # elif data['link_speed_1000m']:
            #     link_speed = self.Get_Speed_Status_dict[2]
                
            # elif data['link_speed_2p5g']:
            #     link_speed = self.Get_Speed_Status_dict[3]
                
            # elif data['link_speed_5g']:
            #     link_speed = self.Get_Speed_Status_dict[4]
                
            # elif data['link_speed_10g']:
            #     link_speed = self.Get_Speed_Status_dict[5]
                
            # elif data['link_speed_20g']:
            #     link_speed = self.Get_Speed_Status_dict[6]
                
            # elif data['link_speed_25g']:
            #     link_speed = self.Get_Speed_Status_dict[7]
                
            # elif data['link_speed_40g']:
            #     link_speed = self.Get_Speed_Status_dict[8]
                
            # elif data['link_speed_50g']:
            #     link_speed = self.Get_Speed_Status_dict[9]
                
            # elif data['link_speed_100g']:
            #     link_speed = self.Get_Speed_Status_dict[10]
                
            # elif data['link_speed_200g']:
            #     link_speed = self.Get_Speed_Status_dict[11]

        else:
            raise RuntimeError("Error GetLinkStatusAfterParsing: Get_Speed_Status_dict is not defined")

        return_dict["MacLinkSpeed"] = link_speed

        ####### get negotiation FEC on link  #############
        FEC_status_list = []
        {0:'25G_KR_FEC_Enabled',1:'25G_RS_528_FEC_Enabled',2:'RS_544_FEC_Enabled'}
        if data['10g_kr_fec']:
            FEC_status_list.append("10G_KR_FEC_Enabled")
        if data['25g_kr_fec']:
            FEC_status_list.append("25G_KR_FEC_Enabled")
        elif data['25g_rs_528']:
            FEC_status_list.append("25G_RS_528_FEC_Enabled")
        elif data['rs_544']:
            FEC_status_list.append("RS_544_FEC_Enabled")
        else:
            FEC_status_list.append("No FEC")

        return_dict["EnabeldFEC"] = FEC_status_list

        #print return_dict
        return return_dict

    def _ReturnAbilitiesListForDebugPrint(tmplist,RegToParse,RegToParseDict):
        '''This function return list with the abilities from register after parsing.
            this function is for debug and used only at DBG_print_cvl_info().
            arguments:
                tmplist - list that contains the abilities after parsing
                RegToParse - register address
                RegToParseDict - dictionary that contain tha parsing according to specific bit
            return:
                tmplist
        '''
        if RegToParse == 0:
            #print 'None'
            tmplist.append('None')
        else:
            for i in range(32):
                if (RegToParse & 1) == 1:
                    #print PRT_AN_LP_NP_dict[i]
                    tmplist.append(RegToParseDict[i])
                RegToParse = RegToParse >> 1
        return tmplist

    def _GetQuadAndPmdNumAccordingToPf(self):
        '''this function return the quad num and pmd num according the pf number
            return: tuple -- (quad number, pmd number)
        '''
        # get the real PCS address according to pf number
        driver = self.driver
        port_num = driver.port_number()
        current_device_number =  driver.device_number()
        number_of_ports = 8 
        if number_of_ports == 1:# according pf to mac mapping in cvl spec 3.4.2.3.2
            quad = 0
            pmd_num = 0
        if number_of_ports == 2:        
            quad = self.data.quad_for_2_ports_dict[port_num]        
            pmd_num = self.data.pmd_num_for_2_ports_dict[port_num]
        elif number_of_ports == 4:     
            if self.GetMuxStatus():
                quad = self.data.quad_for_4_ports_mux_dict[port_num]
                pmd_num = self.pmd_num_for_4_ports_mux_dict[port_num]
            else:
                quad = self.data.quad_for_4_ports_dict[port_num]        
                pmd_num = self.pmd_num_for_4_ports_dict[port_num]
        elif number_of_ports == 8:        
            quad = self.data.quad_for_8_ports_dict[port_num]
            pmd_num = self.pmd_num_for_8_ports_dict[port_num]

        #print "quad: ", quad
        #print "port_num: ", port_num
        #print "pmd_num: ", pmd_num

        return quad,pmd_num

    def _GetPcsOffset(self):
        '''this func return the pcs num according the pf number.
            input: None
            Return: pcs offset
        '''
        quad,pmd_num = self._GetQuadAndPmdNumAccordingToPf()
            
        #print "quad:",quad
        #print "pmd_num:",pmd_num

        link_speed = self.GetMacLinkSpeed()
        #print "link_speed: ",link_speed

        if link_speed == "100G":
            pcs_offset = self.data.MTIP_100_PCS_Addr_Dict[quad]

        elif (link_speed == "10G" or link_speed == "25G" or link_speed == "40G" or link_speed == "50G"):
            if quad == 0:
                pcs_offset = self.MTIP_10_25_40_50_PCS_Quad_0_Addr_Dict[pmd_num]
            elif quad == 1:
                pcs_offset = self.MTIP_10_25_40_50_PCS_Quad_1_Addr_Dict[pmd_num]
            
        elif link_speed == "1G":
            pcs_offset = None
        #print "PCS offset ", hex(pcs_offset)
        return pcs_offset

    def GetPcsAdvencedInfo(self,debug = 0):
        '''This function print PCS Advenced info 
            input: debug -- if true, print the return list
            return: list -- 
                        for pcs link status 2: Receive fault, Transmit fault
                        for PCS BaseR status 1: Receive link status, High BER, Block lock
                        for PCS BaseR status 2: Latched block lock. (LL), Latched high BER. (LH)
        '''
        return_list = []
        # get the real PCS address according to pf number
        pcs_offset = self._GetPcsOffset()

        #pcs_link_status_1 = ReadMTIPRegister(pcs_offset,1)#PCS link status 1
        return_list.append("")
        pcs_link_status_2 = int(self.ReadMTIPRegister(pcs_offset,8),16)#PCS link status 2
        return_list.append("#####  pcs link status 2  #####")
        for i in range(6):
            pcs_link_status_2_run_bit = (pcs_link_status_2 >> i) & 1
            if  pcs_link_status_2_run_bit == 1:
                return_list.append(self.pcs_link_status_2_dict[i])
        return_list.append("Receive fault: " + str(get_bit_value(pcs_link_status_2,10)))
        return_list.append("Transmit fault: " + str(get_bit_value(pcs_link_status_2,11)))

        return_list.append("")
        pcs_baser_status_1 = int(self.ReadMTIPRegister(pcs_offset,32),16)#PCS BaseR status 1
        return_list.append("#####  PCS BaseR status 1  #####")
        return_list.append("Receive link status: " + str(get_bit_value(pcs_baser_status_1,12)))
        return_list.append("High BER: " + str(get_bit_value(pcs_baser_status_1,1)))
        return_list.append("Block lock: " + str(get_bit_value(pcs_baser_status_1,0)))

        return_list.append("")
        pcs_baser_status_2 = int(self.ReadMTIPRegister(pcs_offset,33),16)#PCS BaseR status 2
        return_list.append("#####  PCS BaseR status 2  #####")
        return_list.append("Latched block lock. (LL): " + str(get_bit_value(pcs_baser_status_1,15)))
        return_list.append("Latched high BER. (LH): " + str(get_bit_value(pcs_baser_status_1,14)))

        #print "pcs_link_status_2 ",hex(pcs_link_status_2)
        #print "pcs_baser_status_1 ",hex(pcs_baser_status_1)
        #print "pcs_baser_status_2 ",hex(pcs_baser_status_2)
        current_fec_stat = self.GetCurrentFECStatus()
        if current_fec_stat == '25G_RS_528_FEC_Enabled' or current_fec_stat == 'RS_544_FEC_Enabled': 
            return_list.append("")
            return_list.append("#####  PCS FEC conters  #####")
            return_list.append("FEC: " + current_fec_stat)
            FEC_counter_dict = self.GetFECCounter(current_fec_stat)
            for key,val in FEC_counter_dict.iteritems():
                #print key, ":", val
                return_list.append(key + ": " + str(val))   

        return_list.append("")

        if debug:
            for i in return_list:
                print(i)

        return return_list

    #########################################################################################################
    ######################           Statistics               #############################################
    #########################################################################################################



    def GetBERMacStatistics(self):
        '''This function return dictinary with mac link statistics for BER test.
            argument: None
            return: 
                dictionary -- contain the statistics indications    
                    'TotalPacketRecieve'
                    'TotalPacketTransmite'
                    'Mac_link_status'
                    'Mac_link_speed'
        '''

        MacStatistics = {}
        
        MacStatistics['TotalPacketRecieve'] = self.GetPRC()['TotalPRC']
        MacStatistics['TotalPacketTransmite'] = self.GetPTC()['TotalPTC']
        
        #return Mac link status
        MacStatistics['Mac_link_status'] = self.GetMacLinkStatus()
        
        #return link speed
        MacStatistics['Mac_link_speed'] = self.GetMacLinkSpeed()

        return MacStatistics

    def GetMacStatistics(self, Location = "AQ",GlobReset = 0):
        '''This function return dictinary with mac link statistics
            argument:
            return: 
                dictionary -- contain the statistics indications    
                    'Mac_link_status'
                    'Mac_link_speed'
                    'Phy_Type'
        '''
        Mac_link_statistic_dict = {}
        #return Mac link status
        Mac_link_statistic_dict['Mac_link_status'] = self.GetMacLinkStatus(Location)
        #return  Mac link speed
        Mac_link_statistic_dict['Mac_link_speed'] = self.GetMacLinkSpeed(Location)
        if GlobReset == 0:
            Mac_link_statistic_dict['Phy_Type'] = self.GetPhyType()
            Mac_link_statistic_dict['Current_FEC'] = self.GetCurrentFECStatus()
        return Mac_link_statistic_dict

    def GetPhyStatistics(self):
        '''This function return dictinary with phy link statistics
            argument:
                Advance_phy_statistics - Flag for more statistic
            return:
                dictionary -- contain the statistics indications
                    'Phy_link_status'
                    'Phy_link_speed'
        '''
        Phy_link_statistic_dict = {}
        Phy_link_statistic_dict['Phy_link_status'] = self.GetPhyLinkStatus()
        Phy_link_statistic_dict['Phy_link_speed'] = self.GetPhyLinkSpeed()
        return Phy_link_statistic_dict


    #########################################################################################################
    ######################        logger feature ability        #############################################
    #########################################################################################################
    ###  this scope was taken from logger to let us ability to logging the fw in the performance env   ####



    def clear_rx_events_queue(self):
        '''This function will clear the buffer from previous messages  
            input: None
            return: None
        '''
        #print 'clearing rx events queue ...'   
        #print 'wait until you see message: rx events queue empty'   
        driver = self.driver
        receive_aq_desc = AqDescriptor()
        receive_buffer = [0] * 100
            
        while True:
            receive_aq_desc.opcode = 0
            driver.receive_aq_command(receive_aq_desc, receive_buffer)
            #print 'received op code:', hex(receive_aq_desc.opcode)
            if receive_aq_desc.opcode == 0:
                break      
        #print 'rx events queue empty'
        #print 'finished cearing rx events queue'

    def Write_logger_file(self,logger_list,file_name):
        '''This function Write dnllogger log to file 
            argument:
                logger_list- a list containing the lines to write in the file
                file_name- string contains the file name
            return:
                None                    
        '''
        print("Write logger file to: " + file_name)
        try:
            f = open(file_name,'w',0)
            for line in logger_list:
                msg = ''
                if (line is None) or (line == ''):
                    continue
                for iter in line:
                    msg = msg + hex(iter) + ' '
                f.write(msg + '\r\n')
          
            f.flush()
            f.close()
        except Exception as e:
            print("Exception in Write_logger_file " + str(e))

    def GetFWEvent(self,driver,debug=False):
        '''This function should get FW events
            argument:
                driver - driver instance
                debug - flag for aditional debug info #TODO: add debug print
            return: tuple -- 
                        status[0] contains the status of the AQ command
                        status[1] contains the FW event data    
        '''
        #helper = LM_Validation()
        aq_desc = AqDescriptor()    
        #driver = self.driver
        ret_buf = []
        buffer = [0] * 100
        aq_desc.opcode = 0
        status = driver.receive_aq_command(aq_desc, buffer, debug)
        if status == 0 and aq_desc.retval == 0 and aq_desc.opcode == 0xff09:
            for i in range(aq_desc.datalen):
                ret_buf.append(self._to_unsigned(buffer[i]))
            status = (status, ret_buf)
        else:
            status = (status, None)
        return status

    def logger_grabber_loop(self, return_list, driver):
        '''This function is performing logger_grabber_loop
            argument:
                return_list
                driver- driver instance
            return:
                None
        '''
        start_time = curr_time = time.time()
        
        while (True):
            st = self.GetFWEvent(driver)
            if stop_polling_event.is_set() and st[0] == 1020:# error queue empty 
                #print str(time.time()) + "Got queue empty!"
                break
            else:
                return_list.append(st[1])

    def StartDnlLogging(self):
        '''This function Start the Dnl Logging
            argument:
                None
            return:
                None                        
        '''
        stop_polling_event.clear()
        handler = get_handler()
        driver = self.driver
        self.configure_logging_dnl(True)
        print("start dnl logging")
        self.clear_rx_events_queue()
        time.sleep(0.1)
        manager = mp.Manager()
        return_list = manager.list()    
        p = threading.Thread(target=self.logger_grabber_loop, args=(return_list, driver))
        p.daemon = True
        p.start()
        handler.custom_data["DnlLoggingRawDataList"] = return_list
        handler.custom_data["DnlLoggingProccessHandle"] = p


    def StopDnlLogging(self,LoggerFileName,SaveRawDataFlag,manual = 0):
        '''This function StopDnlLogging
            argument:
                LoggerFileName
                SaveRawDataFlag
                manual
            return:
                True always                     
        '''
        driver = self.driver
        print("stop dnl logging")
        self.configure_logging_dnl(False)
        stop_polling_event.set()
        handler = get_handler()
        p = handler.custom_data["DnlLoggingProccessHandle"]
        return_list = handler.custom_data["DnlLoggingRawDataList"]
        p.join()
        if SaveRawDataFlag:
            if not manual:
                LoggerFileName = handler.create_file_name(LoggerFileName, 'txt', handler.get_device_key())
            self.Write_logger_file(return_list, LoggerFileName)
            if not manual:      
                handler.send_file(LoggerFileName)
        return True

    def logger_test(self):
        '''This function is logging  dnl logger during ttl test for debug and development only
            argument: None
            return: None    
        '''
        ttl_timeout = 10
        self.configure_logging_dnl(True)
        self.clear_rx_events_queue()
        time.sleep(0.1)
        log_file = 'raw_data_file.txt'
        q = mp.Queue()
        p = mp.Process(target=self.logger_grabber_loop, args= (q, log_file))
        p.start()
        
        self.RestartAn()
        #start counter
        start_time = curr_time = time.time()
        while (self.GetMacLinkStatus() == True):
            #print 'waiting for link down'
            if ((curr_time - start_time) > ttl_timeout):
                print("link is down for 15s")
                link_down_flag = False
                break
            curr_time = time.time()
        #wait for link up
        while ((curr_time - start_time) < ttl_timeout):
            curr_time = time.time()
            if self.GetMacLinkStatus('REG'):
                curr_time = time.time()
                print('link up')
                break
        
        #calc TTL time
        ttl_time = curr_time - start_time
        print(ttl_time)

        time.sleep(1)
        self.configure_logging_dnl(False)
        msg = q.get()
        while not msg == "queue empty":
            msg = q.get()
        p.join()

        print("end")

    def ttl_test(ttl_timeout,ttl_pass_criteria,link_stable_test_Flag,link_stability_time,RestartAnSrc,iter_num,AmIDut,last_iter):
        '''This function perform ttl test and print the result
            argument:
                ttl_timeout [Sec]
                ttl_pass_criteria
                link_stable_test_Flag - verify that the link is stable after TTL test
                link_stability_time - time for test if link is stable
                RestartAnSrc - restart AN using AQ or by REG
                iter_num - current iteration
                AmIDut  -flag - True when running in DUT, False in LP
                last_iter - flag for last iteration         
            return:
                None
        '''
        print(MainTtl(ttl_timeout,ttl_pass_criteria,link_stable_test_Flag,link_stability_time,RestartAnSrc,iter_num,AmIDut,last_iter))


###############################################################################
######################         Debug Print Section          ###################
###############################################################################

    def DBG_print_Phy_Tuning(self, serdes_sel,debug = False):
        '''This function print phy tuning info. opcode 9 from CVL-DFT-D8.*EX
            arguments:
                serdes_sel - num of serdes
                debug - if true, print phy tuning dict
            return: None
        '''
        Phytuning_dict = {}
        # for key,val in Phy_tuning_params_dict.iteritems():
        for key, val in self.Phy_tuning_params_dict.items():  # Python 3
            # args opcode,serdes_sel,data_in,debug=False
            ret_val = self.DnlCvlDftTest(0x9, serdes_sel, val, debug=False)
            #print key,ret_val
            Phytuning_dict[key] = ret_val
        if debug:
            keylist = Phytuning_dict.keys()  # The keys() method returns a view object
            list(keylist).sort()
            for key in keylist:
               print(key,Phytuning_dict[key])

            # to print dict in Python 3 : print(Phytuning_dict)

            print('#' *80)
            print("RxFFE_pre2  |RxFFE_pre1  |RxFFE_post1 |RxFFE_Bflf  |RxFFE_Bfhf  |RxFFE_Drate ")
            #print '{0:9s} | {1:9s} | {2:10s} | {3:9s} | {4:9s} | {5:9s}'.format(Phytuning_dict["RxFFE_pre2"], Phytuning_dict["RxFFE_pre1"], Phytuning_dict["RxFFE_post1"],Phytuning_dict["RxFFE_Bflf"], Phytuning_dict["RxFFE_Bfhf"], Phytuning_dict["RxFFE_Drate"])
            print('%-12s|%-12s|%-12s|%-12s|%-12s|%-12s'% (Phytuning_dict["RxFFE_pre2"], Phytuning_dict["RxFFE_pre1"], Phytuning_dict["RxFFE_post1"],Phytuning_dict["RxFFE_Bflf"], Phytuning_dict["RxFFE_Bfhf"], Phytuning_dict["RxFFE_Drate"]))
            print()
            print('#' *80)
            print("CTLE_HF |CTLE_LF |CTLE_DC |CTLE_BW |CTLE_gs1|CTLE_gs2")
            print('%-8s|%-8s|%-8s|%-8s|%-8s|%-8s'%(Phytuning_dict["CTLE_HF"], Phytuning_dict["CTLE_LF"], Phytuning_dict["CTLE_DC"],Phytuning_dict["CTLE_BW"], Phytuning_dict["CTLE_gs1"], Phytuning_dict["CTLE_gs2"]))
            print()
            print('#' * 100)
            print("DFE_GAIN |DFE_GAIN2|DFE_2    |DFE_3    |DFE_4    |DFE_5    |DFE_6    |DFE_7    |DFE_8    |DFE_9    |DFE_A    |DFE_B    |DFE_C    |CTLE_gs2 ")
            print('%-9s|%-9s|%-9s|%-9s|%-9s|%-9s|%-9s|%-9s|%-9s|%-9s|%-9s|%-9s|%-9s|%-9s'%(Phytuning_dict["DFE_GAIN"], Phytuning_dict["DFE_GAIN2"], Phytuning_dict["DFE_2"],Phytuning_dict["DFE_3"], Phytuning_dict["DFE_4"], Phytuning_dict["DFE_5"], Phytuning_dict["DFE_6"], Phytuning_dict["DFE_7"], Phytuning_dict["DFE_8"], Phytuning_dict["DFE_9"], Phytuning_dict["DFE_A"], Phytuning_dict["DFE_B"], Phytuning_dict["DFE_C"], Phytuning_dict["CTLE_gs2"]))
            print()
            print('#' * 80)
            print("Eye height_thle |Eye height_thme |Eye height_thue |Eye height_thlo |Eye height_thmo |Eye height_thuo ")
            print('%-16s|%-16s|%-16s|%-16s|%-16s|%-16s'%(Phytuning_dict["Eye height_thle"], Phytuning_dict["Eye height_thme"], Phytuning_dict["Eye height_thue"],Phytuning_dict["Eye height_thlo"], Phytuning_dict["Eye height_thmo"], Phytuning_dict["Eye height_thuo"]))
            print()


        elif PRT_AN_ENABLED and not link_up_flag:
            print()
            print("###########################################  ")
            print("---------------  DUT  --------------------   ")
            print("###########################################  ")
            print()
            print("PRT State Machine PSTO: ", hex(self.PRT_STATE_MACHINE))
            print("PRT State Machine: ", PRT_STATE_MACHINE_AN[get_bits_slice_value(self.PRT_STATE_MACHINE, 0, 7)])


        elif not PRT_AN_ENABLED and not link_up_flag:# force mode and link down
            print()
            print("###########################################  ")
            print("---------------  DUT  --------------------   ")
            print("###########################################  ")
            print()
            print("PRT State Machine PSTO: ", hex(self.PRT_STATE_MACHINE))
            print("PRT State Machine: ", PRT_STATE_MACHINE_FM[get_bits_slice_value(self.PRT_STATE_MACHINE, 0, 7)])

            # print pcs advanced info
            get_pcs_advenced_info = self.GetPcsAdvencedInfo()
            print()
            print()
            print("###########################################  ")
            print("---------------  PCS Info  ---------------   ")
            print("###########################################  ")

            for i in get_pcs_advenced_info:
                print(i)



    ######################################################################################################
    ##########################                  PCIe sections                   ##########################
    ######################################################################################################

    def GetLcbPortLockStatus(self):
        '''This function returns the status of the LOCK bit in the REG GLPCI_LCBADD(offset 0x0009E944 ) PCIe LCB Address Port
            If returned value is 0b, proceed. Else, read data and try again. Section 13.2.2.3.130 
            argument: None
            return: status of the LOCK bit
        '''
        driver = self.driver
        return get_bit_value(driver.read_csr(0x0009E944), 31)

    def _GetValAddrLCB(self, offset):
        '''This function generates an register-address from the register-offset.
            Section 13.2.2.3.130, An ID of a sub-unit in the PCIe unit. Supported values for Bits 20-30 are:
            126: LCB?s internal config space registers --> 0x07e00000
            127: LCB?s internal memory space registers --> 0x07f00000
            argument: None
            return: register-address from the register-offset
        '''
        return offset|0x07e00000

    def ReadLcbRegister(self, offset):
        '''This function returns a LCB register-data by register-offset
            Section 13.2.2.3.130  PCIe LCB Address Port - GLPCI_LCBADD(0x0009E944)
            Section 13.2.2.3.131  PCIe LCB Data Port - GLPCI_LCBDATA (0x0009E940)
            argument: offset (hex)
            return: LCB register-data
        '''
        driver = self.driver
        if self.GetLcbPortLockStatus() == 1:
            print(" lock was on 1 at the beginning")
            driver.write_csr(0x0009E944, self._GetValAddrLCB(offset))# write the LCB reg address in the PCIe LCB Address Port 
            driver.read_csr(0x0009E940) #read the reg data from the PCIe LCB Data Port
        driver.write_csr(0x0009E944, self._GetValAddrLCB(offset))# write the LCB reg address to the PCIe LCB Address Port 
        val = driver.read_csr(0x0009E940)#read the reg data from the PCIe LCB Data Port
        #print hex(val)
        return val

    def WriteLcbRegister(self, offset,data):
        '''This function writes a data to LCB register by register-offset
            Section 13.2.2.3.130  PCIe LCB Address Port - GLPCI_LCBADD(0x0009E944)
            Section 13.2.2.3.131  PCIe LCB Data Port - GLPCI_LCBDATA (0x0009E940)
            argument: 
                offset (hex)
                data - data to write
            return: LCB register-data
        '''
        driver = self.driver
        if self.GetLcbPortLockStatus() == 1:
            print(" lock was on 1 at the beginning")
            driver.write_csr(0x0009E944, self._GetValAddrLCB(offset))# write the LCB reg address in the PCIe LCB Address Port
            driver.read_csr(0x0009E940) #read the reg data from the PCIe LCB Data Port
            time.sleep(0.5)
        driver.write_csr(0x0009E944, self._GetValAddrLCB(offset)) # write the LCB reg address to the PCIe LCB Address Port
        driver.write_csr(0x0009E940, data) #write the reg data to the PCIe LCB Data Port

    def GetPCIECurrentLinkSpeed(self):
        '''This function returns PCIE link speed: 
            argument: None
            return: 'Gen1' / 'Gen2' / 'Gen3' / 'Gen4'
        '''
        #TODO implement this methdo

        link_speed = {
            1: "Gen1",
            2: "Gen2",
            3: "Gen3",
            4: "Gen4"
        }

        return link_speed.get(val,"Wrong")

    def GetPCIECurrentLinkWidth(self):
        '''This function returns PCIE link width: 
            argument: None
            return: 'x1' / 'x2' / 'x4' / 'x8' / 'x16'
        '''
        #TODO implement this method for cpk
        link_width = {
            0: "Reserved",
            1: "x1",
            2: "x2",
            4: "x4",
            8: "x8",
            16: "x16"
        }
        return link_width.get(val, "Wrong")

    def GetDevicePowerState(self):
        '''
            This function returns Device power state: 
            argument: None
            return: "D0" / "Reserved" / "D3hot"
        '''
        reg = self.driver.read_pci(0x44)
        val = get_bits_slice_value(reg[1],0,1)

        power_sate = {0: "D0",
                      2: "Reserved",
                      3: "D3hot"}

        print("Device Power State: ", power_sate.get(val,"Wrong"))

    #########################################################################################################
    #################################         Power        ##################################################
    #########################################################################################################

    def SetD3PowerState(self):
        driver = self.driver
        driver.write_pci(0x44, 0x200b) 
        
    def SetD0PowerState(self):
        driver = self.driver
        driver.write_pci(0x44, 0x2008) 

    def SetD3PowerStateWake(self):
        driver = self.driver
        driver.write_pci(0x44, 0x210b) 

    def SetWakeUp(self):
        driver = self.driver
        ############# PFPM_APM. APME = 1 ###############################
        reg_addr1 = calculate_port_offset(0x000b8080, 0x4, driver.port_number())
        driver.write_csr(reg_addr1, 0x1)
        ############# PFPM_WUFC.MAG = 1 ###############################
        reg_addr2 = calculate_port_offset(0x0009dc00, 0x4, driver.port_number())
        val2 = driver.read_csr(reg_addr2)
        val2 = (val2 & 0x3f) | (1 << 1)
        driver.write_csr(reg_addr2, val2)

        driver.write_pci(0x44, 0x2108)

    def SetOffWakeUp(self):
        driver = self.driver
        ############# PFPM_APM. APME = 1 ###############################
        reg_addr1 = calculate_port_offset(0x000b8080, 0x4, driver.port_number())
        driver.write_csr(reg_addr1, 0x0)
        ############# PFPM_WUFC.MAG = 1 ###############################
        reg_addr2 = calculate_port_offset(0x0009dc00, 0x4, driver.port_number())
        val2 = driver.read_csr(reg_addr2)
        val2 = (val2 & 0x3d)
        driver.write_csr(reg_addr2, val2)

        driver.write_pci(0x44, 0x2008)


    #########################################################################################################
    ######################         Stand alone debug tests      #############################################
    #########################################################################################################

    def DBG_globr_test(self, num_of_iteration,ttl_timeout):
        '''This function performs globr_test for debug
            argument:
                num_of_iteration
                ttl_timeout (sec)
            return:
                None
        '''
        print("Link speed: ",self.GetMacLinkSpeed())
        for i in range(num_of_iteration):       
            print("globr num: ",i)
            self.Reset(1)
            while (self.GetMacLinkStatus("REG")):
                pass
            start_time = curr_time = time.time()
            link_flag = True
            while ((curr_time - start_time) < ttl_timeout):
                curr_time = time.time()       
                if self.GetMacLinkStatus("REG"):
                    curr_time = time.time()
                    link_flag = False
                    print('link up')
                    
                    break
            print("TTL: ",curr_time - start_time)
            time.sleep(5)
            if (link_flag):
                input("Press enter to continue")
                return(0)


    def DBG_restartAN_test_BU(self, num_of_iteration,ttl_timeout):#TODO add link stability check and link drop source
        '''This function performs  restartAN_test for debug
            argument:
                num_of_iteration
                ttl_timeout
            return:
                None
        '''

        ttl_list = []
        avg_ttl = 0
        print("Link speed: ", self.GetMacLinkSpeed())
        for i in range(num_of_iteration):       
            print("Restart AN num: ",i)
            self.RestartAn()
            while (self.GetMacLinkStatus("REG")):
                pass
            start_time = curr_time = time.time()
            link_flag = True
            while ((curr_time - start_time) < ttl_timeout):
                curr_time = time.time()
                if self.GetMacLinkStatus("REG"):
                    curr_time = time.time()
                    link_flag = False
                    print('link up')
                    time.sleep(1)
                    break
            TTL = curr_time - start_time
            ttl_list.append(TTL)
            print("TTL: ",TTL)
            time.sleep(2)
            if (link_flag):
                input("Press enter to continue")
                return(0)
        for i in ttl_list:
             avg_ttl = avg_ttl + i

        print("AVG TTL: ",avg_ttl/len(ttl_list))

    def GetTimeStamp(self):
        '''This function return date and time 
            argument:
                None
            return:
                Stamp(YYMMDD_HHMINSEC)
        '''
        ts = time.localtime()
        stamp = str(ts.tm_year)+str(ts.tm_mon)+str(ts.tm_mday)+'_'+str(ts.tm_hour)+str(ts.tm_min)+str(ts.tm_sec)
        return stamp

    def create_log_name(self,path,iter,ttl):
        '''This function create log name according to path, port number, ttl, number of iteration, date and time.
            argument:
                Path - log location
                Iter - num of iteration
                ttl
            return:
                Fullname of file
        '''
        driver = self.driver
        port = driver.port_number()
        p = path
        fullname = p + str(port) + "_" + str(round(ttl)) + "_" + str(iter) + "_" + self.GetTimeStamp() + ".txt"
        return fullname

    def DBG_restartAN_test(self, num_of_iteration,ttl_timeout,enable_logger = 0,logger_low_limit_ttl = 2):#TODO add link stability check and link drop source
        '''This function print AVG, MAX and MIN ttl (summary of iterations). for debug only
            argument:
                num_of_iteration (int)
                ttl_timeout (int) - max time for TTL
                enable_logger (True/False) - if true enable logger
                logger_low_limit_ttl (int) - if ttl longer then this, save log from logger.
            return:
                None
        '''
        ttl_list = []
        avg_ttl = 0

        print("Link speed: ",self.GetMacLinkSpeed())
        for i in range(num_of_iteration):
            SaveRawDataFlag = False     
            
            if enable_logger:
                print('logger is enabled')
                self.StartDnlLogging()
        
            print("Restart AN num: ",i)
            self.RestartAn()
            while (self.GetMacLinkStatus("REG")):
                pass
            start_time = curr_time = time.time()
            link_flag = True
            while ((curr_time - start_time) < ttl_timeout):       
                curr_time = time.time()
                if self.GetMacLinkStatus("REG"):
                    curr_time = time.time()
                    link_flag = False
                    print('link up')
                    time.sleep(1)
                    break
            ttl = curr_time - start_time
            ttl_list.append(ttl)        
            print("TTL: ",ttl)

            if enable_logger:
                LoggerFileName = self.create_log_name("/home/laduser/LoggerRawData/RawData_IterationNum_", i, ttl)
                if ttl > logger_low_limit_ttl:
                    SaveRawDataFlag = True
                    #print "rad data file saved to: ",LoggerFileName
                print('logger is disable')
                self.StopDnlLogging(LoggerFileName, SaveRawDataFlag, 1)

            time.sleep(3)
            if (link_flag):
                # raw_input("Press enter to continue")
                input("Press enter to continue")   # Python 3
                return(0)

        print()
        print("MIN TTL: ", min(ttl_list))
        print("MAX TTL: ", max(ttl_list))
        print("AVG TTL: ", sum(ttl_list)/len(ttl_list))


    def DBG_traffic_test(self, num_of_iteration,ber_timeout,packet_size):
        '''This function performs traffic test for debug and prints trafic stats.
            The function checks stability during trafic in MAC and PHY
            argument:
                num_of_iteration
                ber_timeout- time for trafic[Sec]
                packet_size - packet_size for trtafic
            return:
                None
        '''
        curr_time = 0
        iter_num = 0
        ErrorStatistics = {}

        for iter_num in range(num_of_iteration):

            self.ClearMACstat()
            CurrentMacLinkStatus_old_value = self.GetMacLinkStatus()
            CurrentPhyLinkStatus_old_value = self.GetPhyLinkStatus()
            #phy_tuning_paraps_dict = GetPhytuningParams()
            new_PTC_Dict = self.GetPTC()
            new_PRC_Dict = self.GetPRC()
            print("Iteration: ",iter_num)
            print("PTC: " ,new_PTC_Dict['TotalPTC'])
            print("PRC: ", new_PRC_Dict['TotalPRC'])

            print("Start TXRX")
            self.EthStartTraffic(packet_size)
            start_time = sampling_time_counter = time.time()
            while (curr_time < ber_timeout):
                curr_time = time.time() - start_time

                CurrentMacLinkStatus = self.GetMacLinkStatus()
                CurrentPhyLinkStatus = self.GetPhyLinkStatus()
                #print "curr time ",curr_time
                if (CurrentMacLinkStatus == False or CurrentPhyLinkStatus == False):
                    print("link drop event")
                #time.sleep(0.005)
            
            print("Stop TXRX")
            self.EthStopTraffic()
            #phy_tuning_paraps_dict = GetPhytuningParams()
            new_PTC_Dict = self.GetPTC()
            new_PRC_Dict = self.GetPRC()
            print("Iteration: ",iter_num)
            print("PTC: " ,new_PTC_Dict['TotalPTC'])
            print("PRC: ", new_PRC_Dict['TotalPRC'])

            ErrorStatistics = self.GetMacErrorsCounters(ErrorStatistics)
            print()
            print("######  Mac Error Statistics  #######")
            print()
            keylist = ErrorStatistics.keys()
            keylist.sort()
            for key in keylist:
                print(key,ErrorStatistics[key])
            print()
            print("######  Mac PTC Statistics  #######")
            print()
            keylist = new_PTC_Dict.keys()
            keylist.sort()
            for key in keylist:
                print(key,new_PTC_Dict[key])
            print()
            print("######  Mac PRC Statistics  #######")
            print()
            keylist = new_PRC_Dict.keys()
            keylist.sort()
            for key in keylist:
                print(key,new_PRC_Dict[key])

    def DBG_globr_test_4_ports(self,num_of_iteration,ttl_timeout):
        '''This function performs  TTL test after performing global reset for 4 ports.
            The function prints the TTL time for each port in case linke is up, otherwise prints error 
            argument:
                num_of_iteration- Number of times to perform the test
                ttl_timeout -max time for TTL [Sec]
            return:
                None
        '''
        driver = self.driver    
        print("Link speed: ", self.GetMacLinkSpeed())
        
        for i in range(num_of_iteration):       
            print("globr iteration: ", i+1)
            self.Reset(1)
            link_flag_port0 = True
            link_flag_port1 = True
            link_flag_port2 = True
            link_flag_port3 = True


            while (self.GetMacLinkStatus("REG")):
                pass
            start_time = curr_time = time.time()
            link_flag = True
            while ((curr_time - start_time) < ttl_timeout):
                curr_time = time.time()

                if link_flag_port0:
                    reg_addr0 = calculate_port_offset(0x001E47A0, 0x4, 0)
                    reg_data0 = driver.read_csr(reg_addr0)
                    LinkStatus0 = get_bit_value(reg_data0,30)       
                    if LinkStatus0:
                        curr_time_port0 = time.time()
                        print('link up on port 0')
                        print("TTL port 0: ",curr_time_port0 - start_time)
                        link_flag_port0 = False

                if link_flag_port1:
                    reg_addr1 = calculate_port_offset(0x001E47A0, 0x4, 1)
                    reg_data1 = driver.read_csr(reg_addr1)
                    LinkStatus1 = get_bit_value(reg_data1,30)
                    if LinkStatus1:
                        curr_time_port1 = time.time()
                        print('link up on port 1')
                        print("TTL port 1: ",curr_time_port1 - start_time)
                        link_flag_port1 = False

                if link_flag_port2:
                    reg_addr2 = calculate_port_offset(0x001E47A0, 0x4, 2)
                    reg_data2 = driver.read_csr(reg_addr2)
                    LinkStatus2 = get_bit_value(reg_data2,30)       
                    if LinkStatus2:
                        curr_time_port2 = time.time()
                        print('link up on port 2')
                        print("TTL port 2: ",curr_time_port2 - start_time)
                        link_flag_port2 = False

                if link_flag_port3:
                    reg_addr3 = calculate_port_offset(0x001E47A0, 0x4, 3)
                    reg_data3 = driver.read_csr(reg_addr3)
                    LinkStatus3 = get_bit_value(reg_data3,30)       
                    if LinkStatus3:
                        curr_time_port3 = time.time()
                        print('link up on port 3')
                        print("TTL port 3: ",curr_time_port3 - start_time)
                        link_flag_port3 = False 

                #if link_flag_port3 == False and link_flag_port2 == False and link_flag_port1 == False and link_flag_port0 == False:
                #   link_flag = False
                #   break   
                    
            time.sleep(2)
            if link_flag_port0:
                input("link is down in port 0, Press enter to exit")
            if link_flag_port1:
                input("link is down in port 1, Press enter to exit")
            if link_flag_port2:
                input("link is down in port 2, Press enter to exit")
            if link_flag_port3:
                input("link is down in port 3, Press enter to exit")
                #return(0)

        #reg_addr = calculate_port_offset(0x001E47A0, 0x4, driver.port_number())
        #reg_data = driver.read_csr(reg_addr)
        #LinkStatus = get_bit_value(reg_data,30)

           ############################### Link Topology Admin commands WIP ##########################################

    def ReadEEPROM(self):
        '''this function reads the eeprom of the cable via I2C
            arguments:None
        '''
        node_handler_dict = dict()
        P = 0
        retval = 0
        while(True):
            if P > 8:#just in case something goes wrong
                break
            topology_list = self.GetLinkTopologyHandle(P)
            status = topology_list[0]
            retval = topology_list[1]
            if retval == 18:
                break
            data = topology_list[2]
            node_handler_dict[P] = data['node_handle']
            P += 1
        #cable_type_to_topology_hanlder_dict = {'sfp' : {0:7,2:8,4:9,6:10,1:11,3:12,5:13,7:14}, 'qsfp' : {0:2,1:3}}
        #handlers_dict = cable_type_to_topology_hanlder_dict.get(cable_type,'cable type unknown')
        eeprom_dict = dict()
        handlers_dict = node_handler_dict
        if handlers_dict == 'cable type unknown':
            print('cable type not supported')
            return
        for port,handle in handlers_dict.iteritems():
            eeprom_dict[port] = list()
            for i in range(16):
                offset = 16*i
                I2C = self.ReadI2C(port,handle,offset)
                data = I2C[2]
                eeprom_dict[port] = eeprom_dict[port]+data
        return eeprom_dict



###############################################################################
######################         debug prints auto complete     #############
###########################################################################

    def PRT_AN_HCD_OUTPUT(self):
        return self.ReadDnlPstore(0x21)

    def PRT_AN_LP_NP(self):
        return self.ReadDnlPstore(0x22)

    def PRT_AN_LP_BP(self):
        return self.ReadDnlPstore(0x23)

    def PRT_AN_LOCAL_NP(self):
        return self.ReadDnlPstore(0x24)

    def PRT_AN_LOCAL_BP(self):
        return self.ReadDnlPstore(0x25)

    def PRT_STATE_MACHINE(self):
        return self.ReadDnlPstore(0x26)

    def PRT_PCS_SELECT(self):
        return self.ReadDnlPstore(0x27)

    def PRT_SET_PMD_LINK_UP_ARG0(self):
        return self.ReadDnlPstore(0x28)

    def PRT_SET_PMD_LINK_UP_ARG1(self):
        return self.ReadDnlPstore(0x29)

    def PRT_SET_PMD_LINK_UP_ARG2(self):
        return self.ReadDnlPstore(0x2A)

    def PRT_SET_PMD_LINK_UP_ARG3(self):
        return self.ReadDnlPstore(0x2B)

    def PRT_SRDS_INT_CMD_ADDR(self):
        return self.ReadDnlPstore(0x2C)

    def PRT_CVL_SERDES_POLARITY(self):
        return self.ReadDnlPstore(0x2D)

    def PRT_FM_SPEED_OUTPUT(self):
        return self.ReadDnlPstore(0x2E)

    def PRT_LAST_CONFIG(self):
        return self.ReadDnlPstore(0x2F)

    def PRT_SET_PMD_LINK_Down_ARG0(self):
        return self.ReadDnlPstore(0x30)

    def PRT_CVL_FLAGS(self):
        return self.ReadDnlPstore(0x31)

    def PRT_SERDES_LOOP(self):
        return self.ReadDnlPstore(0x32)

    def PRT_WATCHDOG_TIMER(self):
        return self.ReadDnlPstore(0x33)

    def PRT_SCRATCH0(self):
        return self.ReadDnlPstore(0x41)

    def PRT_LAST_ERROR_CVL_ALL(self):
        return self.ReadDnlPstore(0x42)

    def PRT_LAST_ERROR_SET_PMD_LINK_UP(self):
        return self.ReadDnlPstore(0x43)

    def PRT_SET_PMD_LINK_UP_ARG0_BYPASS(self):
        return self.ReadDnlPstore(0x44)

    def PRT_SET_PMD_LINK_UP_ARG1_BYPASS(self):
        return self.ReadDnlPstore(0x45)

    def PRT_SET_PMD_LINK_UP_ARG2_BYPASS(self):
        return self.ReadDnlPstore(0x46)

    def PRT_SET_PMD_LINK_UP_ARG3_BYPASS(self):
        return self.ReadDnlPstore(0x47)

    def PRT_SET_LINK_UP_INPUT_ARG0(self):
        return self.ReadDnlPstore(0x06)

    def PRT_SET_LINK_UP_INPUT_ARG1(self):
        return self.ReadDnlPstore(0x07)

    def PRT_SET_LINK_UP_INPUT_ARG2(self):
        return self.ReadDnlPstore(0x08)

    def PRT_SET_LINK_UP_INPUT_ARG3(self):
        return self.ReadDnlPstore(0x09)

    def PRT_TOPO_CAPABILITIES_0(self):
        return self.ReadDnlPstore(0x0A)

    def PRT_TOPO_CAPABILITIES_1(self):
        return self.ReadDnlPstore(0x0B)

    def PRT_TOPO_CAPABILITIES_2(self):
        return self.ReadDnlPstore(0x0C)

    def PRT_TOPO_CAPABILITIES_3(self):
        return self.ReadDnlPstore(0x0D)

    def PRT_MEDIA_CAPABILITIES_0(self):
        return self.ReadDnlPstore(0x0E)

    def PRT_GET_CAPABILITIES_SM(self):
        return self.ReadDnlPstore(0x0F)

    def PRT_SET_LINK_CAPABILITIES_0(self):
        return self.ReadDnlPstore(0x10)

    def PRT_SET_LINK_CAPABILITIES_1(self):
        return self.ReadDnlPstore(0x11)

    def PRT_SET_LINK_CAPABILITIES_2(self):
        return self.ReadDnlPstore(0x12)

    def PRT_SET_LINK_CAPABILITIES_3(self):
        return self.ReadDnlPstore(0x13)

    def PRT_OUTERLINK_INFO(self):
        return self.ReadDnlPstore(0x14)

    def PRT_LINK_STATUS(self):
        return self.ReadDnlPstore(0x15)

    def PRT_LESM_INIT_AN_CONFIG(self):
        return self.ReadDnlPstore(0x16)

    def PRT_LESM_INIT_AN_LP_CONFIG(self):
        return self.ReadDnlPstore(0x17)

    def PRT_LESM_INIT_COUNTERS(self):
        return self.ReadDnlPstore(0x18)

    def PRT_LESM_INIT_FORCED_MODES(self):
        return self.ReadDnlPstore(0x19)

    def PRT_LESM_INIT_FEC_MODES(self):
        return self.ReadDnlPstore(0x1A)

    def PRT_LESM_INIT_FORCED_TIMEOUTS(self):
        pass
        #copy from cvl.py
