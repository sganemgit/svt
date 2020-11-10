
import sys
import time
from core.utilities.BitManipulation import *
from core.utilities.SvtDecorator import *
from core.structs.AqDescriptor import AqDescriptor
from core.structs.CapabilityStructure import CapabilityStructure
from devices.cpk.cpkBase import cpkBase

class cpk(cpkBase):
    '''
        This class contains all the methods to interface with a cvl pf
    '''
    def PrintInfo(self):
        print(self.info())

    def PrintSkuInfo(self):
        sku_info = self.GetSkuInfo()
        for key, val in sku_info.items():
            print('{} : {}'.format(key, val))

    def info(self):
        '''
            This function print cpk info
        '''
        fw_info = self.driver.get_fw_info()
        ret_string = "#"*80 +"\n"
        ret_string += "Device info: \n"
        ret_string += "-"*13 +"\n"
        ret_string += "Device Name : CPK\n"
        ret_string += "Device Number : {}\n".format(self.driver.device_number())
        ret_string += "Port Number : {}\n".format(self.driver.port_number())
        ret_string += "Current MAC link status : {}\n".format(self.GetCurrentLinkStatus())
        ret_string += "Current MAC link Speed : {}\n".format(self.GetCurrentLinkSpeed())
        ret_string += "Current Phy Type : {}\n".format(self.GetCurrentPhyType())
        ret_string += "Current FEC Type : {}\n".format(self.GetCurrentFec())
        ret_string += "Current PCIe link speed : {}\n".format(self.GetCurrentPcieLinkSpeed())
        ret_string += "Current PCIe link Width : {}\n".format(self.GetCurrentPcieLinkWidth())
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

    def GetCurrentMacLinkStatus(self, Location = "AQ"):
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

    def GetCurrentPhyType(self):
        gls = dict()
        gls['port'] = 0 
        gls['cmd_flag'] = 1
        status, data = self.aq.GetLinkStatus(gls)
        if status:
            raise RuntimeError("Error {}: Admin command was not successful".format(self.aq.GetLinkStatusFields.__name__))

        phy_type = data['phy_type']
        
        for offset, phy_type_str in self.data.get_Ability_Phy_Type_dict.items():
            if phy_type & (1<<offset):
                return phy_type_str
    
    def GetCurrentLinkStatus(self):
        gls = dict()
        gls['port'] = 0 
        gls['cmd_flag'] = 1
        status, data = self.aq.GetLinkStatus(gls)
        if status:
            raise RuntimeError("Error {}: Admin command was not successful".format(self.aq.GetLinkStatusFields.__name__))
        link_status = data['link_sts']
        if link_status: 
            return 'UP'
        else:
            return 'DOWN'

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
        for key, val in self.data.get_speed_status_dict.items():
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
        if reset_type in self.data.cpk_reset_type_dict:
            self.driver.device_reset(self.data.cpk_reset_type_dict[reset_type])
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
        
        status, data = self.aq.GetPhyAbilities(get_abils)
        
        if status:
            raise RuntimeError("Error _GetPhyTypeAbilitiesAq: Admin command was not successful")  
        
        module_type_info_dict = dict()    
        current_module_type = data['current_module_type']

        module_type_info_dict['Module_ID'] = current_module_type & 0xFF

        byte1 = (current_module_type >> 8) & 0xFF
        supported_tecknologies_list = list()
        for key, val in self.data.suppoted_module_technologies_dict.items():
            mask = 1 << key
            if byte1 & mask: 
                supported_tecknologies_list.append(val)

        module_type_info_dict['supported_tecknologies'] = supported_tecknologies_list

        module_type_info_dict['GBE_compliance_code'] = (current_module_type >> 16) & 0xFF
        return module_type_info_dict

    def GetCurrentFec(self):
        '''
            This function return the current FEC status
        '''
        gls = {}
        gls['port'] = 0 
        gls['cmd_flag'] = 1
        status, data = self.aq.GetLinkStatus(gls)
        if status:
            raise RuntimeError("Error GetLinkStatus: Admin command failed")

        link_speed = data['current_link_speed']
        for key, val in self.data.get_speed_status_dict.items():
            mask = 1 << key
            if link_speed & mask:
                link_speed = val
                break

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
        
        status, data = self.aq.GetPhyAbilities(get_abils)
        
        if status:
            raise RuntimeError("Error _GetPhyTypeAbilitiesAq: Admin command was not successful")  
        
        if data['module_compliance_enforcement'] & 0x1:
            return 'strict'
        else:
            return 'lenient'

    def GetPhyTypeAbilities(self, rep_mode=0):
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
        
        status, data = self.aq.GetPhyAbilities(get_abils)
        
        if status:
            raise RuntimeError("Error _GetPhyTypeAbilitiesAq: Admin command was not successful")  
            
        phy_type = data['phy_type']
        
        phy_type_list = list()
        
        for i in range(len(self.data.get_Ability_Phy_Type_dict)):
            if ((phy_type >> i) & 0x1):
                phy_type_list.append(self.data.get_Ability_Phy_Type_dict[i])
               
        return phy_type_list
     
    def GetEeeAbilities(self, rep_mode=0):
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
        
        status, data = self.aq.GetPhyAbilities(get_abils) 
        if status:
            raise RuntimeError("Error _GetEEEAbilitiesAq: Admin command was not successful")  
            
        EEE_list = list()
        eee_cap = data['eee_cap']
        for key, val in self.aq.get_Ability_EEE_dict.items():
            mask = 1 << key
            if mask & eee_cap:
                EEE_list.append(val)
        return EEE_list

    #TODO change to DisableFecRequest camelcase compliante
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
        data = self.aq.GetPhyAbilities({'port':0, 'rep_qual_mod':0, 'rep_mode':rep_mode}) ##TODO: check values

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
        status =  self.aq.SetPhyConfig(config)
        
        if status[0]:
            error_msg = 'Error DisableFECRequests: Admin command was not successful, retval {}'.format(status[1])
            raise RuntimeError(error_msg)   

    def DisableLesm(self, rep_mode = 1):
        '''this function diable LESM while keeping all other abillities intact 
            arguments: rep_mode
            return: none 
            level: L2
        '''
        config = {}
        phy_type = 0
        data = self.aq.GetPhyAbilities({'port':0, 'rep_qual_mod':0, 'rep_mode':rep_mode}) ##TODO: check values

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
        status =  self.aq.SetPhyConfig(config)
        if status[0]:
            error_msg = 'Error DisableLESM: Admin command was not successful, retval {}'.format(status[1])
            raise RuntimeError(error_msg)

    def DisableAN37(self, rep_mode = 0):
        config = {}
        phy_type = 0
        data = self.aq.GetPhyAbilities({'port':0, 'rep_qual_mod':0, 'rep_mode':rep_mode})

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
        status =  self.aq.SetPhyConfig(config)
        print(status)
        
        if status[0]:
            error_msg = 'Error DisableLESM: Admin command was not successful, retval {}'.format(status[1])
            raise RuntimeError(error_msg)   

    def SetPhyConfiguration(self, phy_type_list, set_fec, debug=False):
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
        config['pause_abil'] = data['pause_abil']
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

        status, data =  self.aq.SetPhyConfig(config)

        if status:
            raise RuntimeError('Error _SetPhyConfigurationAQ: _SetPhyConfig Admin command was not successful. status: {} retval: {}'.format(status, data))   
 
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

        status = self.aq.SetPhyLoopback(phy_lpbk_args)

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

        status = self.aq.SetPhyLoopback(phy_lpbk_args)

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
        status = self.aq.SetMacLoopback(AQ_args)

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

        status = self.aq.SetPhyLoopback(phy_lpbk_args)
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
        status = self.aq.SetPhyLoopback(phy_lpbk_args)

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
        status = self.aq.SetMacLoopback(AQ_args)

        if status[0]:
            error_msg = "Error DisableMACLoopback: Admin command was not successful, retval{}".format(status[1])
            raise RuntimeError(error_msg)

    def GetCurrentPcieLinkSpeed(self):
        link_status_register = self.driver.read_pci(0xB2)
        link_speed = link_status_register & 0xF
        vector_bit = self.data.link_speed_encoding[link_speed]
        return self.data.supported_Link_speed_vector[vector_bit]

    def GetCurrentPcieLinkWidth(self):
        link_status_register = self.driver.read_pci(0xB2)

        negotiated_link_width = (link_status_register >> 4) & 0x3f
        return self.data.link_width_encoding[negotiated_link_width]

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
        
    def DisableLinkManagement(self):
        '''This function disable firmware's link managment. 
            argument: none
            return: none
        '''

        args = {'port':0, 'index':0, 'cmd_flags':0x10}
        status = self.SetPhyDebug(args)

        if status[0]: 
            error_msg = 'Error LinkManagementDisable: Admin command was not successful, retval {}'.format(status[1])
            raise RuntimeError(error_msg)

    def EnableLinkManagement(self):
        '''This function enable firmware's link managment. 
            argument: none
            return: none
        '''

        args = {'port':0, 'index':0, 'cmd_flags':0}
        status = self.aq.SetPhyDebug(args)

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
        pstores = self.aq.DnlReadPstore(self, pstores_number_to_read,debug)
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

        ret_val = self.aq.DnlReadPstore(context,psto_index,debug=False)
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
        return_val = self.aq.NeighborDeviceRead(0x2,0,1, address)
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

    def ReadMtipRegister(self, offset,address,debug = False):
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
        SbIosfMassageDict = {}
        SbIosfMassageDict['dest'] = 0
        SbIosfMassageDict['source'] = 0
        SbIosfMassageDict['opcode'] = 0
        SbIosfMassageDict['Tag'] = 0
        SbIosfMassageDict['Bar'] = 0
        SbIosfMassageDict['addrlen'] = 0
        SbIosfMassageDict['EH'] = 0
        SbIosfMassageDict['exphdrid'] = 0
        SbIosfMassageDict['EH_2ndDW'] = 0
        SbIosfMassageDict['sai'] = 0
        SbIosfMassageDict['rs'] = 0
        SbIosfMassageDict['fbe'] = 0
        SbIosfMassageDict['Sbe'] = 0
        SbIosfMassageDict['Fid'] = 0
        SbIosfMassageDict['address'] = 0
        SbIosfMassageDict['address_4thDW'] = 0
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
        return_buffer = self.aq.NeighborDeviceRequestAq(0,buffer)



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
        receive_aq_desc = AqDescriptor()
        buffer = [0]*100
            
        while True:
            receive_aq_desc.opcode = 0
            self.driver.receive_aq_command(receive_aq_desc, buffer)
            if receive_aq_desc.opcode == 0:
                break

    def GetFwEvent(self,driver,debug=False):
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
    ##########################                    LCB                           ##########################
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

    #########################################################################################################
    #################################         Power        ##################################################
    #########################################################################################################

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

    def ReadSffEeprom(self):
        '''this function reads the eeprom of the cable via I2C
            arguments:None
        '''
        node_handler_dict = dict()
        P = 0
        retval = 0
        while(True):
            if P > 8:#just in case something goes wrong
                break
            topology_list = self.aq.GetLinkTopologyHandle(P)
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
                I2C = self.aq.ReadI2C(port,handle,offset)
                data = I2C[2]
                eeprom_dict[port] = eeprom_dict[port]+data
        return eeprom_dict

    def ReadDnlPersistentStores(self):
        data = dict()
        data['PRT_AN_HCD_OUTPUT'] = self.ReadDnlPstore(0x21)
        data['PRT_AN_LP_NP'] = self.ReadDnlPstore(0x22)
        data['PRT_AN_LP_BP'] = self.ReadDnlPstore(0x23)
        data['PRT_AN_LOCAL_NP'] = self.ReadDnlPstore(0x24)
        data['PRT_AN_LOCAL_BP'] = self.ReadDnlPstore(0x25)
        data['PRT_STATE_MACHINE'] = self.ReadDnlPstore(0x26)
        data['PRT_PCS_SELECT'] = self.ReadDnlPstore(0x27)
        data['PRT_SET_PMD_LINK_UP_ARG0'] = self.ReadDnlPstore(0x28)
        data['PRT_SET_PMD_LINK_UP_ARG1'] = self.ReadDnlPstore(0x29)
        data['PRT_SET_PMD_LINK_UP_ARG2'] = self.ReadDnlPstore(0x2a)
        data['PRT_SET_PMD_LINK_UP_ARG3'] = self.ReadDnlPstore(0x2b)
        data['PRT_SRDS_INT_CMD_ADDR'] = self.ReadDnlPstore(0x2c)
        data['PRT_CVL_SERDES_POLARITY'] = self.ReadDnlPstore(0x2d)
        data['PRT_FM_SPEED_OUTPUT'] = self.ReadDnlPstore(0x2e)
        data['PRT_LAST_CONFIG'] = self.ReadDnlPstore(0x2f)
        data['PRT_SET_PMD_LINK_Down_ARG0'] = self.ReadDnlPstore(0x30)
        data['PRT_CVL_FLAGS'] = self.ReadDnlPstore(0x31)
        data['PRT_SERDES_LOOP'] = self.ReadDnlPstore(0x32)
        data['PRT_WATCHDOG_TIMER'] = self.ReadDnlPstore(0x33)
        data['PRT_SCRATCH0'] = self.ReadDnlPstore(0x41)
        data['PRT_LAST_ERROR_CVL_ALL'] = self.ReadDnlPstore(0x42)
        data['PRT_LAST_ERROR_SET_PMD_LINK_UP'] = self.ReadDnlPstore(0x43)
        data['PRT_SET_PMD_LINK_UP_ARG0_BYPASS'] = self.ReadDnlPstore(0x44)
        data['PRT_SET_PMD_LINK_UP_ARG1_BYPASS'] = self.ReadDnlPstore(0x45)
        data['PRT_SET_PMD_LINK_UP_ARG2_BYPASS'] = self.ReadDnlPstore(0x46)
        data['PRT_SET_PMD_LINK_UP_ARG3_BYPASS'] = self.ReadDnlPstore(0x47)
        data['PRT_SET_LINK_UP_INPUT_ARG0'] = self.ReadDnlPstore(0x06)
        data['PRT_SET_LINK_UP_INPUT_ARG1'] = self.ReadDnlPstore(0x07)
        data['PRT_SET_LINK_UP_INPUT_ARG2'] = self.ReadDnlPstore(0x08)
        data['PRT_SET_LINK_UP_INPUT_ARG3'] = self.ReadDnlPstore(0x09)
        data['PRT_TOPO_CAPABILITIES_0'] = self.ReadDnlPstore(0x0a)
        data['PRT_TOPO_CAPABILITIES_1'] = self.ReadDnlPstore(0x0b)
        data['PRT_TOPO_CAPABILITIES_2'] = self.ReadDnlPstore(0x0c)
        data['PRT_TOPO_CAPABILITIES_3'] = self.ReadDnlPstore(0x0d)
        data['PRT_MEDIA_CAPABILITIES_0'] = self.ReadDnlPstore(0x0e)
        data['PRT_GET_CAPABILITIES_SM'] = self.ReadDnlPstore(0x0f)
        data['PRT_SET_LINK_CAPABILITIES_0'] = self.ReadDnlPstore(0x10)
        data['PRT_SET_LINK_CAPABILITIES_1'] = self.ReadDnlPstore(0x11)
        data['PRT_SET_LINK_CAPABILITIES_2'] = self.ReadDnlPstore(0x12)
        data['PRT_SET_LINK_CAPABILITIES_3'] = self.ReadDnlPstore(0x13)
        data['PRT_OUTERLINK_INFO'] = self.ReadDnlPstore(0x14)
        data['PRT_LINK_STATUS'] = self.ReadDnlPstore(0x15)
        data['PRT_LESM_INIT_AN_CONFIG'] = self.ReadDnlPstore(0x16)
        data['PRT_LESM_INIT_AN_LP_CONFIG'] = self.ReadDnlPstore(0x17)
        data['PRT_LESM_INIT_COUNTERS'] = self.ReadDnlPstore(0x18)
        data['PRT_LESM_INIT_FORCED_MODES'] = self.ReadDnlPstore(0x19)
        data['PRT_LESM_INIT_FEC_MODES'] = self.ReadDnlPstore(0x1a)
        data['PRT_LESM_INIT_FORCED_TIMEOUTS'] = self.ReadDnlPstore(0x1b)
        return data

    def _GetAllDiscoveredDeviceCapabilities(self, debug=False):
        status, data = self.aq.DiscoverDeviceCapabilities(dict(), debug)
        occured_capability_dict = dict()
        if not status:
            DeviceCapabilities = dict()
            for i in range(0,data['number_of_records']*32,32):
                all_bytes = list()
                all_bytes.extend(data['resource_recognized'][i:i+32])
                if all_bytes[0] in occured_capability_dict.keys():
                    occured_capability_dict[all_bytes[0]] +=1
                    key_name = self.data.device_capabilities_dict[all_bytes[0]] + "_"+ str(occured_capability_dict[all_bytes[0]])
                else: 
                    occured_capability_dict[all_bytes[0]] = 1
                    key_name = self.data.device_capabilities_dict[all_bytes[0]] 
                DeviceCapabilities[key_name] = all_bytes
            return DeviceCapabilities
        else:
             print('Failed to send dicsocer device capabilities Admin Command, status: {} '.format(status))

    def _GetCapabilityStructure(self,capability_name,capability_list):
        cap_struct = CapabilityStructure()
        cap_struct.name = capability_name
        cap_struct.capability = (capability_list[1] << 8) | capability_list[0]
        cap_struct.major_version = capability_list[2]
        cap_struct.minor_version = capability_list[3]
        cap_struct.number = (capability_list[7] << 24) | (capability_list[6] << 16) | (capability_list[5] << 8) | capability_list[4]
        cap_struct.logical_id = (capability_list[11] << 24) | (capability_list[10] << 16) | (capability_list[9] << 8) | capability_list[8]
        cap_struct.physical_id = (capability_list[15] << 24) | (capability_list[14] << 16) | (capability_list[13] << 8) | capability_list[12]
        for index, byte in enumerate(capability_list[16:23]):
            cap_struct.data1 = (byte << (index*8)) | cap_struct.data1
        for index, byte in enumerate(capability_list[24:31]):
            cap_struct.data1 = (byte << (index*8)) | cap_struct.data1
        return cap_struct

    def GetDiscoveredDeviceCapability(self, capability=None):
        all_discovered_dev_Caps = self._GetAllDiscoveredDeviceCapabilities()
        cap_structs_list = list()
        if capability:
            duplicate_capabilities = {k:v for k,v in all_discovered_dev_Caps.items() if capability in k}
            all_discovered_dev_Caps = duplicate_capabilities
        for capability_name,capability_list in all_discovered_dev_Caps.items():
            cap_structs_list.append(self._GetCapabilityStructure(capability_name,capability_list))
        return cap_structs_list

    def GetSkuInfo(self):
        sku_cap = self.GetDiscoveredDeviceCapability('SKU')[0]
        sku_info = dict()
        ports = sku_cap.number & 0x3
        if ports == 0x0: 
            sku_info['enabled_ports'] = '8'
        elif ports == 0x1:
            sku_info['enabled_ports'] = '4'
        elif ports == 0x2:
            sku_info['enabled_ports'] = '2'
        elif ports == 0x3:
            sku_info['enabled_ports'] = '1'

        bandwidth = (sku_cap.number >> 2) & 0x3

        if bandwidth == 0x0:
            sku_info['bandwidth'] = '200G'
        elif bandwidth == 0x1: 
            sku_info['bandwidth'] = '100G'
        elif bandwidth == 0x2:
            sku_info['bandwidth'] = '50G'
        elif bandwidth == 0x3:
            sku_info['bandwidth'] = '25G'
        sku_info['PE Engine'] = 'disabled' if sku_cap.number & 0x10 else 'enabled'
        sku_info['Switch Mode'] = 'enabled' if sku_cap.number & 0x20 else 'disabled'
        sku_info['CSR Protcetion'] = 'enabled' if sku_cap.number & 0x40 else 'disabled'
        sku_info['Block BME to FW'] = 'not_writable_by_fw' if sku_cap.number & 0x200 else 'writable_by_fw'
        sku_info['SOC Type'] = 'SNR' if sku_cap.number & 0x400 else 'ICX-D'
        sku_info['BTS Mode'] = 'non_bts' if sku_cap.number & 0x800 else 'bts'
        return sku_info

    def GetPhyAbilitiesFields(self):
        config = dict()
        config['port'] = 0 #not relevant for CVL according to CVL Spec
        config['rep_qual_mod'] = 0
        config['rep_mode'] = 1 
        status, data = self.aq.GetPhyAbilities(config)
        if status:
            raise RuntimeError("Error _GetPhyTypeAbilitiesAq: Admin command failed")
        return data  

    def EnableLenientMode(self):
        self.SetLenientMode(True)

    def DisableLenientMode(self):
        self.SetLenientMode(False)

    def SetLenientMode(self, Enable):

        status, data1 = self.aq.GetLinkStatus({'port':0, 'cmd_flag':0})
        if status:
            raise RuntimeError("Get Link Sattus failed")
        status, data = self.aq.GetPhyAbilities({'port':0, 'rep_qual_mod':0, 'rep_mode':0}) 
        if status:
            raise RuntimeError("GetPhyAbilities failed")

        config = dict()
        config['port'] = 0 
        config['phy_type_0'] = data1['phy_type_0'] 
        config['phy_type_1'] = data1['phy_type_1']
        config['phy_type_2'] = data1['phy_type_2'] 
        config['phy_type_3'] = data1['phy_type_3'] 
        config['pause_abil'] = data['pause_abil']
        config['low_pwr_abil'] = data['low_pwr_abil']
        config['en_link'] = 1
        config['en_auto_update'] = 1
        config['lesm_en'] = data['lesm_en']
        config['auto_fec_en'] = data['auto_fec_en']
        config['low_pwr_ctrl'] = data['low_pwr_ctrl']
        config['eee_cap_en'] = data['eee_cap']
        config['eeer'] = data['eeer']        
        config['fec_firecode_10g_abil'] = data['fec_firecode_10g_abil'] #data['fec_firecode_10g_abil'] 
        config['fec_firecode_10g_req'] = data['fec_firecode_10g_req'] 
        config['fec_rs528_req'] = data['fec_rs528_req'] 
        config['fec_firecode_25g_req'] = data['fec_firecode_25g_req'] 
        config['fec_rs544_req'] = data['fec_rs544_req'] 
        config['fec_rs528_abil'] = data['fec_rs528_abil'] 
        config['fec_firecode_25g_abil'] = data['fec_firecode_25g_abil'] 
        config['module_complinance_enforcement'] = 0 if Enable else 1 

        status, data = self.aq.SetPhyConfig(config)
        if status:
            error_msg = 'Error _SetPhyConfigurationAQ: _SetPhyConfig Admin command was not successful, retval {}'.format(data)
            raise RuntimeError(error_msg)

    def ReadNvmModuleByTypeId(self, module_type_id):
        '''
            flow: 1) request resource onwnership over the nvm (must release within 3 sec)
                  2) read TLV based on moudle ID 
                  3) release resource onwnership
        '''
        nvm_read_config = dict()
        nvm_read_config['offset'] = 0
        #nvm_read_config['module_typeID'] = self.data.nvm_module_type_id_dict[module_type_id]
        nvm_read_config['module_typeID'] = module_type_id
        nvm_read_config['length'] = 0xffff
        nvm_read_config['last_command_bit'] = 1

        request_resource_config = dict()
        request_resource_config['resource_id'] = 0x1 #NVM
        request_resource_config['access_type'] = 1 #read 
        status1, data1 = self.aq.RequestResourceOwnership(request_resource_config)
        if status1: 
            raise RuntimeError('RequestResourceOwnership AQ faild status: {} revalue: {}'.format(status1, data1))

        #we have successfully aquired ownership over the nvm. Default timeout for this operation is 3000ms. need to be quick
        try: 
            status, data = self.aq.NvmRead(nvm_read_config)
            if status: 
                raise RuntimeError("NVM read Admin command failed. status: {} retval: {}".format(status, data))
        finally:
            stuts1, data1 = self.aq.ReleaseResourceOwnership(request_resource_config)
            if stuts1: 
                raise RuntimeError('Release Resource Ownership Amdin command fails stuts1: {} retval: {}'.format(stuts1, data1))
        return data

    def SetDefaultOverrideMask(self, config):

        port = config['port']
        phy_types = config['phy_types'] # int[16 bytes] 
        lenient = config.get('lenient', 0x0)
        epct_ability_enable = config.get('epct_ability_enable', 0x0)
        port_disable = config.get('port_disable', 0x0)     
        override_enable = config.get('override_enable', 0x1)
        disable_automatic_link = config.get('disable_automatic_link', 0x0)
        eee_enable = config.get('eee_enable', 0x0) 
        pause_ability = config.get('pause_ability', 0x3) 
        lesm_enable = config.get('lesm_enable', 0x0)
        auto_fec_enable = config.get('auto_fec_enable', 0x0)
        fec_options = config.get('fec_options', 0x0)
        override_phy_types = config.get('override_phy_types', 0x0)
        override_disable_automatic_link = config.get('override_disable_automatic_link', 0x0)
        override_eee = config.get('override_eee', 0x0)
        override_pause = config.get('override_pause', 0x0)
        override_lesm_enable = config.get('override_lesm_enable', 0x0)
        override_fec = config.get('override_fec', 0x0)

        byte_1 = ((eee_enable & 0x1) << 5) | ((disable_automatic_link & 0x1) << 4) | ((override_enable & 0x1) << 3) | ((port_disable & 0x1) <<2) | ((epct_ability_enable & 0x1) <<1) | (lenient & 0x1)
        byte_2 = ((auto_fec_enable & 0x1) <<7) | ((lesm_enable & 0x1) << 6) | (pause_ability & 0x3)
        byte_3 = fec_options & 0xff
        byte_4 = ((override_fec & 0x1) << 5) | ((override_lesm_enable & 0x1) << 4) | ((override_pause & 0x1) << 3) | ((override_eee & 0x1) <<2) | ((override_disable_automatic_link & 0x1) <<1) | (override_phy_types & 0x1)

        data = self.ReadNvmModuleByTypeId(0x134)
        
        word_list = convert_byte_list_to_16bitword_list(data['nvm_module'])
        # a word is 16 bit long

        word_list[1+10*port] = (byte_2 & 0xff) <<8 | (byte_1 & 0xff)
        word_list[2+10*port] = (byte_4 & 0xff) <<8 | (byte_3 & 0xff)
        word_list[3+10*port] = int(phy_types & 0xffff)
        word_list[4+10*port] = int((phy_types >> 16) & 0xffff)
        word_list[5+10*port] = int((phy_types >> 32) &  0xffff)
        word_list[6+10*port] = int((phy_types >> 48) & 0xffff)
        word_list[7+10*port] = int((phy_types >> 64) &  0xffff)
        word_list[8+10*port] = int((phy_types >> 80) & 0xffff)
        word_list[9+10*port] = int((phy_types >> 96) &  0xffff)
        word_list[10+10*port] = int((phy_types >> 112) & 0xffff)

        new_pfa_data = conver_16bitword_list_to_byte_list(word_list)

        request_resource_config = dict()
        request_resource_config['resource_id'] = 0x1 #NVM
        request_resource_config['access_type'] = 2 #write 
        status1, data1 = self.aq.RequestResourceOwnership(request_resource_config)
        if status1: 
            raise RuntimeError('RequestResourceOwnership AQ faild status: {} retval: {}'.format(status1, data1))

        #we have successfully aquired ownership over the nvm. Default timeout for this operation is 180000ms. need to be quick
        try: 
            # nvm_erase_config = dict()
            # nvm_erase_config['module_typeID'] = data['module_typeID']
            # nvm_erase_config['last_command_bit'] = 1
            # status, data = self.aq.NvmErase(nvm_erase_config)
            # if status:
            #     raise RuntimeError("NVM erase has failed. status {} retval: {}".format(status, data))
            #writing to NVM
            nvm_write_config = dict()
            #nvm_write_config['module_typeID'] = self.data.nvm_module_type_id_dict[module_type_id]
            nvm_write_config['module_typeID'] = data['module_typeID']
            nvm_write_config['length'] = data['length']
            nvm_write_config['last_command_bit'] = 0
            nvm_write_config['data'] = new_pfa_data
            status, data = self.aq.NvmWrite(nvm_write_config)
            if status:
                raise RuntimeError("NVM Write Admin command failed. status: {} retval: {}".format(status, data))
            status, data = self.aq.NvmWriteActivate(dict())
            if status:
                raise RuntimeError("NVM Write Activate Admin Command failed. status: {} retval: {}".foramt(status, data))
            time.sleep(1)
        finally:
            stuts1, data1 = self.aq.ReleaseResourceOwnership(request_resource_config)
            if stuts1:
                raise RuntimeError('Release Resource Ownership Amdin command fails stuts1: {} retval: {}'.format(stuts1, data1))
