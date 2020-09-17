
#--------------------------------------------
# @author Shady Ganem <shady.ganem@intel.com>
#--------------------------------------------

import sys
import threading

from core.structs.AqDescriptor import AqDescriptor
from core.utilities.BitManipulation import *
from devices.cvl.temp import *
import time

from devices.cvl.cvlDefines import cvlDefines, cvl_structs, AqOpCodes


class cvl(cvlDefines):
    'This class contains all the methods to interface with a cvl pf'
    
    def info(self, advance = False, Location = "AQ"):
        '''This function print cvl info
            argument:
                Advance - True/False. if true print more info.
                Location - AQ/REG
            return:
                None
        '''
        port = self.driver.port_number()
        device_number = self.driver.device_number()
        print("######################################")
        print("CVL port {}".format(port))
        print("CVL device {}".format(device_number))
        print("######################################")
        link_status_dict = self.GetLinkStatusAfterParsing()
        link_up_flag = 1 if link_status_dict['MacLinkStatus'] == 'Up' else 0
        
        print("Phy Types abilities: ")
        for phy in self.GetPhyTypeAbilities(rep_mode = 0):
            print('        {}'.format(phy))
        print("Phy Type: ", link_status_dict['PhyType'])
        print("FEC Type: ", self.GetCurrentFECStatus())
        print("Mac Link Status: ",link_status_dict['MacLinkStatus'])
        if link_up_flag:
            print("Mac Link Speed: ",link_status_dict['MacLinkSpeed'])
            print("Phy Link Status: ",'UP' if self.GetPhyLinkStatus()==1 else 'Down') #GetPhyLinkStatus() # ONPI)
            print("Phy Link Speed: ",self.GetPhyLinkSpeed()) 
            #print "FEC abilities: ",GetFecAbilities(rep_mode = 0)
            print("Enabled FEC: ", link_status_dict['EnabeldFEC'])
            print("EEE abilities: ", self.GetEEEAbilities(rep_mode = 0))#GetPhyAbility)
            print() 

        print("Current PCIe link speed, ",self.GetPCIECurrentLinkSpeed())
        print("Current PCIe link Width, ",self.GetPCIECurrentLinkWidth())

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
        """
        This function clears CVL register
        :param register_name: Defined in reg_dict in cvlDefines
        """
        for addr in self.reg_dict[register_name]:
            reg_addr = calculate_port_offset(addr, mul, self.driver.port_number())
            self.driver.write_csr(reg_addr, 0xffffffff)

    def ClearMACstat(self):
        '''This function clears following MAC statistics registers.
            clear: PTC, PRC, CRCERRS, ILLERRC, ERRBC, MLFC, MRFC, RLEC, RUC, RFC, ROC, RJC, MSPDC, LDPC.
            (12.2.2.19)
        '''
        for reg in self.reg_dict:
            self.Clear_register(register_name=reg, mul=0x4) if reg == "LDPC" else self.Clear_register(register_name=reg)


###############################################################################
#                       Traffic Section                                       #
###############################################################################

    def EthStartTraffic(self, packet_size = 512):
        '''This function starts Tx and Rx.
            argument: packet size - Default is 512
            return: None
        '''
        driver = self.driver
        driver.start_rx(packet_size = packet_size)
        time.sleep(2)
        driver.start_tx(packet_size = packet_size)

    def EthStartRx(self, packet_size = 512):
        '''This function starts Tx and Rx.
            argument: packet size - Default is 512
            return: None
        '''
        driver = self.driver
        driver.start_rx(packet_size = packet_size)
    
    def EthStartTx(self, packet_size = 512):
        '''This function starts Tx and Rx.
            argument: packet size - Default is 512
            return: None
        '''
        driver = self.driver
        driver.start_tx(packet_size = packet_size)

    def EthStopRx(self):
        '''This function stops Tx and Rx.
            argument: None
            return: None
        '''
        driver = self.driver
        driver.stop_rx()
    
    def EthStopTx(self):
        '''This function stops Tx and Rx.
            argument: None
            return: None
        '''
        driver = self.driver
        driver.stop_tx()

    def EthStopTraffic(self):
        '''This function stops Tx and Rx.
            argument: None
            return: None
        '''
        driver = self.driver
        driver.stop_tx()
        time.sleep(3)
        driver.stop_rx()

    def GetCurrentThroughput(self, packet_size=512):
        '''This function returns current Throughput
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
        '''This function returns the link status.
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
        '''This function returns the link status (13.2.2.4.78).
           PRTMAC_LINKSTA 0x001E47A0
               argument: None
               return: True/false
        '''
        # driver = self.driver
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
        result = self.GetLinkStatus(gls)

        if not result[0]:  # if Admin command was successful - False
            data = result[1]
        else:
            raise RuntimeError("Error _GetMacLinkStatusAQ: Admin command was not successful")

        status = data['link_sts']
        return status

    def GetLinkStatusFields(self):
        gls = dict()
        gls['port'] = 0 
        gls['cmd_flag'] = 1
        result = self.GetLinkStatus(gls)
        if not result[0]:
            data = result[1]
        else:
            raise RuntimeError("Error {}: Admin command was not successful".format(self.GetLinkStatusFields.__name__))
        print()
        print(data)
        print()

        print("link status {}".format(data['link_sts']))
        print("media available {}".format(data['media_avail']))

        print("PHY Type list  {}" .format(data['phy_type_list']))
        print()


    def GetCurrentLinkSpeed(self, Location = "AQ"):
        '''This function return Mac Link Speed.
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
        status, data = self.GetLinkStatus(gls)

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
        '''This function performs restart autoneg
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
        '''This function performs restart autoneg
            This function is for debug only because Restart AN by REG is not implimented
        '''
        raise RuntimeError("Restart AN by REG is not implimented")

    def _RestartAnAq(self):
        '''This function performs restart autoneg by AQ
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
        '''This function performs resets
            argument: reset_type (string) - "globr" , "pfr" , "corer", "empr", "flr", "pcir", "bmer", "vfr", "vflr"
            return: None
        '''
        # driver = self.driver
        if reset_type in self.reset_type_dict:
            self.driver.device_reset(self.reset_type_dict[reset_type])
        # if reset_type ==  "globr":
        #     driver.device_reset("GLOBAL")
        # elif reset_type ==  "pfr" :
        #     driver.device_reset("PF")
        # elif reset_type == "corer" :
        #     driver.device_reset("CORE")
        # elif reset_type == "empr":
        #     driver.device_reset("EMP")
        # elif reset_type == "flr":
        #     driver.device_reset("FL")
        # elif reset_type == "pcir":
        #     driver.device_reset("PCI")
        # elif reset_type == "bmer":
        #     driver.device_reset("BME")
        # elif reset_type ==  "vfr":
        #     driver.device_reset("VF_SW")
        # elif reset_type ==   "vflr":
        #     driver.device_reset("VFLR")
        else:
            print("could not identify reset type")

    def Reset2(self,Reset, Location = "REG"):
        '''This function performs reset to CVL
            argument:
                Location = "REG" / "AQ"
                Reset = 0 - for core reset
                        1 - for global reset
                        2 - for EMP reset
        '''
        if Location == "REG":
            self._ResetReg(Reset)
        elif Location == "AQ":
            self._ResetAq()
            # self._ResetAq(Reset)
        else:
            raise RuntimeError("Err Reset: Error Location, please insert location REG/AQ")

    def _ResetReg(self, Reset):
        ''' RESET GLGEN_RTRIG (0x000B8190)
            argument:
                Reset = 0 - for core reset
                        1 - for global reset
                        2 - for EMP reset
        '''
        driver = self.driver
        reg_addr = 0x00B8190
        reg_value = driver.read_csr(reg_addr)   
        reg_value = reg_value | (1 << Reset)
        driver.write_csr(reg_addr, reg_value)

    def _ResetAq(self):
        '''This function performs reset to CVL by admin command. 
            for debug only because reset by AQ is not implimented.
        '''
        raise RuntimeError("Reset by AQ is not implimented")

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
        '''This function return Phy type
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
        '''This function return Phy type.
            for debug only because GetPhyType by REG is not implimented.
        '''
        raise RuntimeError("Get Phy type by Reg is not implemented")

    def _GetPhyTypeAq(self):
        '''This function return Phy type using Get link status AQ.
            return: Phy type in str
        '''
        gls = {}
        gls['port'] = 0 #not relevant for CVL according to CVL Spec
        gls['cmd_flag'] = 1
        result = self.GetLinkStatus(gls)
        if not result[0]: # if Admin command was successful - False
            data = result[1]
        else:
            raise RuntimeError("Error _GetPhyTypeAq: Admin command was not successful")  
        phy_type = (data['phy_type_3'] << 96 ) | (data['phy_type_2'] << 64 ) | (data['phy_type_1'] << 32 ) | data['phy_type_0']
        if self.Get_Phy_Type_Status_dict:
            for i in range(len(self.Get_Phy_Type_Status_dict)):
                if ((phy_type >> i) & 0x1):
                    return self.Get_Phy_Type_Status_dict[i]

        else:
            raise RuntimeError("Error _GetPhyTypeAq: Get_Phy_Type_Status_dict is not defined")

    def GetCurrentFECStatus(self, Location = "AQ"):
        '''This function return the current FEC status
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
        '''This function returns the FEC status using register.
            for debug only because GetCurrentFecStatus by REG is not implimented.
            return: None
        '''
        raise RuntimeError("Get current FEC status by Reg is not implimented")

    def _GetCurrentFECStatusAq(self):
        '''This function returns the FEC status using Get link status AQ.
            return: FEC type by str
        '''
        link_speed = self.GetPhyLinkSpeed()

        if self.GetPhyType() == 'N/A':
            return 'N/A'
        gls = {}
        gls['port'] = 0 #not relevant for CVL according to CVL Spec
        gls['cmd_flag'] = 1
        result = self.GetLinkStatus(gls)

        if not result[0]: # if Admin command was successful - False
            data = result[1]
        else:
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

    def GetPhyTypeAbilities(self, rep_mode = 0, Location = "AQ"):
        '''This function return list of phy types
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
        '''This function return list of phy types
            for debug only because reset by AQ is not implimented.
        '''
        raise RuntimeError("Get Phy Type Abilities by Reg is not implimented")      

    def _GetPhyTypeAbilitiesAq(self, rep_mode):
        ''' Description: Get various PHY type abilities supported on the port.
            input:
                rep_mode : int[2 bits] -- 00b reports capabilities without media, 01b reports capabilities including media, 10b reports latest SW configuration request
            return:
                phy_type_list - contain phy type abilities by str
        '''
        
        get_abils = {}
        get_abils['port'] = 0 #not relevant for CVL according to CVL Spec
        get_abils['rep_qual_mod'] = 0
        get_abils['rep_mode'] = rep_mode
        
        result = self.GetPhyAbilities(get_abils)
        
        if not result[0]: # if Admin command was successful - False
            data = result[1]
        else:
            raise RuntimeError("Error _GetPhyTypeAbilitiesAq: Admin command was not successful")  
            
        phy_type = data['phy_type']
        
        phy_type_list = list()
        
        for i in range(len(self.get_Ability_Phy_Type_dict)):
            if ((phy_type >> i) & 0x1):
                phy_type_list.append(self.get_Ability_Phy_Type_dict[i])
               
        return phy_type_list

    def GetEEEAbilities(self, rep_mode, Location = "AQ"):
        '''This function return list of EEE abilities
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
        '''This function return list of EEE abilities
            for debug only because FecAbilities by REG is not implimented.
        '''
        raise RuntimeError("Get EEE Abilities by Reg is not implimented")   
     
    def _GetEEEAbilitiesAq(self, rep_mode):
        ''' Description: Get EEE abilities supported on the port.
            input:
                rep_mode : int[2 bits] -- 00b reports capabilities without media, 01b reports capabilities including media, 10b reports latest SW configuration request
            return:
                EEE_list - contain EEE abilities by str
        '''
        
        get_abils = {}
        get_abils['port'] = 0 #not relevant for CVL according to CVL Spec
        get_abils['rep_qual_mod'] = 0
        get_abils['rep_mode'] = rep_mode
        
        result = self.GetPhyAbilities(get_abils) 
        if not result[0]: # if Admin command was successful - False
            data = result[1]
        else:
            raise RuntimeError("Error _GetEEEAbilitiesAq: Admin command was not successful")  
            
        #print hex(data['eee_cap'])
            
        EEE_list = []
        for i in range(len(self.get_Ability_EEE_dict)):
            if ((data['eee_cap'] >> i) & 0x1):
                EEE_list.append(self.get_Ability_EEE_dict[i])
        
        #print EEE_list
        return EEE_list

    def GetFecAbilities(self,rep_mode = 1, Location = "AQ"):
        '''This function return list of FEC abilities
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
        '''This function return list of FEC abilities
            for debug only because FecAbilities by REG is not implimented.
        '''
        raise RuntimeError("Get FEC Abilities by Reg is not implimented")

    def _GetFecAbilitiesAq(self,rep_mode):
        ''' Description: Get available FEC options for the link
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
        '''This function return Phy Link Speed.
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
        '''This function return Phy Link Speed.
            return: 
                link speed by str - '10M' / '100M' / '1G' / '2.5G' / '5G' / '10G' / '20G' / '25G' / '40G' / '50G' / '100G'
        '''
        driver = self.driver
        reg_addr = calculate_port_offset(0x03001030, 0x100, driver.port_number())
        value = self.ReadEthwRegister(reg_addr)
        return self.Phy_link_speed_dict[int(value,16)]
        
    def _GetPhyLinkSpeedAq(self):
        '''This function return Phy Link Speed using Get link status AQ.
            return:
                link speed by str - '10M' / '100M' / '1G' / '2.5G' / '5G' / '10G' / '20G' / '25G' / '40G' / '50G' / '100G' / '200G' 
        '''
        raise RuntimeError("_GetPhyLinkSpeedAq need to be done")

    def GetPhyLinkStatus(self, Location = "AQ"):
        '''This function return Phy Link status.
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
        '''This function return PCS Link Status .
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

    def DisableLldp(self, shutdown=0 , persistent=0, debug=0):
        driver = self.driver
        aq_desc = AqDescriptor()
        data_len = 0x0
        aq_desc.opcode = 0x0a05 
        aq_desc.datalen = data_len
        buffer = [0] * data_len
        aq_desc.param0 = (persistent << 1 | shutdown) 
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.flags = 0x0

        status = driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Set Phy Debug Admin Command, status: ', status, ', FW ret value: ', aq_desc.retval)
        err_flag = (aq_desc.flags & 0x4) >> 2 #isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)

    def EnableLldp(self,persistent = 0, debug = 0):
        driver = self.driver
        #helper = LM_Validation()
        aq_desc = AqDescriptor()
       # helper._debug('SetPhyDebug Admin Command')
        data_len = 0x0
        aq_desc.opcode = 0x0a06 
        aq_desc.datalen = data_len
        buffer = [0] * data_len
        aq_desc.param0 = (persistent << 1 | 1) 
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.flags = 0x0

        status = driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Set Phy Debug Admin Command, status: ', status, ', FW ret value: ', aq_desc.retval)
        err_flag = (aq_desc.flags & 0x4) >> 2 #isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)

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
        data = self.GetPhyAbilities({'port':0, 'rep_qual_mod':0, 'rep_mode':rep_mode}) 

        if data[0]:
            error_msg = 'Error _SetPhyConfigurationAQ: GetPhyAbilities Admin command was not successful, retval {}'.format(data[1])
            raise RuntimeError(error_msg)

        abilities = data[1]
        
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
            config['fec_firecode_10g_abil'] = 0 #abilities['fec_firecode_10g_abil'] 
            config['fec_firecode_10g_req'] = 0 
            config['fec_rs528_req'] = 0 
            config['fec_firecode_25g_req'] = 0 
            config['fec_rs544_req'] = 0 
            config['fec_rs528_abil'] = 0 #abilities['fec_rs528_abil']
            config['fec_firecode_25g_abil'] = 0 #abilities['fec_firecode_25g_abil']
            
        elif set_fec == '10G_KR_FEC':
            config['fec_firecode_10g_abil'] = abilities['fec_firecode_10g_abil'] 
            config['fec_firecode_10g_req'] = 1
            config['fec_rs528_req'] = 0 
            config['fec_firecode_25g_req'] = 0 
            config['fec_rs544_req'] = 0 
            config['fec_rs528_abil'] = abilities['fec_rs528_abil']
            config['fec_firecode_25g_abil'] = abilities['fec_firecode_25g_abil']
        
        elif set_fec == '25G_KR_FEC':
            config['fec_firecode_10g_abil'] = abilities['fec_firecode_10g_abil'] 
            config['fec_firecode_10g_req'] = 0 
            config['fec_rs528_req'] = 0 
            config['fec_firecode_25g_req'] = 1 
            config['fec_rs544_req'] = 0 
            config['fec_rs528_abil'] = 0
            config['fec_firecode_25g_abil'] = 0
            
        elif set_fec == '25G_RS_528_FEC':
            config['fec_firecode_10g_abil'] = abilities['fec_firecode_10g_abil'] 
            config['fec_firecode_10g_req'] = 0 
            config['fec_rs528_req'] = 1
            config['fec_firecode_25g_req'] = 0 
            config['fec_rs544_req'] = 0
            config['fec_rs528_abil'] = abilities['fec_rs528_abil']
            config['fec_firecode_25g_abil'] = abilities['fec_firecode_25g_abil']

        elif set_fec == '25G_RS_544_FEC':
            config['fec_firecode_10g_abil'] = abilities['fec_firecode_10g_abil'] 
            config['fec_firecode_10g_req'] = 0 
            config['fec_rs528_req'] = 0 
            config['fec_firecode_25g_req'] = 0 
            config['fec_rs544_req'] = 1
            config['fec_rs528_abil'] = abilities['fec_rs528_abil']
            config['fec_firecode_25g_abil'] = abilities['fec_firecode_25g_abil']
            
        else:
            error_msg = 'Error _SetPhyConfigurationAQ: fec input is not valid. insert NO_FEC/10G_KR_FEC/25G_KR_FEC/25G_RS_528_FEC/25G_RS_544_FEC'
            raise RuntimeError(error_msg)

        status = ()
        status =  self.SetPhyConfig(config)

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
            link_status = self.GetLinkStatus({'port':0, 'cmd_flag':1})
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
     
    def DebugReadDnlPstores(context, pstores_number_to_read,debug=False):
        '''read PSTO for debug.
            arguments: 
                context - context number
                pstores_number_to_read - PSTO number to read
            return:
                print all pstors
        '''
        pstores = _DnlReadPstore(context, pstores_number_to_read,debug)
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
     
    def AQ_Debug (self,flags,opcode,param0,param1):
        '''This function is for debug only.
            arguments:
                flags - 2 bytes (hex)
                opcode - 2 bytes (hex)
                param0 - 4 bytes (hex)
                param1 - 4 bytes (hex)
            return:
                print all admin command fields:
                    retval, flags, opcode, param0, param1, cookie_high, cookie_low, addr_high, addr_low, buffer
        '''
        driver = self.driver        

        data_len = 0x1000        
        aq_desc = AqDescriptor()
        aq_desc.flags = flags
        aq_desc.opcode = opcode
        aq_desc.param1 = param0
        aq_desc.flags = param1
        aq_desc.datalen = data_len
        buffer = [0] * data_len
        #buf = [0,1,2,3,4,5]
        #driver.send_aq_command(aq_desc, buf)
        #val1 = buf[0]
        #val2 = buf[1]

        driver.send_aq_command(aq_desc,buffer)

        print('retval: ', hex(aq_desc.retval))
        print('flags: ', hex(aq_desc.flags))
        print('opcode: ', hex(aq_desc.opcode))
        print('param0: ', hex(aq_desc.param0))
        print('param1: ', hex(aq_desc.param1))
        print('cookie_high: ', hex(aq_desc.cookie_high))
        print('cookie_low: ', hex(aq_desc.cookie_low))
        print('addr_high: ', hex(aq_desc.addr_high))
        print('addr_low: ', hex(aq_desc.addr_low))
        print('buffer: ',buffer)


    ######################################################################################################
    ###############################           DNL section             ####################################
    ######################################################################################################

    def _DnlCallActivity(self, activity_id, context, sto_0, sto_1, sto_2, sto_3,debug=False):
        '''This function is an indirect admin command used to call a DNL activity in the specified context. 
            arguments:
                activity_id - The ID of the activity to be called
                context - port number
                sto_0, sto_1, sto_2, sto_3 
            return: tuple contain-- sto_0, sto_1, sto_2, sto_3 
        '''

        driver = self.driver
            
        param0 = 0 # Activity id - 2 bytes, reserved - 1 byte, context 1 byte
        param0 = activity_id
        param0 = (param0 << 16) | context

        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x682
        aq_desc.flags = 0x1400
        aq_desc.datalen = 16
        aq_desc.param0 = param0

        buffer = []
        stos = [sto_0, sto_1, sto_2, sto_3]
        for sto in stos:
            buffer.append(sto & 0xFF)
            buffer.append((sto >> 8) & 0xFF)
            buffer.append((sto >> 16) & 0xFF)
            buffer.append((sto >> 24) & 0xFF)

        status = driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send DNL CALL ACTIVITY AQ command, status:', status, ', FW ret value: ', aq_desc.retval)

        sto_0 = compose_num_from_array_slice(buffer, 0, 4)
        sto_1 = compose_num_from_array_slice(buffer, 4, 4)
        sto_2 = compose_num_from_array_slice(buffer, 8, 4)
        sto_3 = compose_num_from_array_slice(buffer, 12, 4)
        
        return (sto_0, sto_1, sto_2, sto_3)

    def _DnlReadPstore(self, context, psto_index_to_read,debug=False):
        '''Function that returns the value of the specific PSTO requested
            arguments: 
                context - context number
                pstores_number_to_read - PSTO number to read
            return: pstores
        '''
         
        driver = self.driver
             
        psto_select = 0x1
        psto_size = 4
        psto_actual_index = psto_index_to_read + 1
        data_len = (psto_actual_index) * psto_size
        psto_select = (psto_select & 0xff) << 8
        context = context & 0xff
         
        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x683
        aq_desc.flags = 0x1000
        aq_desc.datalen = data_len
        aq_desc.param0 = psto_select | context    #byte 16 - context, 17 - store select
     
        buffer =[0] * data_len
         
        status = driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send DNL READ STORE AQ command, status:', status, ', FW ret value: ', aq_desc.retval)
             
        pstores = []
        index = 0
        for i in range(0, psto_actual_index):
            pstores.append(compose_num_from_array_slice(buffer, index, psto_size))
            index += psto_size
             
        return pstores[-1] 
     
    def _DnlWriteStore(self, context, store_type, store_index, value,debug=False):
        '''Function that write the value to specific PSTO.
            arguments: context - context number
                       store_type - 'sto' / 'psto'
                       store_index - offest
                       value - value to write
            return: None
        '''
        driver = self.driver
             
        if store_type == 'sto':
            sto_select = 0x0
        elif store_type == 'psto':
            sto_select = 0x1
        else:
            raise RuntimeError('Invalid store type: ' + store_type)
             
        store_index = (store_index & 0xffff ) << 16
        sto_select = (sto_select & 0xff) << 8
        context = context & 0xff
         
        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x684
        aq_desc.param0 =  store_index | sto_select | context # byte 16 - context, 17 - store select, 18:19 - offset
        aq_desc.param1 = value & 0xffffffff
         
        status = driver.send_aq_command(aq_desc,buffer,debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send DNL WRITE STORE AQ command, status:', status, ', FW ret value: ', aq_desc.retval)

    def DnlCvlDftTest(self, opcode,serdes_sel,data_in,debug=False):
        '''This function run DNL dft test according to the list below (CVL-DFT-DO.8EX file).
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
        '''This function return value from psore.
            argument: psto_index 
            return: value (hex)
        '''
        driver = self.driver
        context = driver.port_number()

        ret_val = self._DnlReadPstore(context,psto_index,debug=False)
        #print 'ret_val',ret_val
        #ret_val = ret_val.replace('L','')
        return hex(ret_val)

    def DnlGetPhyInfo(self):
        '''This function calls DNL script get_phy_info
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
        '''This function return port number
            argument: None
            return: port number (int)
        '''
        # driver = self.driver
        return self.driver.port_number()

    def ReadCsrRegister(self,offset):
        '''This function return CSR register value according to CSR register address.
            argument: offset - CSR register address
            return: value - CSR register value
        '''
        # driver = self.driver
        reg_value = self.driver.read_csr(offset)
        print("Register Value: ",hex(reg_value))

    def WriteCsrRegister(self,offset,value):
        '''This function write value to CSR register address.
            arguments: 
                offset - CSR register address
                value - value to write
            return: None
        '''
        # driver = self.driver
        self.driver.write_csr(offset, value)

    def ReadEthwRegister(self, address):
        '''This function support read from ethw.
            supporting read/write via SBiosf to neighbor device.
            arguments: 
                address - address to read in the neighbor device CSRs.
            return: 
                value - return value from the neighbor device.
        ''' 
        return_val = self.NeighborDeviceRead(0x2,0,1, address)
        return return_val

    def WriteEthwRegister(self,address,data):
        '''this function support write to ethw.
            supporting read/write via SBiosf to neighbor device.
            arguments: 
                address - address to write in the neighbor device CSRs.
                data - data to write in the neighbor device CSRs.
        ''' 
        self.NeighborDeviceWrite(0x2,1,1, address,data)
        pass

    def ReadMTIPRegister(self, offset,address,debug = False):
        '''this function read from MTIP in ethw.
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
        '''this function support Neighbor Device Request via AQ (CVL spec B.2.1.2)
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


        #print [hex(x) for x in buffer]

        return_buffer = self._NeighborDeviceRequestAq(0,buffer)
        #print "return_buffer: ",return_buffer
        pass

    def NeighborDeviceRead(self, dest,opcode,addrlen, address):
        '''this function support Neighbor Device Request via AQ (CVL spec B.2.1.2)
            supporting read/write via SBiosf to neighbor device.
            arguments: 
                dest - Neighbor Device address, according Table 3-33, in 3.3.4.1 CVL Spec.
                opcode - read/write etc...  according Table 3-34, in 3.3.4.1 CVL Spec
                addrlen - address length 0: 16 bit, 1: 48 bits. according Table B-8, appandix B.3.1 CVL spec
                address - address to read in the neighbor device CSRs.
            return: 
                value - return value from the neighbor device.
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
        Byte1_3rdDW = (SbIosfMassageDict['Sbe'] << 4) | (SbIosfMassageDict['fbe'] | 0xF) # the fbe value taken from BDX team
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

        # need to fill 0 for the ladt DW according tanya
        buffer.append(0)
        buffer.append(0)
        buffer.append(0)
        buffer.append(0)

        #print [hex(x) for x in buffer]
        #print "DW_1", hex(buffer[3] << 24 | buffer[2] << 16 | buffer[1] << 8 | buffer[0])
        #print "DW_2", hex(buffer[7] << 24 | buffer[6] << 16 | buffer[5] << 8 | buffer[4])
        #print "DW_3", hex(buffer[11] << 24 | buffer[10] << 16 | buffer[9] << 8 | buffer[8])
        #print "DW_4", hex(buffer[15] << 24 | buffer[14] << 16 | buffer[13] << 8 | buffer[12] )

        return_buffer = self._NeighborDeviceRequestAq(1,buffer)
        return_val = hex((return_buffer[7] << 24) | (return_buffer[6] << 16) | (return_buffer[5] << 8) |return_buffer[4])# print second DW
        #print "return val: ", return_val
        return return_val.replace("L","")

    def _NeighborDeviceRequestAq(self, opcode,Massage):
        '''this function support Neighbor Device Request via AQ (CVL spec B.2.1.2)
            supporting read/write via SBiosf to neighbor device.
            arguments: 
                Massage - massage value that contain the SB IOSF massage.
                opcode - 0 for write command, 1 for read command
            return:
                buffer from AQ
        '''
        driver = self.driver

        data_len = 16

        aq_desc = AqDescriptor()
        aq_desc.flags = 0x3400  # BUF flag - byte 1 bit 3 - for read buffer. 
        aq_desc.opcode = 0xC00
        aq_desc.datalen = data_len
        aq_desc.param0 = (data_len - 4) if opcode else data_len # buffer - 4 bytes (tanya Request)
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0

        #buffer = [0] * data_len
        buffer = Massage # verify how to put the massage in the buffer
        status = driver.send_aq_command(aq_desc, buffer)
        if status != 0 or aq_desc.retval != 0:
            error_msg = 'Error _NeighborDeviceRequestAq, status {} retval {}'.format(status, aq_desc.retval)
            raise RuntimeError(error_msg)

        #print "buffer: ",buffer
        return buffer

    def _Average(self, lst):
        '''This function return average of list
            argument: lst (list)
            return: none
        '''
        return sum(lst) / len(lst)

    def _GetValAddrPCIE(self, address):
        ''' This function returns PCIE value by input address
        '''
        driver = self.driver
        return driver.read_pci(address) 

    def _to_unsigned(self, value):
        '''This function convert sign value to unsigned.
            argument: value (sign number)
            return: unsigned value
        '''
        if value >= 0:
            return value
        else:
            return value + 2**8
        
     
    def SetMdioBit(self, Page,Register,BitNum):
        '''This function set MDIO bit.
        '''
        # driver = self.driver
        reg_value = self.driver.read_phy_register(Page, Register, self.driver.port_number())
        print(hex(reg_value))
        reg_value = reg_value | (1 << BitNum)
        print(hex(reg_value))
        self.driver.write_phy_register(Page, Register, driver.port_number(), reg_value)
     
    def ClearMdioBit(self,Page,Register,BitNum):
        '''This function clear MDIO bit.
        '''
        # driver = self.driver
        reg_value = self.driver.read_phy_register(Page, Register, self.driver.port_number())
        print(hex(reg_value))
        reg_value = reg_value & ~(1 << BitNum)
        print(hex(reg_value))
        self.driver.write_phy_register(Page, Register, self.driver.port_number(), reg_value)

    def CheckDeviceAliveness(self):
        '''This function returns true if the device is alive or false otherwise
            it's done for PCIe issue .
               return: True/false
        '''
        # driver = self.driver

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
        result = self.GetLinkStatus(gls)
        if not result[0]: # if Admin command was successful - False
            data = result[1]
        else:
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
        '''This function return dictionary that contain phy and mac link status and speed, fec mode.
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
     
        result = self.GetLinkStatus(gls)
        
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
        if self.Get_Speed_Status_dict:
            if data['link_speed_10m']:
                link_speed = self.Get_Speed_Status_dict[0]
                
            elif data['link_speed_100m']:
                link_speed = self.Get_Speed_Status_dict[1]
                
            elif data['link_speed_1000m']:
                link_speed = self.Get_Speed_Status_dict[2]
                
            elif data['link_speed_2p5g']:
                link_speed = self.Get_Speed_Status_dict[3]
                
            elif data['link_speed_5g']:
                link_speed = self.Get_Speed_Status_dict[4]
                
            elif data['link_speed_10g']:
                link_speed = self.Get_Speed_Status_dict[5]
                
            elif data['link_speed_20g']:
                link_speed = self.Get_Speed_Status_dict[6]
                
            elif data['link_speed_25g']:
                link_speed = self.Get_Speed_Status_dict[7]
                
            elif data['link_speed_40g']:
                link_speed = self.Get_Speed_Status_dict[8]
                
            elif data['link_speed_50g']:
                link_speed = self.Get_Speed_Status_dict[9]
                
            elif data['link_speed_100g']:
                link_speed = self.Get_Speed_Status_dict[10]
                
            elif data['link_speed_200g']:
                link_speed = self.Get_Speed_Status_dict[11]

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
            quad = self.quad_for_2_ports_dict[port_num]        
            pmd_num = self.pmd_num_for_2_ports_dict[port_num]
        elif number_of_ports == 4:     
            if self.GetMuxStatus():
                quad = self.quad_for_4_ports_mux_dict[port_num]
                pmd_num = self.pmd_num_for_4_ports_mux_dict[port_num]
            else:
                quad = self.quad_for_4_ports_dict[port_num]        
                pmd_num = self.pmd_num_for_4_ports_dict[port_num]
        elif number_of_ports == 8:        
            quad = self.quad_for_8_ports_dict[port_num]
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
            pcs_offset = self.MTIP_100_PCS_Addr_Dict[quad]

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


    def configure_logging_dnl(self, enable):
        '''This function perform configuration for the dnl logging using aq command
            argument:
                enable: flag to enable/disable dnl logging
            return:
                None 
        '''
        driver = self.driver
        aq_desc = AqDescriptor()
        byte16 = 0x0 
        byte18 = 0x0 
        if enable:
            byte16 = 0x1  # bit 0 is 1 to enable AQ logging 
            byte18 = 0x1 
            #print "enable configure_logging_dnl"
        else:
            byte16 = 0x0  # bit 0 is 1 to enable AQ logging 
            byte18 = 0x1 
            #print "disable configure_logging_dnl"
        param0 = (byte18 & 0xff ) << 16
        param0 = param0 | (byte16 & 0xff)

        buf = []            
        dnl_module_index = 0x4  
        buf_data = (1 << 12) | (dnl_module_index & 0xffffff)    
        buf.append(buf_data & 0xff) 
        buf.append((buf_data >> 8) & 0xff)
            
        aq_desc = AqDescriptor()
        aq_desc.opcode = 0xff09
        aq_desc.flags = 0x1400
        aq_desc.datalen = len(buf)
        aq_desc.param0 = param0 

        status = driver.send_aq_command(aq_desc, buf)
        if status != 0 or aq_desc.retval != 0:
            raise RuntimeError('Failed to configure logging, failed to send aq command, status={}, retval={}'.format(status, aq_desc.retval))

        #print 'configure logging aq command has been sent successfully'

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


###############################################################################
#                                Admin Queue Commands                         #
###############################################################################

    def SetPhyConfig(self, config, debug=False):
        #Updated for HAS 1.3
        '''
            Description:  Set various PHY configuration parameters on port. 
            input:
                config -- type(dict)
                    'port' : int[1 byte] -- Logical Port Number
                    'phy_type_0' : int[4 bytes] -- Bytes 3:0 of PHY capabilities, bit definitions in Section 3.5.3.2.1 of CPK HAS
                    'phy_type_1' : int[4 bytes] -- Bytes 7:4 of PHY capabilities, bit definitions in Section 3.5.3.2.1 of CPK HAS
                    'phy_type_2' : int[4 bytes] -- Bytes 11:8 of PHY capabilities, bit definitions in Section 3.5.3.2.1 of CPK HAS
                    'phy_type_3' : int[4 bytes] -- Bytes 15:12 of PHY capabilities, bit definitions in Section 3.5.3.2.1 of CPK HAS
                    'tx_pause_req' : int[1 bit] -- bit to request that TX_PAUSE be enabled on the link
                    'rx_pause_req' : int[1 bit] -- bit to request that RX_PAUSE be enabled on the link
                    'low_pwr_abil' : int[1 bit] -- bit to indicate if modules may engage Power Classes higher than 1, if set only Power Class 1 is allowed
                    'en_link' : int[1 bit] -- 1 to enable link, 0 to disable link
                    'en_auto_update' : int[1 bit] -- 1 to allow FW to issue Setup Link command immediately after SetPHYConfig completes, 0 to only execute SetPHYConfig
                    'lesm_en' : int[1 bit] -- 1 to enable LESM, 0 to disable
                    'auto_fec_en' : int[1 bit] -- 1 to enable AutoFEC, 0 to disable
                    'low_pwr_ctrl' : int[1 bit]  - 1 to enable D3cold LPLU, 0 to disable D3cold LPLU
                    'eee_cap_en' : int[2 bytes] - bitfield defined in Section 3.5.7.6.8 of CPK has to enable or disable advertisement of EEE capabilities
                    'eeer' : int[2 bytes] -- Value to program to EEER register of the MAC
                    'fec_firecode_10g_abil' : int[1 bit] -- Enable advertisement of 10G Fire Code FEC ability, only applicable in 10GBASE-KR
                    'fec_firecode_10g_req' : int[1 bit] -- Enable request for 10G Fire Code FEC, only applicable in 10GBASE-KR
                    'fec_rs528_req' : int[1 bit] -- Enable request for RS-528 FEC
                    'fec_firecode_25g_req' : int[1 bit] -- Enable request for 25G Fire Code FEC
                    'fec_rs544_req' : int[1 bit] -- Enable requuest for RS-544 FEC
                    'fec_rs528_abil' : int[1 bit] -- Enable advertisement of RS-528 FEC, only applicable for Consortium modes?
                    'fec_firecode_25g_req' : int[1 bit] -- Enable advertisement of 25G Fire Code FEC, only applicable for Consortium modes?
            return:
                status -- type(tuple) (bool, int)
                    bool -- Indication if Admin command was successful, False if so, True if not
                    int -- if bool True, value of Admin command retval, if false is None
        '''
        #Generic AQ descriptor --> Set PHY Config Admin command translation
        aq_desc = AqDescriptor()
        buffer = list()
        # Add PHY Type to buffer (bytes 0-15)
        buffer.extend(turn_arg_to_bytes(config['phy_type_0']))
        buffer.extend(turn_arg_to_bytes(config['phy_type_1']))
        buffer.extend(turn_arg_to_bytes(config['phy_type_2']))
        buffer.extend(turn_arg_to_bytes(config['phy_type_3']))
        byte_16 = (config['auto_fec_en'] << 7) | (config['lesm_en'] << 6) | (config['en_auto_update'] << 5) | (config.get('an_mode', 0) << 4) | (config['en_link'] << 3) | (config['low_pwr_abil'] << 2) | (config['rx_pause_req'] << 1) | config['tx_pause_req']
        byte_17 = config['low_pwr_ctrl'] & 0xff
        byte_18 = config['eee_cap_en'] & 0xff
        byte_19 = (config['eee_cap_en'] >> 8) & 0xff
        byte_20 = config['eeer'] & 0xff
        byte_21 = (config['eeer'] >> 8) & 0xff
        byte_22 = (config['fec_firecode_25g_abil'] << 7) | (config['fec_rs528_abil'] << 6) | (config['fec_rs544_req'] << 4) | (config['fec_firecode_25g_req'] << 3) | (config['fec_rs528_req'] << 2) | (config['fec_firecode_10g_req'] << 1) | config['fec_firecode_10g_abil']
        byte_23 = 0 & 0xFF  # FW requires buffer to be 24 bytes long, appending empty byte at the end of data structure to achieve this
        buffer.append(byte_16)
        buffer.append(byte_17)
        buffer.append(byte_18)
        buffer.append(byte_19)
        buffer.append(byte_20)
        buffer.append(byte_21)
        buffer.append(byte_22)
        buffer.append(byte_23)
        buffer.extend([0]*(0x100 - len(buffer)))
        aq_desc.opcode = 0x0601
        aq_desc.flags = 0x1400 #Include buffer and read flags for this command
        aq_desc.param0 = config['port']
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.datalen = len(buffer)
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Set PHY Config Admin Command, status: {} , FW ret value: {}'.format(status,aq_desc.retval))
        err_flag = (aq_desc.flags & 0x4) >> 2 #isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)
        
        return status

    def SetMacConfig(self, config, debug = False):
        #Update for HAS 1.3
        '''
            Description: Set various MAC configuration parameters on the port.
            input:
                config -- type(dict):
                    'max_frame' : int[2 bytes]  -- Sets the maximum ethernet frame size on a port
                    'pacing_type' : int[1 bit] -- 1 enables fixed IPG rate pacing, 0 is  data-based rate pacing -- Bytes 2.7
                    'pacing_rate' : int[4 bits] -- bitfield sets either the IPG words or the data pacing rate depending on state of pacing_type
                    'tx_priority' : int[1 byte]
                    'tx_value' : int[2 bytes]
                    'fc_refr_thresh' : int[2 bytes]
            return:
                status -- type(tuple) (bool, int)
                    bool -- Indication if Admin command was successful, False if so, True if not
                    int -- if bool True, value of Admin command retval, if false is None
        '''

        byte_0 = config['max_frame'] & 0xff
        byte_1 = (config['max_frame'] >> 8) & 0xff
        byte_2 = (config['pacing_type'] << 7) | (config['pacing_rate'] << 3)
        byte_3 = config['tx_priority'] & 0xff
        byte_4 = config['tx_value'] & 0xff
        byte_5 = (config['tx_value'] >> 8) & 0xff
        byte_6 = config['fc_refr_thresh']& 0xff
        byte_7 = (config['fc_refr_thresh'] >> 8) & 0xff
        byte_8 = 0
        byte_9 = 0
        byte_10 = 0
        byte_11 = 0
        byte_12 = 0
        byte_13 = 0
        byte_14 = 0
        byte_15 = 0

        aq_desc = AqDescriptor()
        data_len = 0x0
        aq_desc.opcode = 0x0603
        aq_desc.datalen = data_len
        buffer = [0] * data_len
        aq_desc.param0 = (byte_3 << 24) | (byte_2 << 16) | (byte_1 << 8) | byte_0
        aq_desc.param1 = (byte_7 << 24) | (byte_6 << 16) | (byte_5 << 8) | byte_4
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.flags = 0x0
        
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Set MAC Config Admin Command, status: {}, FW ret value: {}'.format(status, aq_desc.retval))
        err_flag = (aq_desc.flags & 0x4) >> 2 #isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)
        return status

    def SetupLink(self, slu_args, debug = False):
        #Updated for HAS 1.3
        '''
            Description:  Sets up the link and restarts link auto-negotiation. This operation could bring down the link. This
                        command needs to be executed for other set link parameters to take effect on the link.
            input:
                slu_args -- type(dict):
                    'port' : int[1 byte]
                    'restart' : int[1 bit] -- 1 to restart the link
                    'enable' : int[1 bit] -- 1 to enable the link, 0 to disable the link
            return:
                status -- type(tuple) (bool, int)
                    bool -- Indication if Admin command was successful, False if so, True if not
                    int -- if bool True, value of Admin command retval, if false is None
        '''
        #Generic AQ descriptor --> Setup Link and Retart Auto-negotiation Admin command translation
        # e.g. descriptor_term = (most_significant bytes .. least_significant_bytes)
        # param0 = (enable + restart + reserved + logical_port_number)
        # param1 = (0)
        # addr_high = (0)
        # addr_low = (0)
        aq_desc = AqDescriptor()
        data_len = 0x0
        aq_desc.opcode = 0x0605
        aq_desc.datalen = data_len
        buffer = [0] * data_len
        aq_desc.param0 = (slu_args['enable'] << 18) | (slu_args['restart'] << 17) | slu_args['port']
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.flags = 0x0
        
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Setup Link Admin Command, status: ', status, ', FW ret value: ', aq_desc.retval)
        err_flag = (aq_desc.flags & 0x4) >> 2 #isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)
        return status

    def GetPhyAbilities(self, get_abils, debug=False):
        #Updated for HAS 1.3
        '''
            Description:  Get various PHY abilities supported on the port.
            input:
                get_abils -- type(dict)
                    'port' : int[1 byte]
                    'rep_qual_mod' : int[1 bit] -- 1 will report list of qualified modules, 0 will not
                    'rep_mode' : int[2 bits] -- 00b reports capabilities without media, 01b reports capabilities including media, 10b reports latest SW configuration request
            return:
                bool -- Indication if Admin command was successful, False if so, True if not
                dict -- 
                    'phy_type_0' : int[4 bytes] -- Bytes 3:0 of PHY capabilities, bit definitions in Section 3.5.3.2.1 of CPK HAS
                    'phy_type_1' : int[4 bytes] -- Bytes 7:4 of PHY capabilities, bit definitions in Section 3.5.3.2.1 of CPK HAS
                    'phy_type_2' : int[4 bytes] -- Bytes 11:8 of PHY capabilities, bit definitions in Section 3.5.3.2.1 of CPK HAS
                    'phy_type_3' : int[4 bytes] -- Bytes 15:12 of PHY capabilities, bit definitions in Section 3.5.3.2.1 of CPK HAS
                    'phy_type' : type(list) -- use get_all_phy_types utility to decode the phy_type_0, phy_type_1 , phy_type_2, phy_type_3 and return a string list of all phy types
                    'pause_abil': int[1 bit] -- 1 if capable of PAUSE advertisement, 0 if not capable
                    'asy_dir_abil' : int[1 bit] -- 1 if capable of ASY_DIR pause advertisement, 0 if not capable
                    'low_pwr_abil': int[1 bit] -- 0 for high power mode, 1 for low power mode
                    'link_mode' : int[1 bit] -- 1 if link is enabled, 0 if link is disabled
                    'an_mode' : int[1 bit] -- 1 if AN is enabled, 0 if AN is disabled
                    'en_mod_qual' : int[1 bit] -- 1 if Module or PHY qualification is enabled, 0 if not
                    'lesm_en' : int[1 bit] -- 1 if LESM is enabled, 0 if disabled
                    'auto_fec_en' : int[1 bit] -- 1 if AutoFEC is enabled, 0 if disabled
                    'low_pwr_ctrl' : int[1 bit] -- 1 if LPLU is enabled, 0 if LPLU is disabled
                    'eee_cap' : int[2 bytes] -- bitfied indicating which EEE capabilities are capable
                    'eeer' : int[2 bytes] -- Content of the EEER MAC register
                    'oui' : int[4 bytes] -- Current BASE-T PHY ID or Module Vendor ID
                    'phy_fw_ver' : int[8 bytes] -- Outermost PHY FW version
                    'fec_opt' : int[1 byte] -- Available FEC options for the link
                    'fec_firecode_10g_abil' : int[1 bit] -- Enable advertisement of 10G Fire Code FEC ability, only applicable in 10GBASE-KR
                    'fec_firecode_10g_req' : int[1 bit] -- Enable request for 10G Fire Code FEC, only applicable in 10GBASE-KR
                    'fec_rs528_req' : int[1 bit] -- Enable request for RS-528 FEC
                    'fec_firecode_25g_req' : int[1 bit] -- Enable request for 25G Fire Code FEC
                    'fec_rs544_req' : int[1 bit] -- Enable requuest for RS-544 FEC
                    'fec_rs528_abil' : int[1 bit] -- Enable advertisement of RS-528 FEC, only applicable for Consortium modes?
                    'fec_firecode_25g_req' : int[1 bit] -- Enable advertisement of 25G Fire Code FEC, only applicable for Consortium modes?
                    'mod_ext_comp_code' : int[1 byte] -- Extended compliance code of the attached external module, SFP+ (Addr 0xA0, Byte 36) 
                    'mod_id' : int[1 byte] -- module identifier of current module, SFP+ (Addr 0xA0, Byte 0) or QSFP+ (Addr 128, page 0)
                    'mod_sfp_cu_passive': int[1 bit] -- 1 if SFP+ Cu Passive is supported
                    'mod_sfp_cu_active': int[1 bit] -- 1 if SFP+ Cu Active is supported
                    'mod_10g_sr': int[1 bit] -- 1 if 10GBASE-SR is supported
                    'mod_10g_lr': int[1 bit] -- 1 if 10GBASE-LR is supported
                    'mod_10g_lrm': int[1 bit] -- 1 if 10GBASE-LRM is supported
                    'mod_10g_er': int[1 bit] -- 1 if 10GBASE-ER is supported
                    'mod_1g_comp_code' : int[1 byte] -- GbE compliance code of current module, SFP+ (Addr 0xA0, Byte 6) or QSFP+ (Addr 134, page0) 

                    'qual_mod_count' : int[1 byte] -- Number of qualified modules in list(max: 16)
                    'qual_mod_ids' : list[dicts] -- List of Qualified module IDs
                        {'vendor_oui' : int[3 bytes], 'vendor_pn' : int[16 bytes], 'vendor_rev' : int[4 bytes]}
                    if bool is True, dict becomes in with Admin command retval
        '''
        
        #Generic AQ descriptor --> Get PHY Abilities Admin command translation
        # e.g. descriptor_term = (most_significant bytes .. least_significant_bytes)
        # param0(bytes 16-19) = (rep_mode + rep_qual_mod + reserved + logical_port_number)
        # param1(bytes 20-23) = (0)
        # addr_high(bytes 24-27) = (0)
        # addr_low(bytes 28-31) = (0)

        aq_desc = AqDescriptor()
        data_len = 0x1000
        aq_desc.opcode = 0x0600
        aq_desc.datalen = data_len
        buffer = [0] * data_len
        aq_desc.param0 = (get_abils['rep_mode'] << 17) | (get_abils['rep_qual_mod'] << 16) | get_abils['port']
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.flags = 0x1200 #Set the buffer flag & long buffer flag
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Get PHY Abilities Admin Command, status: ', status, ', FW ret value: ', aq_desc.retval)
        err_flag = (aq_desc.flags & 0x4) >> 2 #isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            #The static section of Get PHY Abilities is 32 bytes
            #ut.compose_num_from_array_slice(input, index, width)
            data = {}
            mod_ids = []
            data['phy_type_0'] = compose_num_from_array_slice(buffer, 0, 4)
            data['phy_type_1'] = compose_num_from_array_slice(buffer, 4, 4)
            data['phy_type_2'] = compose_num_from_array_slice(buffer, 8, 4)
            data['phy_type_3'] = compose_num_from_array_slice(buffer, 12, 4)
            data['phy_type'] = compose_num_from_array_slice(buffer, 0, 16)

            phy_type_list = []        
            phy_type_list.extend(get_all_phy_types(data['phy_type_0'], 0))
            phy_type_list.extend(get_all_phy_types(data['phy_type_1'], 1))
            phy_type_list.extend(get_all_phy_types(data['phy_type_2'], 2))
            phy_type_list.extend(get_all_phy_types(data['phy_type_3'], 3))
            #TODO: change code base to not rely on this field. This Field will be deleted
            data['phy_type_list'] = phy_type_list

            data['pause_abil'] = (compose_num_from_array_slice(buffer, 16, 1) & 0x1)
            data['asy_dir_abil'] = (compose_num_from_array_slice(buffer, 16, 1) & 0x2) >> 1
            data['low_pwr_abil'] = (compose_num_from_array_slice(buffer, 16, 1) & 0x4) >> 2
            data['link_mode'] = (compose_num_from_array_slice(buffer, 16, 1) & 0x8) >> 3
            data['an_mode'] = (compose_num_from_array_slice(buffer, 16, 1) & 0x10) >> 4
            data['en_mod_qual'] = (compose_num_from_array_slice(buffer, 16, 1) & 0x20) >> 5
            data['lesm_en'] = (compose_num_from_array_slice(buffer, 16, 1) & 0x40) >> 6
            data['auto_fec_en'] = (compose_num_from_array_slice(buffer, 16, 1) & 0x80) >> 7
            data['low_pwr_ctrl'] = compose_num_from_array_slice(buffer, 17, 1) & 0x1
            data['eee_cap'] = compose_num_from_array_slice(buffer, 18, 2)
            data['eeer'] = compose_num_from_array_slice(buffer, 20, 2)
            data['oui'] = compose_num_from_array_slice(buffer, 22, 4)
            data['phy_fw_ver'] = compose_num_from_array_slice(buffer, 26, 8)
            data['fec_opt'] = compose_num_from_array_slice(buffer, 34, 1)
            data['fec_firecode_10g_abil'] = compose_num_from_array_slice(buffer, 34, 1) & 0x1
            data['fec_firecode_10g_req'] = (compose_num_from_array_slice(buffer, 34, 1) & 0x2) >> 1
            data['fec_rs528_req'] = (compose_num_from_array_slice(buffer, 34, 1) & 0x4) >> 2
            data['fec_firecode_25g_req'] = (compose_num_from_array_slice(buffer, 34, 1) & 0x8) >> 3
            data['fec_rs544_req'] = (compose_num_from_array_slice(buffer, 34, 1) & 0x10) >> 4
            data['fec_rs528_abil'] = (compose_num_from_array_slice(buffer, 34, 1) & 0x40) >> 6
            data['fec_firecode_25g_abil'] = (compose_num_from_array_slice(buffer, 34, 1) & 0x80) >> 7
            data['mod_ext_comp_code'] = compose_num_from_array_slice(buffer, 36, 1)
            data['current_module_type'] = compose_num_from_array_slice(buffer, 37, 3)
            #TODO: remove these fiedlds from code
            data['mod_id'] = compose_num_from_array_slice(buffer, 37, 1) # TODO to be deleted
            data['mod_sfp_cu_passive'] = compose_num_from_array_slice(buffer, 38, 1) & 0x1  # TODO to be deleted
            data['mod_sfp_cu_active'] = (compose_num_from_array_slice(buffer, 38, 1) & 0x2) >> 1  # TODO to be deleted
            data['mod_10g_sr'] = (compose_num_from_array_slice(buffer, 38, 1) & 0x10) >> 4  # TODO to be deleted
            data['mod_10g_lr'] = (compose_num_from_array_slice(buffer, 38, 1) & 0x20) >> 5  # TODO to be deleted
            data['mod_10g_lrm'] = (compose_num_from_array_slice(buffer, 38, 1) & 0x40) >> 6  # TODO to be deleted
            data['mod_10g_er'] = (compose_num_from_array_slice(buffer, 38, 1) & 0x80) >> 7  # TODO to be deleted
            data['mod_1g_comp_code'] = compose_num_from_array_slice(buffer, 39, 1)  # TODO to be deleted

            data['qual_mod_count'] = compose_num_from_array_slice(buffer, 40, 1)
            data['qual_mod_ids'] = 0 #TODO - read CVL HAS TABLE:3-104
            status = (False, data)
        return status

    def GetLinkStatus(self, gls,debug=False):
        #Updated for HAS 1.3
        '''
            Description:  Get link status of the port.
            input:
                gls -- dict
                    'port' : int[1 byte]
                    'cmd_flag': int[2 bits] -- See description in Table 3-105 of CPK HAS
            return:
                status -- type(tuple) (bool, dict)
                bool -- Indication if Admin command was successful, False if so, True if not
                dict -- 
                    'lse_enabled' : int[1 bit] -- 1 if LSE is enabled, 0 if disabled
                    'topo_conflict' : int[1 bit] -- 1 if topology conflict detect, 0 if not
                    'media_conflict' : int[1 bit] -- 1 if media conflict detected, 0 if not
                    'lom_topo_corrupt' : int[1 bit] -- 1 if LOM topology netlist is corrupted, 0 if not
                    'link_sts': int[1 bit] -- 1 if link is up, 0 if down
                    'link_fault': int[1 bit] -- 1 if PHY has detected a link fault condition
                    'tx_link_fault': int[1 bit] -- 1 if a transmit link fault condition is detected 'rx_link_fault': int[1 bit] -- 1 if a receive link fault condition is detected 'remote_fault': int[1 bit] -- 1 if a remote fault condition is detected
                    'ext_prt_sts' : int[1 bit] -- 1 if link up, 0 if down
                    'media_avail' : int[1 bit] -- 1 if media is availble, 0 if not
                    'sig_det' int[1 bit] -- 1 if signal detected, 0 if not
                    'an_comp' : int[1 bit] -- 1 if AN completed successfully, 0 if not(only valid if PHY type supports AN)
                    'lp_an_abil' : int[1 bit] -- 1 if LP supports AN, 0 if not(only valid if PHY type supports AN)
                    'pd_fault' : int[1 bit] -- 1 if parallel detect fault occured, 0 if not(only valid if AN w/ pd support enabled)
                    '10g_kr_fec' : int[1 bit] -- 1 if KR, KR4 or CR4 FEC is enabled, 0 if not(only valid if PHY supports FEC)
                    'low_pwr_state' : int[1 bit] -- 1 if low power mode, 0 if high power mode
                    'tx_pause' : int[1 bit] -- 1 if TX Pause is enabled
                    'rx_pause' : int[1 bit] -- 1 if RX Pause is enabled
                    'qual_mod' : int[1 bit] -- 1 if the module is qualified, 0 if not
                    'temp_alarm' : int[1 bit] -- 1 if temp alarm is asserted by PHY, 0 if not
                    'hi_err' : int[1 bit] -- 1 if high_ber reported by the PHY
                    'tx_susp' : int[2 bits] -- Refer to Table 3-107 in HAS for bitfield definition
                    'lcl_lpbk' : int[1 bit] -- Indicates that PHY local loopback is enabled
                    'rem_lpbk' : int[1 bit] -- Indicates that PHY remote loopback is enabled
                    'mac_lpbk' : int[1 bit] -- Indicates that MAC local loopback is enabled
                    'max_frame' : int[2 bytes] -- Max frame size set on the port
                    '25g_kr_fec' : int[1 bit] -- 1 if 25G KR FEC was negotiated on the link
                    '25g_rs_528' : int[1 bit] -- 1 if 25G RS 528 FEC negotiated on the link
                    'rs_544' : int[1 bit] -- 1 if RS 544 FEC was negotiated on the link
                    'pacing_type' : int[1 bit] -- Determines if Inter-Packet Gap is used for rate pacing or data dependent
                    'pacing_rate' : int[4 bits] -- Refer to Table 3-66 for bitfield definition
                    'link_speed_10m' : int[1 bit] -- 1 if current link speed is 10 Mbps
                    'link_speed_100m' : int[1 bit] -- 1 if current link speed is 100 Mbps
                    'link_speed_1000m' : int[1 bit] -- 1 if current link speed is 1000 Mbps
                    'link_speed_2p5g' : int[1 bit] -- 1 if current link speed is 2.5 Gbps
                    'link_speed_5g' : int[1 bit] -- 1 if current link speed is 5 Gbps
                    'link_speed_10g' : int[1 bit] -- 1 if current link speed is 10 Gbps
                    'link_speed_20g' : int[1 bit] -- 1 if current link speed is 20 Gbps
                    'link_speed_25g' : int[1 bit] -- 1 if current link speed is 25 Gbps
                    'link_speed_40g' : int[1 bit] -- 1 if current link speed is 40 Gbps
                    'link_speed_50g' : int[1 bit] -- 1 if current link speed is 50 Gbps
                    'link_speed_100g' : int[1 bit] -- 1 if current link speed is 100 Gbps
                    'link_speed_200g' : int[1 bit] -- 1 if current link speed is 200 Gbps
                    'phy_type_0' : int[4 bytes] -- Bytes 3:0 of PHY TYPE field, Refer to Table 3-107 for bitfield definition
                    'phy_type_1' : int[4 bytes] -- Bytes 7:4 of PHY TYPE field, Refer to Table 3-107 for bitfield definition
                    'phy_type_2' : int[4 bytes] -- Bytes 11:8 of PHY TYPE field, Refer to Table 3-107 for bitfield definition
                    'phy_type_3' : int[4 bytes] -- Bytes 15:12 of PHY TYPE field, Refer to Table 3-107 for bitfield definition
                    'phy_type' : type(list) -- use get_all_phy_types utility to decode the phy_type_0, phy_type_1 , phy_type_2, phy_type_3 and return a string list of all phy types
                if bool is True, dict becomes int with Admin command retval
        '''
        #Generic AQ descriptor --> Get Link Status Admin command translation
        # e.g. descriptor_term = (most_significant bytes .. least_significant_bytes)
        # param0(bytes 16-19) = (cmd_flag + reserved + logical_port_number)
        # param1(bytes 20-23) = (0)
        # addr_high(bytes 24-27) = (0)
        # addr_low(bytes 28-31) = (0)
        aq_desc = AqDescriptor()
        data_len = 0x1000
        aq_desc.opcode = 0x0607
        aq_desc.datalen = data_len
        buffer = [0] * data_len
        aq_desc.param0 = (gls['cmd_flag'] << 16) | gls['port']
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.flags = 0x1200 #Set the buffer and long buffer flags
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Get Link Status Admin Command, status: ', status, ', FW ret value: ', aq_desc.retval)
        err_flag = (aq_desc.flags & 0x4) >> 2 #isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            #The static section of Get PHY Abilities is 32 bytes
            #ut.compose_num_from_array_slice(input, index, width)
            if debug:
                print(buffer)
            data = {}
            data['lse_enabled'] = (aq_desc.param0 & 0x10000)
            data['topo_conflict'] = compose_num_from_array_slice(buffer, 0, 1) & 0x1
            data['media_conflict'] = (compose_num_from_array_slice(buffer, 0, 1) & 0x2) >> 1
            data['lom_topo_corrupt'] = (compose_num_from_array_slice(buffer, 0, 1) & 0x4) >> 2
            data['link_sts'] = (compose_num_from_array_slice(buffer, 2, 1) & 0x1)
            data['link_fault'] = (compose_num_from_array_slice(buffer, 2, 1) & 0x2) >> 1
            data['tx_link_fault'] = (compose_num_from_array_slice(buffer, 2, 1) & 0x4) >> 2
            data['rx_link_fault'] = (compose_num_from_array_slice(buffer, 2, 1) & 0x8) >> 3
            data['remote_fault'] = (compose_num_from_array_slice(buffer, 2, 1) & 0x10) >> 4
            data['ext_prt_sts'] = (compose_num_from_array_slice(buffer, 2, 1) & 0x20) >> 5
            data['media_avail'] = (compose_num_from_array_slice(buffer, 2, 1) & 0x40) >> 6
            data['sig_det'] = (compose_num_from_array_slice(buffer, 2, 1) & 0x80) >> 7
            data['an_comp'] = (compose_num_from_array_slice(buffer, 3, 1) & 0x1)
            data['lp_an_abil'] = (compose_num_from_array_slice(buffer, 3, 1) & 0x2) >> 1
            data['pd_fault'] = (compose_num_from_array_slice(buffer, 3, 1) & 0x4) >> 2
            data['10g_kr_fec'] = (compose_num_from_array_slice(buffer, 3, 1) & 0x8) >> 3
            data['low_pwr_state'] = (compose_num_from_array_slice(buffer, 3, 1) & 0x10) >> 4
            data['tx_pause'] = (compose_num_from_array_slice(buffer, 3, 1) & 0x20) >> 5
            data['rx_pause'] = (compose_num_from_array_slice(buffer, 3, 1) & 0x40) >> 6
            data['qual_mod'] = (compose_num_from_array_slice(buffer, 3, 1) & 0x80) >> 7
            data['temp_alarm'] = compose_num_from_array_slice(buffer, 4, 1) & 0x1
            data['hi_err'] = (compose_num_from_array_slice(buffer, 4, 1) & 0x2) >> 1
            data['tx_susp'] = (compose_num_from_array_slice(buffer, 4, 1) & 0xC) >> 2
            data['lcl_lpbk'] = compose_num_from_array_slice(buffer, 5, 1) & 0x1
            data['rem_lpbk'] = (compose_num_from_array_slice(buffer, 5, 1) & 0x2) >> 1
            data['mac_lpbk'] = (compose_num_from_array_slice(buffer, 5, 1) & 0x4) >> 2
            data['max_frame'] = compose_num_from_array_slice(buffer, 6, 2)
            data['25g_kr_fec'] = compose_num_from_array_slice(buffer, 8, 1) & 0x1
            data['25g_rs_528'] = (compose_num_from_array_slice(buffer, 8, 1) & 0x2) >> 1
            data['rs_544'] = (compose_num_from_array_slice(buffer, 8, 1) & 0x4) >> 2
            data['pacing_config'] = (compose_num_from_array_slice(buffer, 8, 1) & 0xF8) >> 3
            data['ext_device_pwr_abil'] = (compose_num_from_array_slice(buffer, 9, 1) & 0x3)
            
            data['pacing_type'] = (compose_num_from_array_slice(buffer, 8, 1) & 0x80) >> 7 #TODO - to be deleted
            data['pacing_rate'] = (compose_num_from_array_slice(buffer, 8, 1) & 0x78) >> 3 #TODO - to be deleted
            data['current_link_speed'] = compose_num_from_array_slice(buffer, 10, 2)

            data['link_speed_10m'] = compose_num_from_array_slice(buffer, 10, 1) & 0x1 #TODO - to be deleted
            data['link_speed_100m'] = (compose_num_from_array_slice(buffer, 10, 1) & 0x2) >> 1 #TODO - to be deleted
            data['link_speed_1000m'] = (compose_num_from_array_slice(buffer, 10, 1) & 0x4) >> 2  #TODO - to be deleted
            data['link_speed_1000m'] = (compose_num_from_array_slice(buffer, 10, 1) & 0x4) >> 2 #TODO - to be deleted 
            data['link_speed_2p5g'] = (compose_num_from_array_slice(buffer, 10, 1) & 0x8) >> 3 #TODO - to be deleted
            data['link_speed_5g'] = (compose_num_from_array_slice(buffer, 10, 1) & 0x10) >> 4 #TODO - to be deleted
            data['link_speed_10g'] = (compose_num_from_array_slice(buffer, 10, 1) & 0x20) >> 5 #TODO - to be deleted
            data['link_speed_20g'] = (compose_num_from_array_slice(buffer, 10, 1) & 0x40) >> 6 #TODO - to be deleted
            data['link_speed_25g'] = (compose_num_from_array_slice(buffer, 10, 1) & 0x80) >> 7 #TODO - to be deleted
            data['link_speed_40g'] = compose_num_from_array_slice(buffer, 11, 1) & 0x1 #TODO - to be deleted
            data['link_speed_50g'] = (compose_num_from_array_slice(buffer, 11, 1) & 0x2) >> 1 #TODO - to be deleted
            data['link_speed_100g'] = (compose_num_from_array_slice(buffer, 11, 1) & 0x4) >> 2 #TODO - to be deleted
            data['link_speed_200g'] = (compose_num_from_array_slice(buffer, 11, 1) & 0x8) >> 3 #TODO - to be deleted

            data['phy_type_0'] = compose_num_from_array_slice(buffer, 16, 4)
            data['phy_type_1'] = compose_num_from_array_slice(buffer, 20, 4)
            data['phy_type_2'] = compose_num_from_array_slice(buffer, 24, 4)
            data['phy_type_3'] = compose_num_from_array_slice(buffer, 28, 4)
            data['phy_type'] = compose_num_from_array_slice(buffer, 16, 16)

            phy_type_list = [] #TODO - to be deleted
            phy_type_list.extend(get_all_phy_types(data['phy_type_0'], 0)) #TODO - to be deleted
            phy_type_list.extend(get_all_phy_types(data['phy_type_1'], 1)) #TODO - to be deleted
            phy_type_list.extend(get_all_phy_types(data['phy_type_2'], 2)) #TODO - to be deleted
            phy_type_list.extend(get_all_phy_types(data['phy_type_3'], 3)) #TODO - to be deleted
            data['phy_type_list'] = phy_type_list #TODO - to be deleted

            status = (False, data)
        return status

    def SetPhyLoopback(self, phy_lpbk_args, debug=False):
        #Updated for HAS 1.3
        '''
            Description:  Sets various PHYs loopback modes of the link
            input:
                phy_lpbk -- type(dict)
                    'port' : int[1 byte]
                    'index' : int[1 byte]
                    'enable' : int[1 bit]
                    'type' : int[1 bit]
                    'level' : int[1 bit]
            return:
                status -- type(tuple) (bool, int)
                    bool -- Indication if Admin command was successful, False if so, True if not
                    int -- if bool is False, None, else int is Admin command retval
        '''
        #Generic AQ descriptor --> Set PHY Loopback Admin command translation
        # e.g. descriptor_term = (most_significant bytes .. least_significant_bytes)
        # param0 = (level + type + enable + phy_index + logical_port_number)
        # param1 = (0)
        # addr_high = (0)
        # addr_low = (0)
        #helper = LM_Validation()
        aq_desc = AqDescriptor() # helper._debug('SetPhyLoopback Admin Command')
        data_len = 0x0
        aq_desc.opcode = 0x0619
        aq_desc.datalen = data_len
        buffer = [0] * data_len
        aq_desc.param0 = (phy_lpbk_args['level'] << 26) | (phy_lpbk_args['type'] << 25) | (phy_lpbk_args['enable'] << 24) | (phy_lpbk_args['index'] << 16) | phy_lpbk_args['port']
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.flags = 0x0
        
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Set Phy Loopback Admin Command, status: ', status, ', FW ret value: ', aq_desc.retval)
        err_flag = (aq_desc.flags & 0x4) >> 2 #isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)
        return status

    def SetPhyDebug(self, debug_args,debug=False):
        #Updated for HAS 1.3
        '''
            Description:  Resets PHYs or disables Link Management Firmware
            input:
                debug_args -- type(dict)
                    'port' : int[1 byte]
                    'index' : int[1 byte]
                    'cmd_flags' : int[1 byte] -- See Table 3-115 for bitfield description
            return:
                status -- type(tuple) (bool, int)
                    bool -- Indication if Admin command was successful, False if so, True if not
                    int -- if bool is False, None, else int is Admin command retval
        '''
        # Generic AQ descriptor --> Set PHY Debug Admin command translation
        # e.g. descriptor_term = (most_significant bytes .. least_significant_bytes)
        # param0 = (cmd_flags + index + port)
        # param1 = (0)
        # addr_high = (0)
        # addr_low = (0)

        driver = self.driver
        opCodes = AqOpCodes()
        #helper = LM_Validation()
        aq_desc = AqDescriptor()
       # helper._debug('SetPhyDebug Admin Command')
        data_len = 0x0
        aq_desc.opcode = opCodes.set_phy_debug
        aq_desc.datalen = data_len
        buffer = [0] * data_len
        aq_desc.param0 = (debug_args['cmd_flags'] << 24) | (debug_args['index'] << 16) | debug_args['port']
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.flags = 0x0

        status = driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Set Phy Debug Admin Command, status: ', status, ', FW ret value: ', aq_desc.retval)
        err_flag = (aq_desc.flags & 0x4) >> 2 #isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)
        return status

    def SetMacLoopback(self, args, debug = False):
        '''
            This method sends a Set MAC Loopback addmin command
        '''
        driver = self.driver
        opCodes = AqOpCodes()
        aq_desc = AqDescriptor()
        data_len = 0x0
        aq_desc.opcode = opCodes.set_mac_loopback
        aq_desc.datalen = data_len
        buffer = [0] * data_len
        aq_desc.param0 = args["loopback mode"]
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.flags = 0x0

        status = driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Set Phy Loopback Admin Command, status: ', status, ', FW ret value: ', aq_desc.retval)
        err_flag = (aq_desc.flags & 0x4) >> 2 #isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)
        return status


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
        reg = (self.ReadLcbRegister(0x50))
        val = get_bits_slice_value(reg,16,19) #speed

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
        reg = (self.ReadLcbRegister(0x50))
        val = get_bits_slice_value(reg,20,24) #width

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
        '''This function returns Device power state: 
            argument: None
            return: "D0" / "Reserved" / "D3hot"
        '''
        reg = self._GetValAddrPCIE(0x44)
        val = get_bits_slice_value(reg[1],0,1)

        power_sate = {
            0: "D0",
            2: "Reserved",
            3: "D3hot"
        }
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

    def GetLinkTopologyHandle(self, port, debug = False):
        '''This function returs node handler of a given port
            argument:
                logical_port_number -- (int) 0:7
                debug -- (bool) True/False - if True, print all AQ fields
            return: 
                list --
                    list[0] - status : this the drivers return vlaue 0 = succefull admin command
                    list[1] - retval : this the FW return value 0 = succefull admin command
                    list[2] - dict --
                        'node_handle' - see Section 3.5.6.2.2 in HAS
                        'node_part_number' 
        '''
        handles = dict()
        driver = self.driver
        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x06E1
        aq_desc.flags = 0
        aq_desc.datalen = 0
        aq_desc.param0 = 0
        aq_desc.param0 = (0x2 << 20 | 0x6 << 16 | 1 << 8 | port)
        aq_desc.param1 = 0
        aq_desc.addr_high= 0
        aq_desc.addr_low = 0
        buffer = []
        status      = driver.send_aq_command(aq_desc,buffer)
        if debug == True:
            print("falg = " , hex(aq_desc.flags))
            print( "opcode = " , hex(aq_desc.opcode))
            print("datalen = " ,hex( aq_desc.datalen))
            print("retval = " , hex(aq_desc.retval))
            print("cookie_high = " , hex(aq_desc.cookie_high))
            print("cookie_low = " , hex(aq_desc.cookie_low))
            print("param0 = " , hex(aq_desc.param0))
            print("param1 = " , hex(aq_desc.param1))
            print("addr_high = " , hex(aq_desc.addr_high))
            print("addr_low = " , hex( aq_desc.addr_low))
            return aq_desc
        else:
            node_handle = (aq_desc.param1 & 0x3ff)
            node_part_number = (aq_desc.param1 & 0xff000000) >> 24
            data = dict()
            data['node_handle'] = node_handle
            data['node_part_number'] = node_part_number
        return  [status,aq_desc.retval,data]
        

    def ReadI2C(self, port,node_handle,memory_offset,debug = False):
        '''this function reads 16 bytes of I2C data of a cage in a port context. see HAS Table 3-135. Read I2C admin command (Opcode: 0x06E2)
            arguments: 
                port -- (int) logical port 
                node_handle -- (int) as it appears in the topology
                memory_offset -- offset of the memory address wanted
                debug -- (bool) True/False - if True, print all AQ fields
            return:
                list --
                    list[0] - status : this the drivers return. if vlaue 0 = succefull admin command
                    list[1] - retval : if the FW return value 0 = succefull admin command
                    list[2] - data : 16 bytes of I2C data of a cage in a port context
        '''

        driver  = self.driver
        aq_desc = AqDescriptor()
        aq_desc.opcode  = 0x6E2
        aq_desc.flags = 0
        aq_desc.datalen = 0
        aq_desc.param0 = (0x2 << 20 | 0x6 << 16 | 1 << 8 | port)
        aq_desc.param1 = 0
        aq_desc.param1 = (memory_offset << 16 | node_handle)
        aq_desc.addr_high= 0
        aq_desc.addr_high = (1 << 7 | 0xf)
        aq_desc.addr_low = 0
        buffer = []
        status  = driver.send_aq_command(aq_desc)
        if debug == True:
            print("falg = " ,hex(aq_desc.flags))
            print("opcode = " ,hex(aq_desc.opcode))
            print("datalen = " ,hex( aq_desc.datalen))
            print("retval = " ,aq_desc.retval)
            print("cookie_high = " ,hex(aq_desc.cookie_high))
            print("cookie_low = " ,hex(aq_desc.cookie_low))
            print("param0 = " ,hex(aq_desc.param0))
            print("param1 = " ,hex(aq_desc.param1))
            print("addr_high = " ,hex(aq_desc.addr_high))
            print("addr_low = " ,hex( aq_desc.addr_low))
            return aq_desc
        data =  intgerTo4ByteList(aq_desc.param0)
        data += intgerTo4ByteList(aq_desc.param1)
        data += intgerTo4ByteList(aq_desc.addr_high)
        data += intgerTo4ByteList(aq_desc.addr_low)
        return [status,aq_desc.retval,data]
        
    def WriteI2C(self, port,node_handle,memory_offset,data):
        '''this function write 1 bytes of I2C data. see HAS Table 3-135. write  I2C admin command (Opcode: 0x06E3)
            arguments: 
                port -- (int) logical port number : 0-8
                node_handle -- (int) topology node handle see  Get Link Topology Node Handle
                memory_offset -- this is a 16 bit adrress, address of the byte that the user wishs to write to
                data -- 1 byte of data 0x00 - 0xff. larger numbers are masked only the first 8 bits of the number are written.
            return: 
                list --
                    list[0] - status : this the drivers return vlaue 0 = succefull admin command
                    list[1] - retval : this the FW return value 0 = succefull admin command
        '''
        driver  = self.driver
        aq_desc = AqDescriptor()
        aq_desc.opcode  = 0x6E3
        aq_desc.flags = 0
        aq_desc.datalen = 0
        aq_desc.param0 = ( 0x2 << 20 | 0x6 << 16 | 1 << 8 | port)
        aq_desc.param1 = 0
        aq_desc.param1 = (memory_offset << 16 | node_handle)
        aq_desc.addr_high= 0
        I2C_data = data & 0xff
        aq_desc.addr_high = (I2C_data << 8 | 1)
        aq_desc.addr_low = 0
        buffer = []
        status  = driver.send_aq_command(aq_desc)
        return [status,aq_desc.retval]

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
        return self.ReadDnlPstore(0x1B)
