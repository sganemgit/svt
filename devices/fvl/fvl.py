
#--------------------------------------------
# @author Shady Ganem <shady.ganem@intel.com>
#--------------------------------------------

import sys
from core.structs.AqDescriptor import AqDescriptor
from core.utilities.BitManipulation import *
import time

from devices.fvl.fvlDefines import fvlDefines


class fvl(fvlDefines):
    '''
		This class defines all interfaces to the fvl device
	'''

    
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
            '''This function reads all PTC FVL register
                    Total Packets Transmitted Counter (12.2.2.19.36 - 12.2.2.19.49)
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
                This function reads all PRC FVL registers
                Total Packets Received Counter (12.2.2.19.23-12.2.2.19.35)
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
            
    ##############################################################################################	

    # def GetCRCERRS(self):
    #         ''' This function counts the number of receive packets with CRC error, this includes
    #                 packets that are also counted by other error registers. (12.2.2.19.59)
    #                 GLPRT_CRCERRS = 0x00300080
    #         '''
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x00300080, 0x8, driver.port_number())
    #         reg_data = driver.read_csr(reg_addr)
    #         return reg_data
            
    # def GetILLERRC(self):
    #         ''' This function counts the number of receive packets with Illegal bytes errors. (12.2.2.19.60)
    #                 GLPRT_ILLERRC = 0x003000E0
    #         '''
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x003000e0, 0x8, driver.port_number())
    #         reg_data = driver.read_csr(reg_addr)
    #         return reg_data
            
    # def GetERRBC(self):
    #         ''' This function counts the number of receive packets with Error bytes.
    #                 This counter is only active when in 10G mode (12.2.2.19.61)
    #                 GLPRT_ERRBC = 0x003000C0 
    #         '''
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x003000c0, 0x8, driver.port_number())
    #         reg_data = driver.read_csr(reg_addr)
    #         return reg_data
            
    # def GetMLFC(self):
    #         ''' This function count the number of faults in the local MAC. (12.2.2.19.62)
    #                 GLPRT_MLFC = 0x00300020
    #         '''
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x00300020, 0x8, driver.port_number())
    #         reg_data = driver.read_csr(reg_addr)
    #         return reg_data
            
    # def GetMRFC(self):
    #         ''' This function count the number of faults in the remote MAC. (12.2.2.19.63)
    #                 GLPRT_MRFC = 0x00300040
    #         '''
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x00300040, 0x8, driver.port_number())
    #         reg_data = driver.read_csr(reg_addr)
    #         return reg_data
            
    # def GetRLEC(self):
    #         ''' This function counts the number of packets with receive length errors.
    #                 A length error occurs if an incoming packet length field in the MAC header doesn't match the packet length. (12.2.2.19.64)
    #                 GLPRT_RLEC = 0x003000A0
    #         '''
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x003000a0, 0x8, driver.port_number())
    #         reg_data = driver.read_csr(reg_addr)
    #         return reg_data
            
    # def GetRUC(self):
    #         ''' Receive Undersize Error. This function counts the number of received frames that are shorter than
    #                 minimum size (64 bytes from <Destination Address> through <CRC>, inclusively), and had a valid CRC. (12.2.2.19.65)
    #                 GLPRT_RUC = 0x00300100
    #         ''' 
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x00300100, 0x8, driver.port_number())
    #         reg_data = driver.read_csr(reg_addr)
    #         return reg_data
            
    # def GetRFC(self):
    #         '''Receive Fragments Count. This function counts the number of received frames that are shorter than
    #                 minimum size (64 bytes from <Destination Address> through <CRC>, inclusively), and had an invalid CRC. (12.2.2.19.66)
    #                 GLPRT_RFC = 0x00300560
    #         '''  
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x00300560, 0x8, driver.port_number())
    #         reg_data = driver.read_csr(reg_addr)
    #         return reg_data

    # def GetROC(self):
    #         '''Receive oversize Error. This function counts the number of received frames that are longer than
    #                 maximum size as defined by the "Set MAC config" command (from <Destination Address> through <CRC>,
    #                 inclusively) and have valid CRC. (12.2.2.19.67)
    #                 GLPRT_ROC = 0x00300120
    #         '''	
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x00300120, 0x8, driver.port_number())
    #         reg_data = driver.read_csr(reg_addr)
    #         return reg_data

    # def GetRJC(self):
    #         '''Receive jabber errors. This function counts the number of received packets that passed address filtering,
    #                 and are greater than maximum size and have bad CRC (this is slightly different from the Receive Oversize Count register).
    #                 The packets length is counted from <Destination Address> through <CRC>, inclusively. (12.2.2.19.68)
    #                 GLPRT_RJC = 0x00300580
    #         '''
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x00300580, 0x8, driver.port_number())
    #         reg_data = driver.read_csr(reg_addr)
    #         return reg_data
            
    # def GetMSPDC(self):
    #         '''This function counts the number of MAC short Packets Discarded. This counter is only active when in 10G mode. (12.2.2.19.69)
    #                 GLPRT_MSPDC = 00300060
    #         ''' 
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x00300060, 0x8, driver.port_number())
    #         reg_data = driver.read_csr(reg_addr)
    #         return reg_data
            
    # def GetLDPC_FVL(self):
    #         '''This function counts the number of VM to VM loopback packets discarded. (12.2.2.19.70)
    #                 GLPRT_LDPC = 0x00300620
    #         ''' 
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x00300620, 0x8, driver.port_number())
    #         reg_data = driver.read_csr(reg_addr)
    #         return reg_data

    def GetLDPC_ORCA(self):
            '''This function counts the number of low density parity check (LDPC) CRC errors in ORCA
            '''
            driver = self.driver
            low_data = driver.read_phy_register(0x1, 0xB08B, self.Phy_Address_dict[driver.port_number()])
            high_data = driver.read_phy_register(0x1, 0xB08C, self.Phy_Address_dict[driver.port_number()])
            return (((high_data & 0xffff) <<16) | low_data)

    def GetMacErrorsStatistics(self, ErrorStatistics):
            # handler = get_handler()
            ErrorsStatistics_list = ["MSPDC", "CRCERRS", "ILLERRC", "ERRBC", "MLFC", "MRFC", "RLEC", "RUC", "RFC", "ROC", "RJC","FVL_LDPC"]
            ErrorStatistics['ErrorSummary'] = 0
            for error in ErrorsStatistics_list:
                result = self.read_register(reg)
                ErrorStatistics[error] = result
                ErrorStatistics['ErrorSummary'] = ErrorStatistics['ErrorSummary'] +result

            # CRCERRS = GetCRCERRS()
            # ILLERRC = GetILLERRC()
            # ERRBC = GetERRBC()
            # MLFC = GetMLFC()
            # MRFC = GetMRFC()
            # RLEC = GetRLEC()
            # RUC = GetRUC()
            # RFC = GetRFC()
            # ROC = GetROC()
            # RJC = GetRJC()
            # MSPDC = GetMSPDC()
            # FVL_LDPC = GetLDPC_FVL()
            ORCA_LDPC = GetLDPC_ORCA()

            # ErrorStatistics['CRCERRS'] = CRCERRS
            # ErrorStatistics['ILLERRC'] = ILLERRC
            # ErrorStatistics['ERRBC'] = ERRBC
            # ErrorStatistics['MLFC'] = MLFC
            # ErrorStatistics['MRFC'] = MRFC
            # ErrorStatistics['RLEC'] = RLEC
            # ErrorStatistics['RUC'] = RUC
            # ErrorStatistics['RFC'] = RFC
            # ErrorStatistics['ROC'] = ROC  
            # ErrorStatistics['RJC'] = RJC
            # ErrorStatistics['MSPDC'] = MSPDC
            # ErrorStatistics['FVL_LDPC'] = FVL_LDPC
            # #ErrorStatistics['ORCA_LDPC'] = ORCA_LDPC

            # ErrorStatistics['ErrorSummary'] = CRCERRS+ILLERRC+MLFC+MRFC+ERRBC+RLEC+RUC+RFC+ROC+RJC+MSPDC+FVL_LDPC#+ORCA_LDPC
            # #print 'Reg statistics :' , ErrorStatistics
            return collections.OrderedDict(ErrorStatistics)	
    ############################################################################################################	

    # def ClearPTC64(self):
    #         '''This function clears PTC64 FVL register
    #                 Clear Packets Transmitted [64 Bytes] Counter (12.2.2.19.36/37)
    #                 GLPRT_PTC64L = 0x003006a0
    #                 GLPRT_PTC64H = 0x003006a4
    #         '''
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x003006a0, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         reg_addr = calculate_port_offset(0x003006a4, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass
            
    # def ClearPTC127(self):
    #         '''This function clears PTC127 FVL register
    #                 Clear Packets Transmitted [65-127 Bytes] Counter (12.2.2.19.38/39)
    #                 GLPRT_PTC127L = 0x003006c0
    #                 GLPRT_PTC127H = 0x003006c4
    #         '''
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x003006c0, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         reg_addr = calculate_port_offset(0x003006c4, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass

    # def ClearPTC255(self):
    #         '''This function clears PTC255 FVL register
    #                 Clear Packets Transmitted [128-255 Bytes] Counter (12.2.2.19.40/41)
    #                 GLPRT_PTC255L = 0x003006e0
    #                 GLPRT_PTC255H = 0x003006e4
    #         '''
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x003006e0, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         reg_addr = calculate_port_offset(0x003006e4, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass
            
    # def ClearPTC511(self):
    #         '''This function clears PTC511 FVL register
    #                 Clear Packets Transmitted [256-511 Bytes] Counter (12.2.2.19.42/43)
    #                 GLPRT_PTC511L = 0x00300700
    #                 GLPRT_PTC511H = 0x00300704
    #         '''
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x00300700, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         reg_addr = calculate_port_offset(0x00300704, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass
            
    # def ClearPTC1023(self):
    #         '''This function clears PTC1023 FVL register
    #                 Clear Packets Transmitted [512-1023 Bytes] Counter (12.2.2.19.44/45)
    #                 GLPRT_PTC1023L = 0x00300720
    #                 GLPRT_PTC1023H = 0x00300724
    #         '''
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x00300720, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         reg_addr = calculate_port_offset(0x00300724, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass
            
    # def ClearPTC1522(self):
    #         '''This function clears PTC1522 FVL register
    #                 Clear Packets Transmitted [1024-1522 Bytes] Counter (12.2.2.19.46/47)
    #                 GLPRT_PTC1522L = 0x00300740
    #                 GLPRT_PTC1522H = 0x00300744
    #         '''
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x00300740, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         reg_addr = calculate_port_offset(0x00300744, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass
            
    # def ClearPTC9522(self):
    #         '''This function clears PTC9522 FVL register
    #                 Clear Packets Transmitted [1523-9522 bytes] Counter (12.2.2.19.48/49)
    #                 GLPRT_PTC9522L = 0x00300760
    #                 GLPRT_PTC9522H = 0x00300764
    #         '''
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x00300760, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         reg_addr = calculate_port_offset(0x00300764, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass
            
    # def ClearPRC64(self):
    #         '''This function clears PRC64 FVL register
    #                 Clear Packets Received [64 Bytes] Counter (12.2.2.19.22/23)
    #                 GLPRT_PRC64L = 0x00300480
    #                 GLPRT_PRC64H = 0x00300484
    #         '''
    #         driver= self.driver
    #         reg_addr= calculate_port_offset(0x00300480, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         reg_addr= calculate_port_offset(0x00300484, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass
            
    # def ClearPRC127(self):
    #         '''This function clears PRC127 FVL register
    #                 Clear Packets Received [65-127 Bytes] Counter (12.2.2.19.24/25)
    #                 GLPRT_PRC127L = 0x003004a0
    #                 GLPRT_PRC127H = 0x003004a4
    #         '''
    #         driver= self.driver
    #         reg_addr= calculate_port_offset(0x003004a0, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         reg_addr= calculate_port_offset(0x003004a4, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass
            
    # def ClearPRC255(self):
    #         '''This function clears PRC255 FVL register
    #                 Clear Packets Received [128-255 Bytes] Counter (12.2.2.19.26/27)
    #                 GLPRT_PRC255L = 0x003004c0
    #                 GLPRT_PRC255H = 0x003004c4
    #         '''
    #         driver= self.driver
    #         reg_addr= calculate_port_offset(0x003004c0, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         reg_addr= calculate_port_offset(0x003004c4, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass
            
    # def ClearPRC511(self):
    #         '''This function clears PRC511 FVL register
    #                 Clear Packets Received [256-511 Bytes] Counter (12.2.2.19.28/29)
    #                 GLPRT_PRC511L = 0x003004e0
    #                 GLPRT_PRC511H = 0x003004e4
    #         '''
    #         driver= self.driver
    #         reg_addr= calculate_port_offset(0x003004e0, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         reg_addr= calculate_port_offset(0x003004e4, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass
            
    # def ClearPRC1023(self):
    #         '''This function clears PRC1023 FVL register
    #                 Clear Packets Received [512-1023 Bytes] Counter (12.2.2.19.30/31)
    #                 GLPRT_PRC1023L = 0x00300500
    #                 GLPRT_PRC1023H = 0x00300504
    #         '''
    #         driver= self.driver
    #         reg_addr= calculate_port_offset(0x00300500, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         reg_addr= calculate_port_offset(0x00300504, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass
            
    # def ClearPRC1522(self):
    #         '''This function clears PRC1522 FVL register
    #                 Clear Packets Received [1024-1522 Bytes] Counter (12.2.2.19.32/33)
    #                 GLPRT_PRC1522L = 0x00300520
    #                 GLPRT_PRC1522H = 0x00300524
    #         '''
    #         driver= self.driver
    #         reg_addr= calculate_port_offset(0x00300520, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         reg_addr= calculate_port_offset(0x00300524, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass
            
    # def ClearPRC9522(self):
    #         '''This function clears PRC9522 FVL register
    #                 Clear Packets Received [1523-9522 Bytes] Counter (12.2.2.19.34/35)
    #                 GLPRT_PRC9522L = 0x00300540
    #                 GLPRT_PRC9522H = 0x00300544
    #         '''
    #         driver= self.driver
    #         reg_addr= calculate_port_offset(0x00300540, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         reg_addr= calculate_port_offset(0x00300544, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass
    
    def Clear_register(self, register_name, mul=0x8):
        ''' 
            This function clears FVL register
            :param register_name: Defined in reg_dict in fvlDefines
        '''
        for addr in self.reg_dict[register_name]:
            reg_addr = calculate_port_offset(addr, mul, self.driver.port_number())
            self.driver.write_csr(reg_addr, 0xffffffff)

    ######################################################################################################

    # def ClearCRCERRS(self):
    #         ''' This function clears the count of receive packets with CRC error, this includes
    #                 packets that are also counted by other error registers. (12.2.2.19.59)
    #                 GLPRT_CRCERRS = 0x00300080
    #         '''
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x00300080, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass
            
    # def ClearILLERRC(self):
    #         ''' This function clears the count of receive packets with Illegal bytes errors. (12.2.2.19.60)
    #                 GLPRT_ILLERRC = 0x003000E0
    #         '''
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x003000e0, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass
            
    # def ClearERRBC(self):
    #         ''' This function clears the count of receive packets with Error bytes.
    #                 This counter is only active when in 10G mode (12.2.2.19.61)
    #                 GLPRT_ERRBC = 0x003000C0 
    #         '''
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x003000c0, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass
            
    # def ClearMLFC(self):
    #         ''' This function clears the count of faults in the local MAC. (12.2.2.19.62)
    #                 GLPRT_MLFC = 0x00300020
    #         '''
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x00300020, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass
            
    # def ClearMRFC(self):
    #         ''' This function clears the count of faults in the remote MAC. (12.2.2.19.63)
    #                 GLPRT_MRFC = 0x00300040
    #         '''
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x00300040, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass
            
    # def ClearRLEC(self):
    #         ''' This function clears the count of packets with receive length errors.
    #                 A length error occurs if an incoming packet length field in the MAC header doesn't match the packet length. (12.2.2.19.64)
    #                 GLPRT_RLEC = 0x003000A0
    #         '''
    #         driver = self.driver
    #         reg_addr = calculate_port_offset(0x003000a0, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass
            
    # def ClearRUC(self):
    #         ''' Receive Undersize Error. This function clears the count of received frames that are shorter than
    #                 minimum size (64 bytes from <Destination Address> through <CRC>, inclusively), and had a valid CRC. (12.2.2.19.65)
    #                 GLPRT_RUC = 0x00300100
    #         ''' 
    #         driver= self.driver
    #         reg_addr = calculate_port_offset(0x00300100, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass
            
    # def ClearRFC(self):
    #         '''Receive Fragments Count. This function clears the count of received frames that are shorter than
    #                 minimum size (64 bytes from <Destination Address> through <CRC>, inclusively), and had an invalid CRC. (12.2.2.19.66)
    #                 GLPRT_RFC = 0x00300560
    #         ''' 
    #         driver= self.driver
    #         reg_addr = calculate_port_offset(0x00300560, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass

    # def ClearROC(self):
    #         '''Receive oversize Error. This function clears the count of received frames that are longer than
    #                 maximum size as defined by the "Set MAC config" command (from <Destination Address> through <CRC>,
    #                 inclusively) and have valid CRC. (12.2.2.19.67)
    #                 GLPRT_ROC = 0x00300120
    #         '''
    #         driver= self.driver
    #         reg_addr = calculate_port_offset(0x00300120, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass

    # def ClearRJC(self):
    #         '''Receive jabber errors. This function clears the count of received packets that passed address filtering,
    #                 and are greater than maximum size and have bad CRC (this is slightly different from the Receive Oversize Count register).
    #                 The packets length is counted from <Destination Address> through <CRC>, inclusively. (12.2.2.19.68)
    #                 GLPRT_RJC = 0x00300580
    #         '''
    #         driver= self.driver
    #         reg_addr = calculate_port_offset(0x00300580, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass
            
    # def ClearMSPDC(self):
    #         '''This function clears the count of MAC short Packets Discarded. This counter is only active when in 10G mode. (12.2.2.19.69)
    #                 GLPRT_MSPDC = 0x00300060
    #         ''' 
    #         driver= self.driver
    #         reg_addr = calculate_port_offset(0x00300060, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass
            
    # def ClearLDPC_FVL(self):
    #         '''This function clears the count of VM to VM loopback packets discarded. (12.2.2.19.70)
    #                 GLPRT_LDPC = 0x00300620
    #         '''
    #         driver= self.driver
    #         reg_addr = calculate_port_offset(0x00300620, 0x8, driver.port_number())
    #         driver.write_csr(reg_addr, 0xffffffff)
    #         pass
            
    def ClearMACstat(self):
            '''This function clears following MAC statistics registers. 
                    clear: PTC, PRC, CRCERRS, ILLERRC, ERRBC, MLFC, MRFC, RLEC, RUC, RFC, ROC, RJC, MSPDC, LDPC_FVL, LDPC_ORCA.
                    (12.2.2.19)
            '''
            for reg in self.reg_dict:
                self.Clear_register(reg)
            
    #########################################################################################################
    ######################                 FVL                  #############################################
    #########################################################################################################

    def PrintDebugInfo(self):
            ''' This function returns MAC and PHY Parameters'''

            print "###################### FVL #############################################"
            reg_addr = calculate_port_offset(0x0008c260, 0x4, self.Phy_Address_dict[driver.port_number()])
            reg_value =  self.driver.read_csr(reg_addr)
            print "FVL Mac link status: ",GetMacLinkStatus()
            print "Tamar PCS link status: ",GetInternalPcsLinkStatus()
            FVLPcsMode = GetFVLPcsMode()
            print "Tamar PCS Mode: ",FVLPcsMode
            Mac_link_status_list = GetMacLinkStatus(GetSpeed = True)
            print "FVL MAC link speed: ",Mac_link_speed_dict[Mac_link_status_list[1]]
            #print "PCIE current link speed: ",GetPCIE_CurrentLinkSpeed()
            #print "PCIE current link width: ",GetPCIE_CurrentLinkWidth()
            print "FVL MAC remote fault: ", MacRemoteFault()
            print "FVL MAC local fault: ",MacLocalFault()
            if get_bit_value(reg_value, 13) == 1: print "AN_CLAUSE_37_ENABLE"
            if get_bit_value(reg_value, 16) == 1: print "Advertise support PCS 1G-KX ability"
            if get_bit_value(reg_value, 24) == 1: print "Advertise support for EEE PCS 1G-KX ability"
            if get_bit_value(reg_value, 18) == 1: print "Advertise support PCS 10G-KR ability"
            if get_bit_value(reg_value, 18) == 1: print "Advertise support for EEE PCS 10G-KR ability"
            if get_bit_value(reg_value, 29) == 1: print "AN_CLAUSE_73_ENABLE"
            print "###################### ORCA #############################################"
            
            print "ORCA PHY link status BaseT: ",GetPhyLinkStatus()
            print "ORCA PHY HOST link status: ",GetPhyHostInterLinkStatus()
            Port_type = Get_Port_Type()
            if Port_type == "BaseT":
                    print "Port type: ", Port_type
            link_speed = GetPhyLinkSpeed()
            real_speed = "10G"
            if link_speed == 2: real_speed = "100M"
            elif link_speed == 4: real_speed = "1G"
            elif link_speed == 6: real_speed = "10G"
            elif link_speed == 1: real_speed = "2.5G"
            elif link_speed == 3: real_speed = "5G"
            print "ORCA PHY link speed BaseT: ", real_speed
            MS_Status = Get_MS_Status()
            temp = "Slave" 
            if MS_Status == 1:
                    temp = "Master" 
            print "ORCA PHY resolved to","<",temp,">" 
            print "ORCA PHY Temperature: ",GetCurrentTemperature()
            if (FVLPcsMode == "KX" and real_speed == "1G") or (FVLPcsMode == "SGMII" and real_speed == "100M") :
                    print "ORCA 1G Remote Fault status: ", get_bit_value(Mdio_Read_Debug(0x7,0xFFE1), 4)
            else:
                    print "ORCA PMA fault status: ", PMAFault()
                    print "ORCA PCS fault status: ", PCSFault()
            #PmaPmdCap = Mdio_Read_Debug(0x1,0x0004)
            #print "PMA/PMD capability of operating at 100M: ", get_bit_value(PmaPmdCap, 5)
            #print "PMA/PMD capability of operating at 1G: ", get_bit_value(PmaPmdCap, 4)
            #print "PMA/PMD capability of operating at 10G: ", get_bit_value(PmaPmdCap, 0)
                    
    def GetFVLPcsMode(self):
            interface10G = "None"
            interface1G = "None"
            driver = self.driver
            reg_addr = calculate_port_offset(0x0008c260, 0x4, self.Phy_Address_dict[driver.port_number()])
            reg_value = driver.read_csr(reg_addr)
            SFI_XFI_KR_value = _get_bits_slice_value(reg_value, 2, 3)
            if SFI_XFI_KR_value == 2: interface10G = "SFI"
            elif SFI_XFI_KR_value == 1: interface10G = "XFI"
            elif SFI_XFI_KR_value == 0: interface10G = "KR"
            SGMII_KX_BX_value = (get_bit_value(reg_value, 12)<<1) + get_bit_value(reg_value, 6) 
            if SGMII_KX_BX_value == 2: interface1G = "SGMII"
            elif SGMII_KX_BX_value == 1: interface1G = "KX"
            elif SGMII_KX_BX_value == 0: interface1G = "BX"
            Mac_link_status_list = GetMacLinkStatus(GetSpeed = True)
            MacLinkSpeed = Mac_link_speed_dict[Mac_link_status_list[1]]
            if MacLinkSpeed == "10G": return interface10G 
            elif MacLinkSpeed == "1G" or MacLinkSpeed == "100M": return interface1G


    def GetMacLinkStatus(self, *bits,**options):
            '''This function returns the MAC_LINK_UP status bit by default.
                    If other bits are required pass as additional args.
                    Options:
                            GetSpeed = True/False
            '''

            reg_addr = calculate_port_offset(0x001E2420, 0x4, driver.port_number())
            reg_data = self.driver.read_csr(reg_addr)

            result=[]
            result.append(get_bit_value(reg_data,30))
            for bit_key in bits:
                    result.append(get_bit_value(reg_data,bit_key))
            if options.get('GetSpeed') == True:
                    result.append(_get_bits_slice_value(reg_data,27,29))
            if options.get('GetRF') == True:
                    result.append(get_bit_value(reg_data,2))
            if options.get('GetLF') == True:
                    result.append(get_bit_value(reg_data,3))
                    
            if len(result) == 1:
                    return result[0]
            return result

    def IsMacLinkUp(self, ttl_timeout):
            '''This function returns the if Mac Link UP.
                    argument:
                            ttl_timeout
                    return:
                            True if link is up else False
            '''
            driver = self.driver

            reg_addr = calculate_port_offset(0x001E2420, 0x4, driver.port_number())
            
            start_time = curr_time = time.time()
            while ((curr_time - start_time) < ttl_timeout):
                    curr_time = time.time()
                    reg_data = driver.read_csr(reg_addr)
                    if (get_bit_value(reg_data,30)):
                            return True
            return False

    def ToggleFwLM(self, enable):
            ''' 
                argument:
                            enable = True/False
            '''

            driver = self.driver

            aq_desc = AqDescriptor()
            aq_desc.opcode = 0x622
            aq_desc.param0 = 0x0 if enable else 0x30
            aq_desc.flags = 0x0200

            driver.send_aq_command(aq_desc)

    def MacReset(self, Reset):
            ''' 
                argument:
                        int Reset = 0: for core reset
                                                1: for global reset
                                                2:EMP reset
            '''
            driver = self.driver
            reg_addr = 0x00B8190
            reg_value = driver.read_csr(reg_addr)
            if Reset == 0:
                    reg_value = reg_value | (1<<0)
            elif Reset == 1:
                    reg_value = reg_value | (1<<1)	
            elif Reset == 2:
                    reg_value = reg_value | (1<<2)	
            else:
                    print "wrong reset - nothing to do"
            driver.write_csr(reg_addr, reg_value)

    def RestartAn(self, Location = "Ext_Phy"): 
            '''This function performs restart autoneg
                    [WIP] - add support for admin command reset
                    argument:
                            Location = Ext_Phy/AQ/Int_Phy
            '''
            driver = self.driver
            
            if Location == "Ext_Phy":
                    #ToggleFwLM(False)
                    HostOrBaseTDirection(1)
                    reg_value = driver.read_phy_register(0x7,0,self.Phy_Address_dict[driver.port_number()])
                    reg_value = reg_value | (1<<9)	
                    driver.write_phy_register(0x7, 0, self.Phy_Address_dict[driver.port_number()], reg_value)
                    
            elif Location == "AQ":
                    aq_desc = AqDescriptor()
                    aq_desc.opcode = 0x605
                    aq_desc.param0 = 0x6
                    aq_desc.flags = 0x0200
                    
                    buf = [0]
                    driver.send_aq_command(aq_desc)
                    
                    print 'retval: ', aq_desc.retval
                    print 'flags: ', aq_desc.flags
                    print 'opcode: ', aq_desc.opcode
                    print 'param0: ', aq_desc.param0
                    print 'param1: ', aq_desc.param1
                    print 'cookie_high: ', aq_desc.cookie_high
                    print 'cookie_low: ', aq_desc.cookie_low
                    print 'addr_high: ', aq_desc.addr_high
                    print 'addr_low: ', aq_desc.addr_low
            # TODO - need to match for Calsville	
            elif Location == "Int_Phy":
                    reg_addr = calculate_port_offset(0x0008c260, 0x4, driver.port_number())
                    reg_value = driver.read_csr(reg_addr)
                    reg_value |= 1<<31
                    driver.write_csr(reg_addr, reg_value)
                    
            else:
                    raise RuntimeError("Error RestartAn: Error Location, please insert location Int_Phy/AQ/Ext_Phy")	

    def SetInternalPcsLink(self, interface, speed): ## Ability --> 'SGMII' :('100M', '1G'), 'XFI': ('10G'), SFI: ('10G') 'KR': ('10G'), 'KX': ('1G') 
            '''This function sets Interface and Speed to PCS Link Control 0x0008c260. 
                    argument:
                            interface = 'SGMII', 'XFI', 'SFI', 'KR', 'KX'
                            speed = '100M', '1G', '10G' 
            '''
            driver = self.driver
            reg_addr = calculate_port_offset(0x0008c260, 0x4, driver.port_number())
            reg_value = driver.read_csr(reg_addr)
            #print hex(reg_value)
            reg_value &= 0x0000                         ## Reset register 
            ####### XFI -->> 0x80000404
            if interface == 'XFI':
                    reg_value |= 1<<2                       ## PMD_10G_R_Type_Selection -->> 3 = reserved, 2 = SFI, 1 = XFI, 0 = KR  
                    if speed == '10G':
                            reg_value |= 1<<10                  ## Speed Selection--> 1 = 100M, 2 = 1G, 4 = single lane 10G 
                            reg_value |= 1<<31                  ## Restart AN
                    else: print "Wrong speed insertion"
            ####### SFI -->> 0x80000408
            elif interface == 'SFI':
                    reg_value |= 1<<3                       ## PMD_10G_R_Type_Selection -->> 3 = reserved, 2 = SFI, 1 = XFI, 0 = KR
                    if speed == '10G':
                            reg_value |= 1<<10                  ## Speed Selection--> 1 = 100M, 2 = 1G, 4 = single lane 10G 
                            reg_value |= 1<<31                  ## Restart AN
                    else: print "Wrong speed insertion"
            ####### KR -->> 0xA0040400
            elif interface == 'KR':
                    reg_value |= 1<<29                      ## AUTO_NEG_ENABLE
                    if speed == '10G':
                            reg_value |= 1<<10                  ## Speed Selection--> 1 = 100M, 2 = 1G, 4 = single lane 10G  
                            reg_value |= 1<<18                  ## KR Ability
                            reg_value |= 1<<31                  ## Restart AN
                    else: print "Wrong speed insertion"
            ####### KX -->> 0xA0010240
            elif interface == 'KX':
                    reg_value |= 1<<6                       ## PMD_1G_X_Type_Selection -->>  2 = SGMII, 1 = KX, 0 = BX
                    reg_value |= 1<<29                      ## AUTO_NEG_ENABLE
                    if speed == '1G':
                            reg_value |= 1<<9                   ## Speed Selection--> 1 = 100M, 2 = 1G, 4 = single lane 10G  
                            reg_value |= 1<<16                  ## KX Ability	 
                            reg_value |= 1<<31                  ## Restart AN
                    else: print "Wrong speed insertion"
            ####### SGMII -->> 0xA0003200 = 1G; -->> 0xA0003100 = 100M
            elif interface == 'SGMII':
                    reg_value |= 1<<29                      ## AUTO_NEG_ENABLE
                    reg_value |= 1<<12                      ## PMD_1G_X_Type_Selection -->>  2 = SGMII, 1 = KX, 0 = BX
                    if speed == '1G':
                            reg_value |= 1<<9                   ## Set Speed
                            reg_value |= 1<<13                  ## Set AN_CLAUSE_37_ENABLE
                            reg_value |= 1<<31                  ## Restart AN
                    elif speed == '100M':
                            reg_value |= 1<<8                   ## Set Speed 
                            reg_value |= 1<<13                  ## Set AN_CLAUSE_37_ENABLE
                            reg_value |= 1<<31                  ## Restart AN
                    else: print "Wrong speed insertion"
            else: print "Wrong interface insertion"
            #print hex(reg_value)
            driver.write_csr(reg_addr, reg_value)

    def DBG_restartAN_test(self, num_of_iteration, ttl_timeout, link_stability_time):#TODO add link stability check and link drop source
            ttl_list = []
            avg_ttl = 0
            stable_dict = {}
            Mac_link_status_list = GetMacLinkStatus(GetSpeed = True)
            print "Link speed: ",Mac_link_speed_dict[Mac_link_status_list[1]]
            print "Protocol: ", GetFVLPcsMode()
            for i in range(num_of_iteration):
                    link_stable_flag = True	
                    print "Restart AN num: ",i
                    RestartAn("Int_Phy")
                    while (GetMacLinkStatus()):
                            pass
                    start_time = curr_time = curr_time_stable = stable_time = time.time()
                    link_flag = True
                    while ((curr_time - start_time) < ttl_timeout):       
                            curr_time = time.time()
                            mac_status1 = GetMacLinkStatus()
                            if mac_status1:
                                    curr_time = cur_time_stable = stable_time =  time.time()
                                    ##########################
                                    while ((curr_time_stable - stable_time) < link_stability_time):
                                            curr_time_stable = time.time()
                                            mac_status2 = GetMacLinkStatus()
                                            if mac_status1 != mac_status2:
                                                    link_stable_flag = False
                                            mac_status1	= mac_status2
                                    ##########################
                                    link_flag = False
                                    print 'link up'
                                    #time.sleep(1)
                                    break
                    ttl = curr_time - start_time
                    ttl_list.append(ttl)		
                    print "TTL: ",ttl
                    time.sleep(1)
                    if (not link_stable_flag):
                            print "Link is not stable in iteration num: ", i
                            stable_dict[i] = True
                    if (link_flag):
                            raw_input("Press enter to continue")
                            return(0)
            for i in ttl_list:
                     avg_ttl = avg_ttl + i
            print "AVG TTL: ",avg_ttl/len(ttl_list)
            for i in range(len(stable_dict)):
                    if stable_dict[i] == True:
                            print "Link was not stable at iteration num ", i
            

    def SetForceFvlLinkSpeed(self, interface, speed): ## Ability --> 'SGMII' :('1G'), 'KX' :('1G'), 'KR' :('10G')
            '''This function sets Interface and Speed to PCS Link Control 0x0008c260.
                    this will be use when Link Mng disable 
                    argument:
                            interface = 'SGMII', 'KR', 'KX'
                            speed =  '1G', '10G' 
            '''
            try:
                    driver = self.driver
                    ######################'KR': ('10G')#############################################
                    if interface == 'KR':
                            if speed != '10G':
                                    print "Wrong speed insertion"
                                    raise RuntimeError("Wrong speed insertion")
                            if speed == '10G':
                                    reg_addr = calculate_port_offset(0x8CE00, 0x4, driver.port_number())
                                    temp = driver.read_csr(reg_addr)
                                    temp = temp & 0xFFFFEFFF
                                    driver.write_csr(reg_addr, temp)
                                    reg_addr = calculate_port_offset(0x8C260, 0x4, driver.port_number())
                                    driver.write_csr(reg_addr, 0xA5048070)	
                    ######################'KX': ('1G')#############################################
                    elif interface == 'KX':
                            if speed != '1G':
                                    print "Wrong speed insertion"
                                    raise RuntimeError("Wrong speed insertion")
                            if speed == '1G':
                                    reg_addr = calculate_port_offset(0x8CE00, 0x4, driver.port_number())
                                    temp = driver.read_csr(reg_addr)
                                    temp = temp & 0xFFFFEFFF
                                    driver.write_csr(reg_addr, temp)
                                    reg_addr = calculate_port_offset(0x8C260, 0x4, driver.port_number())
                                    driver.write_csr(reg_addr, 0xA5018070)
                    ######################'SGMII': ('1G')#############################################
                    elif interface == 'SGMII':
                            if speed != '1G':
                                    print "Wrong speed insertion"
                                    raise RuntimeError("Wrong speed insertion")
                            if speed == '1G':	
                                    reg_addr = calculate_port_offset(0x8CE00, 0x4, driver.port_number())
                                    temp = driver.read_csr(reg_addr)
                                    temp = temp & 0xFFFFEFFF
                                    driver.write_csr(reg_addr, temp)
                                    reg_addr = calculate_port_offset(0x8C260, 0x4, driver.port_number())
                                    driver.write_csr(reg_addr, 0x80001238)
            except Exception as e:
                    print "Exception in fvl_eth:SetForceFvlLinkSpeed proclib Error: " + str(e)
                    print
                    raise RuntimeError("Exception in fvl_eth:SetForceFvlLinkSpeed proclib Error")

    def SetForceLinkSpeed(self, interface, speed): ## Ability --> 'SGMII' :('100M', '1G'), SFI: ('2.5G, 5G, 10G') 'KR': ('2.5G, 5G, 10G'), 'KX': ('1G') 
            '''This function sets Interface and Speed to PCS Link Control 0x0008c260 by MDIO.
                    this will be use when Link Mng disable 
                    argument:
                            interface = 'SGMII', 'XFI', 'SFI', 'KR', 'KX'
                            speed = '100M', '1G', '10G' 
            '''

            try:		
                    driver = self.driver
                    ######################'KR': ('2.5G, 5G, 10G')#############################################
                    if interface == 'KR':
                            if speed != '2.5G' and speed != '5G' and speed != '10G':
                                    print "Wrong speed insertion"
                                    raise RuntimeError("Wrong speed insertion")
                            if speed == '10G':
                                    reg_addr = calculate_port_offset(0x8CE00, 0x4, driver.port_number())
                                    temp = driver.read_csr(reg_addr)
                                    temp = temp & 0xFFFFEFFF
                                    driver.write_csr(reg_addr, temp)
                                    reg_addr = calculate_port_offset(0x8C260, 0x4, driver.port_number())
                                    driver.write_csr(reg_addr, 0xA5048070)
                                    #set KR mode enable on Orca host side
                                    self.GetCommandHandler(0x800f,1,1,0,0,0,0)
                                    #set direction to BaseT side			
                                    HostOrBaseTDirection(1)
                                    #clear low power mode
                                    reg_value = driver.read_phy_register(1, 0, self.Phy_Address_dict[driver.port_number()])
                                    reg_value = reg_value & 0xF7FF
                                    driver.write_phy_register(1, 0, self.Phy_Address_dict[driver.port_number()], reg_value)
                                    #Set 10G
                                    Adv10GLinkSpeed(True)				
                                    #clear 5G
                                    Adv5GLinkSpeed(False)
                                    #clear 2.5G
                                    Adv2p5GLinkSpeed(False)		
                                    #clear 1G
                                    Adv1GLinkSpeed(False)
                                    #clear 100M
                                    reg_value = driver.read_phy_register(7, 0x10, self.Phy_Address_dict[driver.port_number()])
                                    reg_value = reg_value & 0xF07F
                                    driver.write_phy_register(7, 0x10, self.Phy_Address_dict[driver.port_number()], reg_value)
                                    #set pause disable
                                    self.GetCommandHandler(0x8020,1,0,0,0,0,0)
                                    #Restart AN
                                    reg_value = driver.read_phy_register(7, 0, self.Phy_Address_dict[driver.port_number()])
                                    reg_value = reg_value | 0x1200
                                    driver.write_phy_register(7, 0, self.Phy_Address_dict[driver.port_number()], reg_value)
                                    #################################################################################### SFI PORTS THROUGHPUT
                                    reg_addr = calculate_port_offset(0x001C0980, 0x4, driver.port_number())
                                    temp = driver.read_csr(reg_addr)
                                    temp = temp & 0xFFFFFF00
                                    driver.write_csr(reg_addr, temp)
                                    ####################################################################################
                            elif speed == '5G':
                                    reg_addr = calculate_port_offset(0x8CE00, 0x4, driver.port_number())
                                    temp = driver.read_csr(reg_addr)
                                    temp = temp & 0xFFFFEFFF
                                    driver.write_csr(reg_addr, temp)
                                    reg_addr = calculate_port_offset(0x8C260, 0x4, driver.port_number())
                                    driver.write_csr(reg_addr, 0xA5048070)
                                    #set Pause and Pace Register
                                    reg_addr = calculate_port_offset(0x1E2040, 0x4, driver.port_number())
                                    temp = driver.read_csr(reg_addr)
                                    temp = temp & 0xFFFF
                                    temp = temp | 0x50000
                                    driver.write_csr(reg_addr, temp)
                                    #set LFC
                                    reg_addr = calculate_port_offset(0x1E2400, 0x4, driver.port_number())
                                    temp = driver.read_csr(reg_addr)
                                    temp = temp | 0x8 # set RFCE
                                    temp = temp & 0xFFFB # clear RPFCM
                                    driver.write_csr(reg_addr, temp)
                                    #set KR mode enable on Orca host side
                                    self.GetCommandHandler(0x800f,1,1,0,0,0,0)
                                    # Rate over XFI 10GBASE-R
                                    self.GetCommandHandler(0x8017,1,0,0,0,0,0)
                                    #set direction to BaseT side			
                                    HostOrBaseTDirection(1)
                                    #clear low power mode
                                    reg_value = driver.read_phy_register(1, 0, self.Phy_Address_dict[driver.port_number()])
                                    reg_value = reg_value & 0xF7FF
                                    driver.write_phy_register(1, 0, self.Phy_Address_dict[driver.port_number()], reg_value)
                                    #Set 10G
                                    Adv10GLinkSpeed(False)				
                                    #clear 5G
                                    Adv5GLinkSpeed(True)
                                    #clear 2.5GGetFVLPcsMode()
                                    Adv2p5GLinkSpeed(False)		
                                    #clear 1G
                                    Adv1GLinkSpeed(False)
                                    #clear 100M
                                    reg_value = driver.read_phy_register(7, 0x10, self.Phy_Address_dict[driver.port_number()])
                                    reg_value = reg_value & 0xF07F
                                    driver.write_phy_register(7, 0x10, self.Phy_Address_dict[driver.port_number()], reg_value)
                                    #set pause enable
                                    self.GetCommandHandler(0x8020,1,1,0,0,0,0)
                                    #Restart AN
                                    reg_value = driver.read_phy_register(7, 0, self.Phy_Address_dict[driver.port_number()])
                                    reg_value = reg_value | 0x1200
                                    driver.write_phy_register(7, 0, self.Phy_Address_dict[driver.port_number()], reg_value)
                                    #################################################################################### SFI PORTS THROUGHPUT
                                    reg_addr = calculate_port_offset(0x001C0980, 0x4, driver.port_number())
                                    temp = driver.read_csr(reg_addr)
                                    temp = temp | 0x000000FF
                                    driver.write_csr(reg_addr, temp)
                                    ####################################################################################
                            elif speed == '2.5G':
                                    reg_addr = calculate_port_offset(0x8CE00, 0x4, driver.port_number())
                                    temp = driver.read_csr(reg_addr)
                                    temp = temp & 0xFFFFEFFF
                                    driver.write_csr(reg_addr, temp)
                                    reg_addr = calculate_port_offset(0x8C260, 0x4, driver.port_number())
                                    driver.write_csr(reg_addr, 0xA5048070)
                                    #set Pause and Pace Register
                                    reg_addr = calculate_port_offset(0x1E2040, 0x4, driver.port_number())
                                    temp = driver.read_csr(reg_addr)
                                    temp = temp | 0x30000
                                    driver.write_csr(reg_addr, temp)
                                    #set LFC
                                    reg_addr = calculate_port_offset(0x1E2400, 0x4, driver.port_number())
                                    temp = driver.read_csr(reg_addr)
                                    temp = temp | 0x8 # set RFCE
                                    temp = temp & 0xFFFB # clear RPFCM
                                    driver.write_csr(reg_addr, temp)
                                    #set KR mode enable on Orca host side
                                    self.GetCommandHandler(0x800f,1,1,0,0,0,0)
                                    # Rate over XFI 10GBASE-R
                                    self.GetCommandHandler(0x8017,1,0,0,0,0,0)
                                    #set direction to BaseT side			
                                    HostOrBaseTDirection(1)
                                    #clear low power mode
                                    reg_value = driver.read_phy_register(1, 0, self.Phy_Address_dict[driver.port_number()])
                                    reg_value = reg_value & 0xF7FF
                                    driver.write_phy_register(1, 0, self.Phy_Address_dict[driver.port_number()], reg_value)
                                    #Set 10G
                                    Adv10GLinkSpeed(False)				
                                    #clear 5G
                                    Adv5GLinkSpeed(False)
                                    #clear 2.5G
                                    Adv2p5GLinkSpeed(True)		
                                    #clear 1G
                                    Adv1GLinkSpeed(False)
                                    #clear 100M
                                    reg_value = driver.read_phy_register(7, 0x10, self.Phy_Address_dict[driver.port_number()])
                                    reg_value = reg_value & 0xF07F
                                    driver.write_phy_register(7, 0x10, self.Phy_Address_dict[driver.port_number()], reg_value)
                                    #set pause enable
                                    self.GetCommandHandler(0x8020,1,1,0,0,0,0)
                                    #Restart AN
                                    reg_value = driver.read_phy_register(7, 0, self.Phy_Address_dict[driver.port_number()])
                                    reg_value = reg_value | 0x1200
                                    driver.write_phy_register(7, 0, self.Phy_Address_dict[driver.port_number()], reg_value)
                                    #################################################################################### SFI PORTS THROUGHPUT
                                    reg_addr = calculate_port_offset(0x001C0980, 0x4, driver.port_number())
                                    temp = driver.read_csr(reg_addr)
                                    temp = temp | 0xFF
                                    driver.write_csr(reg_addr, temp)
                                    ####################################################################################

                    elif interface == 'KX':
                            if speed != '1G':
                                    print "Wrong speed insertion"
                                    raise RuntimeError("Wrong speed insertion")
                            reg_addr = calculate_port_offset(0x8CE00, 0x4, driver.port_number())
                            temp = driver.read_csr(reg_addr)
                            temp = temp & 0xFFFFEFFF
                            driver.write_csr(reg_addr, temp)
                            reg_addr = calculate_port_offset(0x8C260, 0x4, driver.port_number())
                            driver.write_csr(reg_addr, 0xA5018070)
                            #set KR mode enable on Orca host side
                            self.GetCommandHandler(0x800F,1,1,0,0,0,0)				
                            #set direction to BaseT side			
                            HostOrBaseTDirection(1)
                            #clear low power mode
                            reg_value = driver.read_phy_register(1, 0, self.Phy_Address_dict[driver.port_number()])
                            reg_value = reg_value & 0xF7FF
                            driver.write_phy_register(1, 0, self.Phy_Address_dict[driver.port_number()], reg_value)
                            #Set 10G
                            Adv10GLinkSpeed(False)
                            #clear 5G
                            Adv5GLinkSpeed(False)
                            #clear 2.5G
                            Adv2p5GLinkSpeed(False)		
                            #Set 1G
                            Adv1GLinkSpeed(True)
                            #clear 100M
                            reg_value = driver.read_phy_register(7, 0x10, self.Phy_Address_dict[driver.port_number()])
                            reg_value = reg_value & 0xF07F
                            driver.write_phy_register(7, 0x10, self.Phy_Address_dict[driver.port_number()], reg_value)			
                            #set pause disable
                            self.GetCommandHandler(0x8020,1,0,0,0,0,0)
                            #Restart AN
                            reg_value = driver.read_phy_register(7, 0, self.Phy_Address_dict[driver.port_number()])
                            reg_value = reg_value | 0x1200
                            driver.write_phy_register(7, 0, self.Phy_Address_dict[driver.port_number()], reg_value)
                            #################################################################################### SFI PORTS THROUGHPUT
                            reg_addr = calculate_port_offset(0x001C0980, 0x4, driver.port_number())
                            temp = driver.read_csr(reg_addr)
                            temp = temp & 0xFFFFFF00
                            driver.write_csr(reg_addr, temp)
                            ####################################################################################
                    # need to verify all force mode SFI and SGMII		
                    elif interface == 'SFI':
                            if speed != '2.5G' and speed != '5G' and speed != '10G':
                                    print "Wrong speed insertion"
                                    raise RuntimeError("Wrong speed insertion")
                            if speed == '10G':
                                    # FVL Tamar powerup
                                    reg_addr = calculate_port_offset(0x8CE00, 0x4, driver.port_number())
                                    temp = driver.read_csr(reg_addr)
                                    temp = temp & 0xFFFFEFFF
                                    driver.write_csr(reg_addr, temp)
                                    reg_addr = calculate_port_offset(0x8C260, 0x4, driver.port_number())
                                    driver.write_csr(reg_addr, 0x80000438)
                                    #set KR mode disable on Orca host side
                                    self.GetCommandHandler(0x800f,1,0,0,0,0,0)
                                    #set direction to BaseT side			
                                    HostOrBaseTDirection(1)
                                    #clear low power mode
                                    reg_value = driver.read_phy_register(1, 0, self.Phy_Address_dict[driver.port_number()])
                                    reg_value = reg_value & 0xF7FF
                                    driver.write_phy_register(1, 0, self.Phy_Address_dict[driver.port_number()], reg_value)
                                    #Set 10G
                                    Adv10GLinkSpeed(True)				
                                    #clear 5G
                                    Adv5GLinkSpeed(False)
                                    #clear 2.5G
                                    Adv2p5GLinkSpeed(False)		
                                    #clear 1G
                                    Adv1GLinkSpeed(False)
                                    #clear 100M
                                    reg_value = driver.read_phy_register(7, 0x10, self.Phy_Address_dict[driver.port_number()])
                                    reg_value = reg_value & 0xF07F
                                    driver.write_phy_register(7, 0x10, self.Phy_Address_dict[driver.port_number()], reg_value)
                                    #set pause disable
                                    self.GetCommandHandler(0x8020,1,0,0,0,0,0)
                                    #Restart ANreg_addr
                                    reg_value = driver.read_phy_register(7, 0, self.Phy_Address_dict[driver.port_number()])
                                    reg_value = reg_value | 0x1200
                                    driver.write_phy_register(7, 0, self.Phy_Address_dict[driver.port_number()], reg_value)
                            if speed == '5G':
                                    # FVL Tamar powerup
                                    reg_addr = calculate_port_offset(0x8CE00, 0x4, driver.port_number())
                                    temp = driver.read_csr(reg_addr)
                                    temp = temp & 0xFFFFEFFF
                                    driver.write_csr(reg_addr, temp)
                                    reg_addr = calculate_port_offset(0x8C260, 0x4, driver.port_number())
                                    driver.write_csr(reg_addr, 0x80000438)
                                    #set Pause and Pace Register
                                    reg_addr = calculate_port_offset(0x1E2040, 0x4, driver.port_number())
                                    temp = driver.read_csr(reg_addr)
                                    temp = temp | 0x50000
                                    driver.write_csr(reg_addr, temp)
                                    #set KR mode disable on Orca host side
                                    self.GetCommandHandler(0x800f,1,0,0,0,0,0)
                                    # Rate over XFI 10GBASE-R
                                    self.GetCommandHandler(0x8017,1,0,0,0,0,0)
                                    #set direction to BaseT side			
                                    HostOrBaseTDirection(1)
                                    #clear low power mode
                                    reg_value = driver.read_phy_register(1, 0, self.Phy_Address_dict[driver.port_number()])
                                    reg_value = reg_value & 0xF7FF
                                    driver.write_phy_register(1, 0, self.Phy_Address_dict[driver.port_number()], reg_value)
                                    #Set 10G
                                    Adv10GLinkSpeed(False)				
                                    #clear 5G
                                    Adv5GLinkSpeed(True)
                                    #clear 2.5G
                                    Adv2p5GLinkSpeed(False)		
                                    #clear 1G
                                    Adv1GLinkSpeed(False)
                                    #clear 100M
                                    reg_value = driver.read_phy_register(7, 0x10, self.Phy_Address_dict[driver.port_number()])
                                    reg_value = reg_value & 0xF07F
                                    driver.write_phy_register(7, 0x10, self.Phy_Address_dict[driver.port_number()], reg_value)
                                    #set pause disable
                                    self.GetCommandHandler(0x8020,1,0,0,0,0,0)
                                    #Restart AN
                                    reg_value = driver.read_phy_register(7, 0, self.Phy_Address_dict[driver.port_number()])
                                    reg_value = reg_value | 0x1200
                                    driver.write_phy_register(7, 0, self.Phy_Address_dict[driver.port_number()], reg_value)
                            if speed == '2.5G':
                                    # FVL Tamar powerup
                                    reg_addr = calculate_port_offset(0x8CE00, 0x4, driver.port_number())
                                    temp = driver.read_csr(reg_addr)
                                    temp = temp & 0xFFFFEFFF
                                    driver.write_csr(reg_addr, temp)
                                    reg_addr = calculate_port_offset(0x8C260, 0x4, driver.port_number())
                                    driver.write_csr(reg_addr, 0x80000438)
                                    #set Pause and Pace Register
                                    reg_addr = calculate_port_offset(0x1E2040, 0x4, driver.port_number())
                                    temp = driver.read_csr(reg_addr)
                                    temp = temp | 0x30000
                                    driver.write_csr(reg_addr, temp)
                                    #set LFC
                                    reg_addr = calculate_port_offset(0x1E2400, 0x4, driver.port_number())
                                    temp = driver.read_csr(reg_addr)
                                    temp = temp | 0x8 # set RFCE
                                    temp = temp & 0xFFFB # clear RPFCM
                                    driver.write_csr(reg_addr, temp)
                                    #set KR mode disable on Orca host side
                                    self.GetCommandHandler(0x800f,1,0,0,0,0,0)
                                    # Rate over XFI 10GBASE-R
                                    self.GetCommandHandler(0x8017,1,0,0,0,0,0)
                                    #set direction to BaseT side			
                                    HostOrBaseTDirection(1)
                                    #clear low power mode
                                    reg_value = driver.read_phy_register(1, 0, self.Phy_Address_dict[driver.port_number()])
                                    reg_value = reg_value & 0xF7FF
                                    driver.write_phy_register(1, 0, self.Phy_Address_dict[driver.port_number()], reg_value)
                                    #Set 10G
                                    Adv10GLinkSpeed(False)				
                                    #clear 5G
                                    Adv5GLinkSpeed(False)
                                    #clear 2.5G
                                    Adv2p5GLinkSpeed(True)		
                                    #clear 1G
                                    Adv1GLinkSpeed(False)
                                    #clear 100M
                                    reg_value = driver.read_phy_register(7, 0x10, self.Phy_Address_dict[driver.port_number()])
                                    reg_value = reg_value & 0xF07F
                                    driver.write_phy_register(7, 0x10, self.Phy_Address_dict[driver.port_number()], reg_value)
                                    #set pause enable
                                    self.GetCommandHandler(0x8020,1,1,0,0,0,0)
                                    #Restart AN
                                    reg_value = driver.read_phy_register(7, 0, self.Phy_Address_dict[driver.port_number()])
                                    reg_value = reg_value | 0x1200
                                    driver.write_phy_register(7, 0, self.Phy_Address_dict[driver.port_number()], reg_value)
                    elif interface == 'SGMII':
                            if speed != '1G' and speed != '100M':
                                    print "Wrong speed insertion"
                                    raise RuntimeError("Wrong speed insertion")
                            if speed == '100M':
                                    reg_addr = calculate_port_offset(0x8CE00, 0x4, driver.port_number())
                                    driver.write_csr(reg_addr, 0x00001000)
                                    driver.write_csr(0x8C260, 0x80003138)
                                    #set KR mode disable on Orca host side
                                    self.GetCommandHandler(0x800f,1,0,0,0,0,0)
                                    #set direction to BaseT side			
                                    HostOrBaseTDirection(1)
                                    #clear low power mode
                                    reg_value = driver.read_phy_register(1, 0, self.Phy_Address_dict[driver.port_number()])
                                    reg_value = reg_value & 0xF7FF
                                    driver.write_phy_register(1, 0, self.Phy_Address_dict[driver.port_number()], reg_value)
                                    #Set 100M
                                    reg_value = driver.read_phy_register(7, 0x10, self.Phy_Address_dict[driver.port_number()])
                                    reg_value = reg_value & 0xF07F
                                    reg_value = reg_value | 0x100
                                    driver.write_phy_register(7, 0x10, self.Phy_Address_dict[driver.port_number()], reg_value)
                                    #clear 1G
                                    Adv1GLinkSpeed(False)
                                    #clear 10G
                                    Adv10GLinkSpeed(False)
                                    #clear 5G
                                    Adv5GLinkSpeed(False)
                                    #clear 2.5G
                                    Adv2p5GLinkSpeed(False)			
                                    #set pause disable
                                    self.GetCommandHandler(0x8020,1,0,0,0,0,0)
                                    #Restart AN
                                    reg_value = driver.read_phy_register(7, 0, self.Phy_Address_dict[driver.port_number()])
                                    reg_value = reg_value | 0x1200
                                    driver.write_phy_register(7, 0, self.Phy_Address_dict[driver.port_number()], reg_value)
                                    #################################################################################### SFI PORTS THROUGHPUT
                                    reg_addr = calculate_port_offset(0x001C0980, 0x4, driver.port_number())
                                    temp = driver.read_csr(reg_addr)
                                    temp = temp & 0xFFFFFF00
                                    driver.write_csr(reg_addr, temp)
                                    ####################################################################################
            except Exception as e:
                    print "Exception in fvl_eth:SetForceLinkSpeed proclib Error: " + str(e)
                    print
                    raise RuntimeError("Exception in fvl_eth:SetForceLinkSpeed proclib Error")	

    def EthStartTraffic(self, packet_size = 512, number_of_packets = None):
            '''
                This function starts Tx and Rx.
                Default packet size is 512
            '''
            self.driver.start_rx()
            self.driver.start_tx(packet_size = packet_size, number_of_packets=number_of_packets)

    def EthStartRx(self):
            '''
                This function starts Tx and Rx.
                Default packet size is 512
            '''

            self.driver.start_rx()

    def EthStartTx(self, packet_size = 512, number_of_packets = None):
            '''
                This function starts Tx and Rx.
                Default packet size is 512
            '''
        if number_of_packets:
            self.driver.start_tx(packet_size=packet_size, number_of_packets=number_of_packets, tx_limit_type='PACKET_COUNT')
        else: 
            self.driver.start_tx(packet_size=packet_size)

    ###############################################################

    def GetCurrentThroughput(self, packet_size = 512):
            '''This function returns current Throughput 
                    Default packet size is 512''' 
            start_PTC = self.GetPTC()
            start_time = time.time()
            time.sleep(3)
            end_PTC = self.GetPTC()
            return int((end_PTC['TotalPTC'] - start_PTC['TotalPTC'])*8*packet_size/(time.time() - start_time))
            
    def GetThroughput(self, start,end,sample_time,packet_size = 512):
            '''
            This function returns current Throughput 
                    Default packet size is 512''' 

            return int((end - start)*8*packet_size/sample_time)

    ################################################################
    def EthStopRx(self, ring_id=0):
            '''This function stops Tx and Rx.
            '''
            self.driver.stop_rx(ring_id=ring_id)

    def EthStopTx(self, ring_id=0):
            '''This function stops Tx and Rx.
            '''
            self.driver.stop_tx(ring_id=ring_id)

    def EthStopTraffic(self):
            '''This function stops Tx and Rx.
            '''
            self.driver.stop_tx()
            time.sleep(2)
            self.driver.stop_rx()

    def EthGetTrafficStatistics(self):
            '''This function reads traffic statistic
                    and saves results to list and returns
                    it.
                    [WIP] - add additional registers values

            '''
            result = []
            result.append(ut.get_current_date_string())
            result.append(GetPTC1522())
            result.append(GetPRC1522())

            return result

    def GetInternalPcsLinkStatus(self):
            '''RETURN:1-Link is up and there was no link down since last time this register was read (We need to call this function two times to know the current status. 0- Link is/was down (12.2.2.4.81)
                    PCS_LINK_STATUS2 = 0x0008c220
            ''' 
            driver = self.driver
            reg_addr = calculate_port_offset(0x0008c220, 0x4, driver.port_number())
            reg_data = driver.read_csr(reg_addr)
            reg_data = driver.read_csr(reg_addr)
            return get_bit_value(reg_data, 7)

    def Get_Port_Type(self):
            '''this function return port type KR/BaseT
                    argument: 
                    Return: BaseT or KR port type 
            '''
            driver = self.driver
            port = driver.port_number()
            if port == 0:
                    return "BaseT"
            elif port == 2:
                    return "BaseT"
            elif port == 1:
                    return "KR"
            elif port == 3:
                    return "KR"
            else:
                    return "wrong port number"

    def MacRemoteFault(self):
            '''this function return the MAC RX LINK FAULT RF (remote fault)
            '''
            driver = self.driver
            reg_addr = calculate_port_offset(0x001E2420, 0x4, driver.port_number())
            reg_data = driver.read_csr(reg_addr)
            return get_bit_value(reg_data, 2)

    def MacLocalFault(self):
            '''this function return the MAC RX LINK FAULT LF (local fault)
            '''
            driver = self.driver
            reg_addr = calculate_port_offset(0x001E2420, 0x4, driver.port_number())
            reg_data = driver.read_csr(reg_addr)
            return get_bit_value(reg_data, 3)

    def GetFVL_FW_Version(self):
            '''This function returns FVL firmware version
            '''
            driver = self.driver
            aq_desc = AqDescriptor()
            aq_desc.opcode = 0x0001
            #aq_desc.param1 = 0x8c260
            #aq_desc.flags = 0x0200
            
            driver.send_aq_command(aq_desc)

            FW_Version_Dict = {}
            FW_Version_Dict['FW_ROM_Build_ID'] = hex(aq_desc.param0)
            FW_Version_Dict['FW_Build_ID'] = hex(aq_desc.param1)
            FW_Version_Dict['FW_Major_Minor_Version'] = hex(aq_desc.addr_high)
            FW_Version_Dict['FW_API_Major_Miner_Version'] = hex(aq_desc.addr_low)
            return FW_Version_Dict

    def GetEye(self):
            '''this function return Eye value
            '''
            driver = self.driver
            #port = driver.port_number()
            return GetETH_Internal_ehm12(self.Phy_Address_dict[driver.port_number()]*4)
            
    def GetETH_Internal_ehm12(self, lane):
            '''this function return the Internal EHM12 base-address
            '''
            address = 0x0630
            PMD_address = address + (lane << 12)
            ehm12_read = Read_ana_reg(PMD_address)
            if ehm12_read < 0 or ehm12_read > 100:
                    ehm12_read =  Read_ana_reg(PMD_address)
            return ehm12_read

    def DisableIdleDetector(self):
            Write_ana_reg(0x905c,0xc8e672)

    def Write_ana_reg(self, address,data):
            ''' This function write read analog register content
            '''	
            driver = self.driver
            driver.write_csr(0xa4038,address)
            driver.write_csr(0xa403c,data)	
            
    def Read_ana_reg(self, address):
            ''' This function returns read analog register content
            '''
            driver = self.driver
            driver.write_csr(0xa4038,address)
            return driver.read_csr(0xa403c)
            
    def	GetPCIE_CurrentLinkSpeed(self):
            '''This function returns PCIE link speed: 
            "Gen1 = 2.5G, Gen2 = 5G, Gen3 = 8G"'''
            val = _get_bits_slice_value(_get_val_addr_pcie(0xB0),16,19)
            
            link_speed = {
                    1: "Gen1",
                    2: "Gen2",
                    3: "Gen3",
            }
            
            return link_speed.get(val,"Wrong")

            
    def GetPCIE_CurrentLinkWidth(self):
            '''This function returns PCIE link width
            '''
            val = _get_bits_slice_value(_get_val_addr_pcie(0xB0),20,23)
            
            link_width = {
                    0: "Reserved",
                    1: "x1",
                    2: "x2",
                    4: "x4",
                    8: "x8",
            }
            
            return link_width.get(val,"Wrong")
            
    def _get_val_addr_pcie(self, address):
            ''' This function returns PCIE value by input address
            '''
            driver = self.driver
            return driver.read_pci(address)
            
            #FVL ULT
    # FAB_SITE 1:0 0x0 RO UNDEFINED Fab Site. Can be one of four possible sites.
    # TEST_YEAR_LSB 5:2 0x0 RO UNDEFINED
            # Least significant decimal digit of the production
            # year. Possible values are 0 to 9. Production year
            # can be 2000 up to 2009; 2010 up to 2019 and so
            # on.
    # TEST_FAB_WORK_WEEK 11:6 0x0 RO UNDEFINED Production work week: 000001b = WW01 ... 110101b = WW53.
    # X_SIGN1 12 0b RO UNDEFINED X Location Sign.
            # 0b = Positive.
            # 1b = Negative.
    # X_LOCATION 18:13 0x0 RO UNDEFINED X Location From 0 to 63.
    # X_SIGN2 19 0b RO UNDEFINED Y Location Sign.
            # 0b = Positive.
            # 1b = Negative.
    # Y_LOCATION 25:20 0x0 RO UNDEFINED Y Location Sign.
            # 0b = Positive.
            # 1b = Negative
    # WAFER 30:26 0x0 RO UNDEFINED Wafer index can be from 1 to 25.
    # LOT_NUMBER_MSB 31 0b RO UNDEFINED Most significant bit of the lot number. The LS bits
    # LOT_NUMBER_LSB 24:0 0x0 RO UNDEFINED Least significant bits of the lot number. The MS bit is in ULT0.
    # RESERVED 30:25 0x0 RSV Reserved.
    # PARITY 31 0b RO UNDEFINED Even parity of the fuses.	

    def Get_FVL_ULT(self):
            '''This function returns FVL ULT value
            '''
            driver = self.driver
            ult0 = driver.read_csr(0x00094000)
            ult1 = driver.read_csr(0x00094004)
            print "ult0 register (0x00094000) value is: ",hex(ult0)
            print "ult1 register (0x00094004) value is: ",hex(ult1)
            ult = (((ult1 & 0xffffffff) <<32) | ult0)
            ULT_Dict = {}
            bits = _get_bits_slice_value(ult,62,63)
            if bits == 0: FAB_SITE = "N"
            elif bits == 1: FAB_SITE = "P"
            elif bits == 2: FAB_SITE = "T"
            else: FAB_SITE = "Invalid FAB value '"+str(bits)+"' !"
            TEST_YEAR = int(_get_bits_slice_value(ult,58,61))
            TEST_FAB_WORK_WEEK = int(_get_bits_slice_value(ult,52,57))
            X_LOCATION = int(_get_bits_slice_value(ult,45,50))
            if get_bit_value(ult, 51) == 1:
                    X_LOCATION = - X_LOCATION
            Y_LOCATION = int(_get_bits_slice_value(ult,38,43))
            if get_bit_value(ult, 44) == 1:
                    Y_LOCATION = - Y_LOCATION
            WAFER = int(_get_bits_slice_value(ult,33,37))
            LOT = _get_bits_slice_value(ult,7,32) 
            LOT_AlphaNumeric = int_to_base36(LOT) #### Integer to AlphaNumeric convertion (base 36)
            PARITY = int(get_bit_value(ult,1))
            ULT_Dict["FAB_SITE"] = FAB_SITE
            ULT_Dict["TEST_YEAR"] = TEST_YEAR
            ULT_Dict["TEST_FAB_WORK_WEEK"] = 'ww' + str(TEST_FAB_WORK_WEEK)
            ULT_Dict["X_LOCATION"] =  X_LOCATION
            ULT_Dict["Y_LOCATION"] =  Y_LOCATION
            ULT_Dict["WAFER"] =  WAFER
            ULT_Dict["LOT_NUMBER"] = LOT_AlphaNumeric
            ULT_Dict["PARITY"] =  PARITY
            return ULT_Dict

    def int_to_base36(self, num):
        """Converts a positive integer into a base36 string."""
        assert num >= 0
        digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        res = ''
        while not res or num > 0:
            num, i = divmod(num, 36)
            res = digits[i] + res
        return res


    #########################################################################################################
    ######################                 ORCA                 #############################################
    #########################################################################################################
            
    def GetPhyLinkStatus(self):
            '''this function return the PHY_LINK_UP status.
            '''
            HostOrBaseTDirection(1)
            driver = self.driver
            reg_value = driver.read_phy_register(0x7, 1, self.Phy_Address_dict[driver.port_number()])
            reg_value = driver.read_phy_register(0x7, 1, self.Phy_Address_dict[driver.port_number()])
            link_status = get_bit_value(reg_value, 2)
            return link_status

    def GetPhyHostInterLinkStatus(self):
            '''this function return the HOST PHY_LINK_UP status.
            '''
            HostOrBaseTDirection(0)
            driver = self.driver
            reg_value = driver.read_phy_register(0x3, 1, self.Phy_Address_dict[driver.port_number()])
            reg_value = driver.read_phy_register(0x3, 1, self.Phy_Address_dict[driver.port_number()])
            link_status = get_bit_value(reg_value, 2)
            return link_status	

    def GetPhyLinkSpeed(self):
            '''this function return EXT_Phy_LINK_SPEED status
            '''
            HostOrBaseTDirection(1)
            driver = self.driver
            reg_value = driver.read_phy_register(0x1E, 0x400D, self.Phy_Address_dict[driver.port_number()])
            #print hex(reg_value)
            link_speed = _get_bits_slice_value(reg_value, 2, 4)
            return link_speed

    def GetAN_CompleteOrca_BaseT_side(self):
            '''This function return AN_Complete Orca BaseT side'''
            HostOrBaseTDirection(1)
            driver = self.driver
            reg_value = driver.read_phy_register(0x7, 0x1, self.Phy_Address_dict[driver.port_number()])
            GetAutonegComplete = get_bit_value(reg_value,5)
            return GetAutonegComplete

    def GetAN_CompleteOrca_KR_side(self):
            '''This function return AN_Complete Orca KR side'''
            HostOrBaseTDirection(0)
            driver = self.driver
            reg_value = driver.read_phy_register(0x7, 0x1, self.Phy_Address_dict[driver.port_number()])
            GetAutonegComplete = get_bit_value(reg_value,5)
            return GetAutonegComplete

    def Get_MS_Status(self):
            '''this function return the master slave configuration resulation
                    argument: None
                    return:
                            1 = local PHY resolved to Master
                            0 = local PHY resGetCurrentTemperature()olved to Slave				 
            '''
            HostOrBaseTDirection(1)
            driver = self.driver
            reg_value = driver.read_phy_register(0x7, 0x21, self.Phy_Address_dict[driver.port_number()])
            #print hex(reg_value)
            MS_configuration = get_bit_value(reg_value, 14)
            return 	MS_configuration

    def Set_MS_Config(self, MS):
            '''this function config the master slave resulation
                    argument: True = config PHY as Master
                                      False = config PHY as Slave
            '''
            HostOrBaseTDirection(1)
            reg_value = self.driver.read_phy_register(0x7, 0x20, self.Phy_Address_dict[self.driver.port_number()])
            reg_value = reg_value | (1<<15)	
            if (MS==True):
                    reg_value = reg_value |(1<<14)
            else:
                    reg_value = reg_value & (~(1<<14))

            self.driver.write_phy_register(0x7, 0x20, self.Phy_Address_dict[self.driver.port_number()], reg_value)	
            RestartAn()	

    def Adv10GLinkSpeed(self, State):
            '''this function advertise Phy 10G link speed
                    argument: True/False 
            '''
            if (State):
                    SetMdioBit(0x7,0x20,12)
            else:
                    ClearMdioBit(0x7,0x20,12)

    def Adv5GLinkSpeed(self, State):
            '''this function advertise Phy 10G link speed
                    argument: True/FalseGetCurrentTemperature() 
            '''
            if (State):
                    SetMdioBit(0x7,0x20,8)
            else:
                    ClearMdioBit(0x7,0x20,8)

    def Adv2p5GLinkSpeed(self, State):
            '''this function advertise Phy 10G link speed
                    argument: True/False 
            '''
            if (State):
                    SetMdioBit(0x7,0x20,7)
            else:
                    ClearMdioBit(0x7,0x20,7)

    def Adv1GLinkSpeed(self, State):
            '''this function advertise Phy 10G link speed
                    argument: True/False 
            '''
            if (State):
                    SetMdioBit(0x7,0xFFE9,9)
                    ClearMdioBit(0x7,0xFFE9,8)#clear half duplaex
            else:
                    ClearMdioBit(0x7,0xFFE9,9)
                    ClearMdioBit(0x7,0xFFE9,8)

    def SetExtPhyLinkSpeed(self, Speed):
            '''this function set link speed on Phy
                    argument: Link speed in str for exmp: 100M,1G,2.5G,5G,10G 
            '''
            HostOrBaseTDirection(1)
            if Speed == "10G":
                    Adv10GLinkSpeed(True)
                    Adv5GLinkSpeed(True)
                    Adv2p5GLinkSpeed(True)
                    Adv1GLinkSpeed(True)
            elif Speed == "5G":
                    Adv10GLinkSpeed(False)
                    Adv5GLinkSpeed(True)
                    Adv2p5GLinkSpeed(True)
                    Adv1GLinkSpeed(True)
            elif Speed == "2.5G":
                    Adv10GLinkSpeed(False)
                    Adv5GLinkSpeed(False)
                    Adv2p5GLinkSpeed(True)
                    Adv1GLinkSpeed(True)
            elif Speed == "1G":
                    Adv10GLinkSpeed(False)
                    Adv5GLinkSpeed(False)
                    Adv2p5GLinkSpeed(False)
                    Adv1GLinkSpeed(True)
            elif Speed == "100M":
                    Adv10GLinkSpeed(False)
                    Adv5GLinkSpeed(False)
                    Adv2p5GLinkSpeed(False)
                    Adv1GLinkSpeed(False)
            else:
                    raise RuntimeError("SetExtPhyLinkSpeed: speed not valid")

            RestartAn()

    def GetCurrentTemperature(self):
            '''this function return current teperature for BCM PHY
                    argument: None
                    return: temperature in [C]
            '''
            DataRegList = self.GetCommandHandler(0x8031,0,0,0,0,0,0)
            if DataRegList[0]:
                    print "ERROR to read temperature"
                    return 0xffff
            return DataRegList[1]

    def GetSnr(self):
            '''this function return SNR value for BCM PHY
                    argument: None
                    return: DataRegValue[2] SNR for channel A in db
                                    DataRegValue[3] SNR for channel B in db
                                    DataRegValue[4] SNR for channel C in db
                                    DataRegValue[5] SNR for channel D in db

            '''
            DataRegList = self.GetCommandHandler(0x8030,1,0,0,0,0,0)
            if DataRegList[0]:
                    print "ERROR to read SNR"
                    return 0xffff
            for i in range(2,len(DataRegList)):
                    DataRegList[i] /= 10.0
            return DataRegList[2:]
            
    def PHY_FW_Version(self):
            '''this function return FW version for BCM phy
                    argument: None
                    return: FW_version[0] is Firmware version: Branch
                                    FW_version[1] is Firmware version: Main
                                    FW_version[2] is Firmware version: Build
            '''
            driver = self.driver	
            reg_value = driver.read_phy_register(0x30, 0x400F, self.Phy_Address_dict[driver.port_number()])
            FW_version = []	
            FW_version.append(_get_bits_slice_value(reg_value, 0, 6))
            FW_version.append(_get_bits_slice_value(reg_value, 7, 11))
            FW_version.append(_get_bits_slice_value(reg_value, 12, 15))
            return FW_version
            print FW_version

    def PMAFault(self):
            '''this function return PMA/PMD fault status
                    argument: None
                    return: 1 - if fault condition detected
                                    0 - if fault condition is not detected
            '''
            driver = self.driver
            reg_value = driver.read_phy_register(0x1, 0x0001, self.Phy_Address_dict[driver.port_number()])
            PMAFault = get_bit_value(reg_value, 7)
            return PMAFault

    def GetPMDReceiveLinkStatus():
            '''this function return PMA/PMD Orca line Receive link status
                    argument: None
                    return: 1 - PMD link is good
                                    0 - PMD link is down
            '''
            HostOrBaseTDirection(1)
            driver = self.driver
            reg_value = driver.read_phy_register(0x1, 0x0001, self.Phy_Address_dict[driver.port_number()])
            PMDReceiveLinkStatus = get_bit_value(reg_value, 2)
            return PMDReceiveLinkStatus

    def PCSFault(self):
            '''this function return PCS fault status
                    argument: None
                    return: 1 - if fault condition detected
                                    0 - if fault condition is not detected
            '''
            driver = self.driver
            reg_value = driver.read_phy_register(0x3, 0x0001, self.Phy_Address_dict[driver.port_number()])
            PCSFault = get_bit_value(reg_value, 7)
            return PCSFault

    def GetPCSReceiveLinkStatus(self):
            '''this function return PCS Orca line receive link status
                    argument: None
                    return: 1 - PCS link is good
                                    0 - PCS link is down
            '''
            HostOrBaseTDirection(1)
            driver = self.driver
            reg_value = driver.read_phy_register(0x3, 0x0001, self.Phy_Address_dict[driver.port_number()])
            PCSReceiveLinkStatus = get_bit_value(reg_value, 2)
            return PCSReceiveLinkStatus

    def ConfigDirection(self, direction):

            driver = self.driver
            Phy_Address = self.Phy_Address_dict[driver.port_number()]
            if direction:		
                    driver.write_phy_register(0x1E, 0x4110, Phy_Address,0x0001)
                    driver.write_phy_register(0x1E, 0x4111, Phy_Address,0x0001)
                    driver.write_phy_register(0x1E, 0x4113, Phy_Address,0x1002)
            else:
                    driver.write_phy_register(0x1E, 0x4110, Phy_Address,0x2004)
                    driver.write_phy_register(0x1E, 0x4111, Phy_Address,0x2004)
                    driver.write_phy_register(0x1E, 0x4113, Phy_Address,0x2004)	
            
    def HostOrBaseTDirection(self, direction):
            '''this function set the direction to Host interface or BaseT side.
                    in BCM DS the Host and Line(BaseT) are the same MMD 1,3,7
                    to read/write from the side need to set few commande that define in BCM84888 DS Register Maps
                    argument: 1 -> BaseT
                                      0 -> Host interface

            '''	
            handler = get_handler()
                    
            if not 'HostOrBaseTDirection' in handler.custom_data:
                    handler.custom_data['HostOrBaseTDirection'] = direction
                    ConfigDirection(direction)
                    return None
            
            if direction == handler.custom_data['HostOrBaseTDirection']:
                    return None

            ConfigDirection(direction)	

            handler.custom_data['HostOrBaseTDirection'] = direction	

    def SetOrcaMonitorEnable(self, direction = 1):
            ''' argument : 1-> Monitoring Received packet from line side interface
                            0-> Monitoring Received packet from SerDes interface'''
            driver = self.driver
            if direction == 0:
                    driver.write_phy_register(0x1, 0xB980, driver.port_number(),0x0081)
                    driver.write_phy_register(0x1, 0xB982, driver.port_number(),0x800F)
                    driver.write_phy_register(0x1, 0xB984, driver.port_number(),0x0006)		
                    
            elif direction == 1:
                    driver.write_phy_register(0x1, 0xB980, driver.port_number(),0x0081)
                    driver.write_phy_register(0x1, 0xB982, driver.port_number(),0x800F)
                    driver.write_phy_register(0x1, 0xB984, driver.port_number(),0x0004)
            ''' Make a looop from the test'''
            ''' write-> tx-> read'''

    def ReadOrcaMonitor(self):
            ''' This function returns Packet and Error counters of ORCA received Monitoring packets'''

            driver = self.driver
            d = {}
            driver.write_phy_register(0x1,0xB98C,driver.port_number(),0x0002) #latching counter
            driver.write_phy_register(0x1,0xB98C,driver.port_number(),0x0000) #latching counter

            low_pack = driver.read_phy_register(0x1, 0xB99F, driver.port_number())
            high_pack = driver.read_phy_register(0x1, 0xB9A0, driver.port_number())
            pack_count = (((high_pack & 0xffff) <<32) | low_pack)


            low_error = driver.read_phy_register(0x1, 0xB9A1, driver.port_number()) 
            high_error = driver.read_phy_register(0x1, 0xB9A2, driver.port_number())
            error_count = (((high_error & 0xffff) <<32) | low_error)

            d = {'error_count':error_count,'pack_count':pack_count}
            return d  
            



    def SetMdioBit(self, Page,Register,BitNum):
            
            driver = self.driver
            reg_value = driver.read_phy_register(Page, Register, self.Phy_Address_dict[driver.port_number()])
            #print hex(reg_value)
            reg_value = reg_value | (1 << BitNum)
            #print hex(reg_value)
            driver.write_phy_register(Page, Register, self.Phy_Address_dict[driver.port_number()], reg_value)

    def ClearMdioBit(self, Page,Register,BitNum):
            
            driver = self.driver
            reg_value = driver.read_phy_register(Page, Register, self.Phy_Address_dict[driver.port_number()])
            #print hex(reg_value)	
            reg_value = reg_value & ~(1 << BitNum)
            #print hex(reg_value)
            driver.write_phy_register(Page, Register, self.Phy_Address_dict[driver.port_number()], reg_value)

    def GetIEEE_FastRetrain_TX_RX_Count():
            driver = self.driver
            reg_value = driver.read_phy_register(0x1,0x0093,self.Phy_Address_dict[driver.port_number()])
            FR_RX_TX_CNT = {}
            FR_RX_TX_CNT['RX'] = _get_bits_slice_value(reg_value,11,15)
            FR_RX_TX_CNT['TX'] = _get_bits_slice_value(reg_value,6,10)
            return FR_RX_TX_CNT
            
    ###############################################################################################
    ############# command handler section  								 ##########################
    ############# definition BCM84888 DS "MDIO COMMAND HANDLER FUNCTION" ##########################

    def GetCommandHandler(self, opcode,SetOrGetFlag,Data1Reg,Data2Reg,Data3Reg,Data4Reg,Data5Reg):
            '''this function will execute command handler in BCM Phy
                    argument: opcode -> oopcode to execute
                                      SetOrGetFlag -> 1 for write (set)
                                                                      0 for read (get)
                                      Data*Reg -> for opcode that need inputs
                    return: list
                                            list[0] -> 0 for execute command pass, 1 for error
                                            list[1] -> Data1Reg return value
                                            list[2] -> Data2Reg return value
                                            list[3] -> Data3Reg return value
                                            list[4] -> Data4Reg return value
                                            list[5] -> Data5Reg return value
            '''
            # polling until the FW will be free to execute
            # timout 2 sec
            ErrorFlag = False
            TimeOutCount = 0
            while (TimeOutCount < 20):
                    val1,val2 = self.GetCommandHandlerStatus(1)
                    if not val1:
                            break
                    time.sleep(0.1)
                    TimeOutCount += 1
            # for error condition
            if (TimeOutCount > 20):
                    ErrorFlag = True


            if (SetOrGetFlag):
                    # TODO add write to data registers
                    SetGetDataReg(1,Data1Reg,Data2Reg,Data3Reg,Data4Reg,Data5Reg)

            # write opcode
            driver = self.driver
            driver.write_phy_register(0x1E, 0x4005, self.Phy_Address_dict[driver.port_number()], opcode)

            # polling until the FW will be free to execute
            # timout 2 sec
            TimeOutCount = 0
            while (TimeOutCount < 20):
                    val1,val2 = self.GetCommandHandlerStatus(0)
                    if not val1:
                            break
                    time.sleep(0.1)
                    TimeOutCount += 1
            # for error condition
            if (TimeOutCount > 20):
                    ErrorFlag = True

            # if val2 = 8 the commande handler return ERROR
            if val2 == 8:
                    print "ERROR in execution command handler "
                    ErrorFlag = True

            # return 5 data regs Data1Reg,Data2Reg,Data3Reg,Data4Reg,Data5Reg
            DataRegList =  SetGetDataReg(0,Data1Reg,Data2Reg,Data3Reg,Data4Reg,Data5Reg)
            DataRegList.insert(0,ErrorFlag)
            return DataRegList

    def GetCommandHandlerStatus(self, StatusFlag):
            '''this function return command handler status
                    argument: StatusFlag: 1 -> in progress/busy
                                                              0 -> in pass/error , from BCM84888 DS MDIO COMMAND HANDLER FUNCTION
                    return: 1 -> busy
                                0 -> free to execute command 
            '''	
            driver = self.driver
            reg_value = driver.read_phy_register(0x1E, 0x4037, self.Phy_Address_dict[driver.port_number()])
            if StatusFlag:
                    if ((reg_value == 0xBBBB) or  (reg_value == 2)):
                            return 1,reg_value
                    else:
                            return 0,reg_value
            else:
                    if ((reg_value == 0x8) or (reg_value == 0x4)):
                            return 0,reg_value
                    else:
                            return 1,reg_value

    def SetGetDataReg(self, SetOrGetFlag,Data1Reg,Data2Reg,Data3Reg,Data4Reg,Data5Reg):
            '''this function will be writeing or reading from data registers in BCM Phy
                    argument: 
                                      SetOrGetFlag -> 1 for write (set)
                                                                      0 for read (get)
                                      DataRegValue -> data to write
                    return: 
                                      reg value
            '''
            DataRegList = []
            driver = self.driver
            Phy_Address = self.Phy_Address_dict[driver.port_number()]
            if SetOrGetFlag:
                    driver.write_phy_register(0x1E, 0x4038, Phy_Address, Data1Reg)
                    driver.write_phy_register(0x1E, 0x4039, Phy_Address, Data2Reg)
                    driver.write_phy_register(0x1E, 0x403A, Phy_Address, Data3Reg)
                    driver.write_phy_register(0x1E, 0x403B, Phy_Address, Data4Reg)
                    driver.write_phy_register(0x1E, 0x403C, Phy_Address, Data5Reg)
            else:
                    DataRegList.append(driver.read_phy_register(0x1E, 0x4038, Phy_Address))
                    DataRegList.append(driver.read_phy_register(0x1E, 0x4039, Phy_Address))
                    DataRegList.append(driver.read_phy_register(0x1E, 0x403A, Phy_Address))
                    DataRegList.append(driver.read_phy_register(0x1E, 0x403B, Phy_Address))
                    DataRegList.append(driver.read_phy_register(0x1E, 0x403C, Phy_Address))

            #print "DataRegList ",DataRegList
            return DataRegList


    #########################################################################################################
    ######################                                      #############################################
    #########################################################################################################

    def get_bit_value(value, bit_number):
            return (value >> bit_number) & 0x1

    def _get_bits_slice_value(value, bit_start_number, bit_end_number):
            mask_length = bit_end_number - bit_start_number + 1
            mask_string = '1' * mask_length
            mask = int(mask_string, 2)
            slice_value = (value >> bit_start_number) & mask    
            return slice_value

    #########################################################################################################
    ######################                                      #############################################
    #########################################################################################################

    def TX_Scheduler_Config_Port0():
            driver = self.driver
            GLSCD_IFBCMDH=0x000B20A0
            GLSCD_IFBCMDL=0x000B209c
            
            #port 0
            driver.write_csr(GLSCD_IFBCMDH, 0x320697)
            driver.write_csr(GLSCD_IFBCMDL, 0x23)
            driver.write_csr(GLSCD_IFBCMDH, 0x320b80)
            driver.write_csr(GLSCD_IFBCMDL, 0x23)
            driver.write_csr(GLSCD_IFBCMDH, 0x31a4)
            driver.write_csr(GLSCD_IFBCMDL, 0x23)
            driver.write_csr(GLSCD_IFBCMDH, 0x10a1)
            driver.write_csr(GLSCD_IFBCMDL, 0x3)
            driver.write_csr(GLSCD_IFBCMDH, 0x1088)
            driver.write_csr(GLSCD_IFBCMDL, 0x3)	
            
    def TX_Scheduler_Config_Port2():
            driver = self.driver
            GLSCD_IFBCMDH=0x000B20A0
            GLSCD_IFBCMDL=0x000B209c	
            #port 2
            driver.write_csr(GLSCD_IFBCMDH, 0x320697)
            driver.write_csr(GLSCD_IFBCMDL, 0x223)
            driver.write_csr(GLSCD_IFBCMDH, 0x320b80)
            driver.write_csr(GLSCD_IFBCMDL, 0x223)
            driver.write_csr(GLSCD_IFBCMDH, 0x31a4)
            driver.write_csr(GLSCD_IFBCMDL, 0x223)
            driver.write_csr(GLSCD_IFBCMDH, 0x10a1)
            driver.write_csr(GLSCD_IFBCMDL, 0x203)
            driver.write_csr(GLSCD_IFBCMDH, 0x1088)
            driver.write_csr(GLSCD_IFBCMDL, 0x203)
            

    #########################################################################################################
    ######################           Admin Command              #############################################
    #########################################################################################################



#########################################################################################################
######################           DEBUG SECTION              #############################################
#########################################################################################################

    def AQ_Debug ():
                    driver = self.driver		
                    aq_desc = AqDescriptor()
                    aq_desc.opcode = 0xff04
                    aq_desc.param1 = 0x8c260
                    aq_desc.flags = 0x0200
                    
                    #buf = [0,1,2,3,4,5]
                    #driver.send_aq_command(aq_desc, buf)
                    #val1 = buf[0]
                    #val2 = buf[1]

                    driver.send_aq_command(aq_desc)

                    print 'retval: ', hex(aq_desc.retval)
                    print 'flags: ', hex(aq_desc.flags)
                    print 'opcode: ', hex(aq_desc.opcode)
                    print 'param0: ', hex(aq_desc.param0)
                    print 'param1: ', hex(aq_desc.param1)
                    print 'cookie_high: ', hex(aq_desc.cookie_high)
                    print 'cookie_low: ', hex(aq_desc.cookie_low)
                    print 'addr_high: ', hex(aq_desc.addr_high)
                    print 'addr_low: ', hex(aq_desc.addr_low)

    def Mdio_Read_Debug(self, Page, Register):
            driver = self.driver
            reg_value = driver.read_phy_register(Page, Register, self.Phy_Address_dict[driver.port_number()])
            return reg_value

    def Mdio_Write_Debug(self, Page,Register,value):
            driver = self.driver
            driver.write_phy_register(Page, Register, self.Phy_Address_dict[driver.port_number()], value)

    def CSR_Write_Debug(self, Address,Value,Mul=0):
            driver = self.driver
            reg_addr = calculate_port_offset(Address, Mul, driver.port_number())
            driver.write_csr(reg_addr, Value)

    def CSR_Read_Debug(self, Address,Mul=0):
            driver = self.driver
            reg_addr = calculate_port_offset(Address, Mul, driver.port_number())
            return driver.read_csr(reg_addr)

    def DbgReadMdioRegister(self, Page,Register):
            driver = self.driver
            reg_value = driver.read_phy_register(Page, Register, self.Phy_Address_dict[driver.port_number()])
            #print hex(reg_value)
            return hex(reg_value)

    def ReadMdioRegister(self, Page,Register):
            driver = self.driver
            reg_value = driver.read_phy_register(Page, Register, self.Phy_Address_dict[driver.port_number()])
            #print hex(reg_value)
            return reg_value

    def WriteMdioRegister(self, Page,Register,value):
            driver = self.driver
            driver.write_phy_register(Page, Register, self.Phy_Address_dict[driver.port_number()], value)

    def XFI_TX_prbs31_gen_config(self):
            ''' This function sets TX prbs31 according to "Advance Data Sheet 84892-DS102" pdf file section 2.7.1.11
            '''
            self.ConfigDirection(0) # set MDIO direction to host interface
            self.WriteMdioRegister(1,0xD0E1,0xB) # set XFI TX PRBS to PRBS31, and enable PRBS

    def XFI_RX_prbs31_chk_config(self):
            ''' This function sets RX prbs31 according to "Advance Data Sheet 84892-DS102" pdf file section 2.7.1.12
            '''
            self.ConfigDirection(0) # set MDIO direction to host interface
            self.WriteMdioRegister(1,0xD0D1,0x2B) # set XFI RX PRBS to PRBS31, and enable PRBS
            
    def XFI_Set_prbs31_mode(self):
            self.XFI_TX_prbs31_gen_config()
            self.XFI_RX_prbs31_chk_config()

    def XFI_RX_prbs_chk_lock_status(self):
            ''' This function check prbs lock RX status according to "Advance Data Sheet 84892-DS102" pdf file section 2.7.1.13
            '''
            prbs_chk_lock_status = ReadMdioRegister(1,0xD0D9)
            if (prbs_chk_lock_status & 0x1) == 1:
                    print "PRBS chacker is on lock state"
            else:
                    print "PRBS chacker is unlock state"

    def XFI_RX_prbs_chk_err_cnt_status(self):
            ''' This function check prbs error count according to "Advance Data Sheet 84892-DS102" pdf file section 2.7.1.14/5
            '''
            prbs_chk_err_cnt_msb_status = ReadMdioRegister(1,0xD0DA)
            prbs_chk_err_cnt_lsb_status = ReadMdioRegister(1,0xD0DB)
            #print "prbs_chk_err_cnt_msb_status: ",prbs_chk_err_cnt_msb_status
            #print "prbs_chk_err_cnt_lsb_status: ",prbs_chk_err_cnt_lsb_status
            prbs_chk_err_cnt_sum = (prbs_chk_err_cnt_msb_status << 16) | prbs_chk_err_cnt_lsb_status
            print "PRBS error count: ",prbs_chk_err_cnt_sum

    def XFI_TX_inject_single_error(self):
            ''' This function inject single error "Advance Data Sheet 84892-DS102" pdf file section 2.7.1.11
            '''
            XFI_TX_prbs_gen_config = ReadMdioRegister(1,0xD0E1)
            XFI_TX_prbs_gen_config = XFI_TX_prbs_gen_config & 0xFFDF # clear bit 5, error inject works when bit it changes from 0 -> 1
            WriteMdioRegister(1,0xD0E1,XFI_TX_prbs_gen_config)	
            XFI_TX_prbs_gen_config = XFI_TX_prbs_gen_config | 0x20 # set 1 to bit 5 to inject error
            WriteMdioRegister(1,0xD0E1,XFI_TX_prbs_gen_config)

    def Enable_line_side_pcs_loopback(self):
            ConfigDirection(1) # set MDIO direction to host interface
            XFI_pcs_control_register = ReadMdioRegister(3,0x0)
            print type(XFI_pcs_control_register)
            XFI_pcs_control_register = XFI_pcs_control_register | 0x4000 # set 1 to bit 14 to enable loopback
            WriteMdioRegister(3,0x0,XFI_pcs_control_register)


    def Set_Host_side_link_to_10G_KR_mode(self):
            # set Blackfin host interface to KR mode, "Advance Data Sheet 84892-DS102" pdf file section 1.23.1.16
            self.GetCommandHandler(0x800f,1,1,0,0,0,0)

    def Set_Host_side_link_to_10G_SFI_mode(self):
            # set Blackfin host interface to XFI mode, "Advance Data Sheet 84892-DS102" pdf file section 1.23.1.16
            self.GetCommandHandler(0x800f,1,0,0,0,0,0)

    def Get_host_interface_link_mode():
            # get Blackfin host interface mode, "Advance Data Sheet 84892-DS102" pdf file section 1.23.1.15
            CommandHandlerReturnValue = self.GetCommandHandler(0x800e,0,0,0,0,0,0)
            #print CommandHandlerReturnValue
            link_mode = CommandHandlerReturnValue[1]
            print "return value", link_mode
            if link_mode == 0xFFFF:
                    print "command handler read error"
            elif link_mode == 0x0:
                    print "Host Interface reports KR mode disable (XFI enable)"
            elif link_mode == 0x1:
                    print "Host Interface reports KR mode enable"
            else:
                    print "unknown error occur"

    def Reset(self, reset_type = 'pfr'):
        '''This function performs resets
            argument: reset_type (string) - "globr" , "pfr" , "corer", "empr", "flr", "pcir", "bmer", "vfr", "vflr"
            return: None
        '''
        if reset_type in self.reset_type_dict:
            self.driver.device_reset(self.reset_type_dict[reset_type])
        else:
            print("could not identify reset type")

###############################################################################
#                                link configuration Commands                  #
###############################################################################

    def SetLinkSpeed(self, speed, an_mode = True, debug = False):
        
        supported_speeds = self.GetSupportedSpeeds()

        if speed in supported_speeds:
            link_speed = 1 << self.phy_speed_to_bit_dict[speed]
        else:
            msg = "provided speed is not supported"
            raise RuntimeError(msg)
        args = dict()
        args['rep_active'] = 1
        status, data = self.GetPhyAbilities(args) 
        if status:
            error_msg = 'Error - SetPhyConfiguration: GetPhyAbilities Admin command was not successful, retval {}'.format(data)
            raise RuntimeError(error_msg)

        config = dict() 
        config['phy_type'] = data['phy_type']
        config['link_speed'] = link_speed
        config['pause_abil'] = 0
        config['low_pwr_abil'] = 0
        config['en_link'] = 1
        config['an_mode'] = 1 if an_mode else 0
        config['en_auto_link_update'] = 1
        config['eee_capability'] = (0X3 << 8) | data['eee_capability']
        config['eeer'] = data['eeer']
        config['low_pwr_ctrl'] = data['low_pwr_ctrl']
        config['phy_type_extension'] = data['phy_type_extension']
        config['fc_fec_abil'] = data['fc_fec_abil']
        config['rs_fec_abil'] = data['rs_fec_abil']
        config['fc_fec_req'] = data['fc_fec_req']
        config['rs_fec_req'] = data['rs_fec_req']
        config['en_auto_fec_mode'] = data['en_auto_fec_mode']

        status, data =  self.SetPhyConfig(config, debug)

        if status:
            error_msg = 'Error - SetPhyConfig Admin command was not successful, retval {}'.format(data)
            raise RuntimeError(error_msg)

    def GetPhyTypeAbilities(self):
        status, data = self.GetPhyAbilities(dict())

        if status:
            error_msg = 'Error - GetPhyTypeAbilities: GetPhyAbilities Admin command was not successful, retval {}'.format(data)
            raise RuntimeError(error_msg)   

        phy_type = data['phy_type']
        phy_type_extension = data['phy_type_extension']
        phytype_list = list()
        for i in range(32):
            mask = 1 << i 
            if phy_type & mask:
                phytype_list.append(self.get_Ability_PhyType_dict[i])

        for i in range(8):
            mask = 1 << i 
            if phy_type_extension & mask:
                phytype_list.append(self.get_Ability_PhyTypeExtension_dict[i])

        return phytype_list

    def GetSupportedSpeeds(self):
        status, data = self.GetPhyAbilities(dict())

        if status:
            error_msg = 'Error - GetPhyAbilities: GetPhyAbilities Admin command was not successful, retval {}'.format(data)
            raise RuntimeError(error_msg)   

        link_speed = data['link_speed_abil']

        supported_speeds = list()
        for i in range(8):
            mask = 1 << i
            if link_speed & mask:
                supported_speeds.append(self.get_Ability_speed_dict[i])

        return supported_speeds

    def SetPhyConfiguration(self, PhyType, FEC_type, debug = False):
        phy_type = 0
        status, data = self.GetPhyAbilities(dict()) 

        if status:
            error_msg = 'Error - SetPhyConfiguration: GetPhyAbilities Admin command was not successful, retval {}'.format(data)
            raise RuntimeError(error_msg)

        abilities = data

        config = {}
        config['port'] = 0 #not relevant for CVL according to CVL Spec
        config['tx_pause_req'] = abilities['pause_abil']
        config['rx_pause_req'] = abilities['asy_dir_abil']
        config['low_pwr_abil'] = 0
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

        status, data =  self.SetPhyConfig(config)

        if debug == True:
            if status == 0:
                print("Admin command successded") #TODO print admin command message 
            else:
                print("Admin command failed")
                print(config)
        if status:
            error_msg = 'Error - SetPhyConfig Admin command was not successful, retval {}'.format(data)
            raise RuntimeError(error_msg)

    def GetLinkStatusField(self):
        status, data = self.GetLinkStatus(dict())
        return data['link_status']

    def GetLinkSpeed(self):
        status, data = self.GetLinkStatus(dict())

        if status:
            error_msg = 'Error - GetLinkSpeed: GetLinkStatus Admin command was not successful, retval {}'.format(data)
            raise RuntimeError(error_msg)
        link_speed_field = data['link_speed']
        for i in range(8):
            mask = 1 << i
            if link_speed_field & mask:
                return self.get_Ability_speed_dict[i]

###############################################################################
#                                Admin Queue Commands                         #
###############################################################################

    def SetPhyConfig(self, config, debug = False):
        '''
            Description:  Set various PHY configuration parameters on port. 
            input:
                config -- type(dict)
                    'phy_type' : int[4 bytes] -- Bytes 3:0 of PHY capabilities
                    'link_speed' : int[1 byte]  -- Bytes 4 
                    'pause_abil' : int[2 bits] -- Bytes 5.0:5.1 
                    'low_pwr_abil': int[1 bit] -- Bytes 5.2
                    'en_link' : int[1 bit] -- Bytes 5.3
                    'an_mode' : int[1 bit] -- Bytes 5.4
                    'en_auto_link_update': int[1 bit] -- Bytes 5.5
                    'reserved' int[2 bit] -- Bytes 5.6:5.7
                    'EEE_capability_en' int[2 bytes] -- Bytes 6:7
                    'EEER' : int[4 bytes] -- Bytes 8:11
                    'low_pwr_ctrl' : int[1 byte] -- Bytes 12
                    'phy_type_extension': int[1 byte] -- Bytes 13
                    'fc_fec_abil': int[1 bit] -- Bytes 14.0
                    'RS_FEC_abil': int[1 bit] -- Bytes 14.1
                    'FC_FEC_req' : int[1 bit] -- Bytes 14.2
                    'RS_FEC_req' : int[1 bit] -- Bytes 14.3
                    'en_auto_FEC_mode' : int[1 bit] -- Bytes 14.4
                    'reserved' : int[1 bytes 3 bit] -- Bytes 14.5:15
            return:
                status -- type(tuple) (bool, int)
                    bool -- Indication if Admin command was successful, False if so, True if not
                    int -- if bool True, value of Admin command retval, if false is None
        '''
        driver = self.driver
        aq_desc = AqDescriptor()
        data_len = 0
        buffer = []

        byte_0 = config['phy_type'] & 0xff
        byte_1 = (config['phy_type'] >> 8) & 0xff
        byte_2 = (config['phy_type'] >> 16) & 0xff
        byte_3 = (config['phy_type'] >> 24) & 0xff
        byte_4 = config['link_speed']
        byte_5 = (config['en_auto_link_update'] << 5) | (config['an_mode'] << 4) | (config['en_link'] << 3) | (config['low_pwr_abil'] << 2) | config['pause_abil']
        byte_6 = config['eee_capability'] & 0xff
        byte_7 = (config['eee_capability'] >> 8) & 0xff
        byte_8 = config['eeer'] & 0xff
        byte_9 = (config['eeer'] >> 8) & 0xff
        byte_10 = (config['eeer'] >> 16) & 0xff
        byte_11 = (config['eeer'] >> 24) & 0xff
        byte_12 = config['low_pwr_ctrl']
        byte_13 = config['phy_type_extension']
        byte_14 = (config.get('en_auto_fec_mode',1) << 4) | (config['rs_fec_req'] << 3) | (config['fc_fec_req'] << 2) | (config['rs_fec_abil'] << 1) | config['fc_fec_abil']
        byte_15 = 0

        aq_desc.opcode = 0x0601
        aq_desc.flags = 0x2000 #Do not interrupt 
        # bytes 16-19
        aq_desc.param0 = config['phy_type']
        # bytes 20-23
        aq_desc.param1 = (byte_7 << 24) | (byte_6 << 16) | (byte_5 << 8) | byte_4
        # bytes 24-27
        aq_desc.addr_high = (byte_11) | (byte_10 << 16) | (byte_9 << 8) | byte_8
        # bytes 28-31
        aq_desc.addr_low = (byte_15) | (byte_14 << 16) | (byte_13 << 8) | byte_12
        aq_desc.datalen = data_len

        status = driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Set PHY Config Admin Command, status: {} , FW ret value: {}'.format(status,aq_desc.retval))

        err_flag = (aq_desc.flags & 0x4) >> 2 #isolate the error flag

        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)
        return status

    def SetMacConfig(self, config,debug=False):
        '''
            Description: Set various MAC configuration parameters on the port.
            input:
                config -- type(dict):
                    'max_frame' : int[2 bytes]  -- Sets the maximum ethernet frame size on a port
                    'pacing_type' : int[1 bit] -- 1 enables fixed IPG rate pacing, 0 is  data-based rate pacing
                    'pacing_rate' : int[4 bits] -- bitfield sets either the IPG words or the data pacing rate depending on state of pacing_type
                    'tx_priority' : int[1 byte]
                    'tx_value' : int[2 bytes]
                    'fc_refr_thresh' : int[2 bytes]
            return:
                status -- type(tuple) (bool, int)
                    bool -- Indication if Admin command was successful, False if so, True if not
                    int -- if bool True, value of Admin command retval, if false is None
        '''
        driver = self.driver
        opCodes = AqOpCodes()
        aq_desc = AqDescriptor()
        #lvar assignment
        data_len = 0x0
        aq_desc.opcode = opCodes.set_mac_config
        aq_desc.datalen = data_len
        buffer = [0] * data_len
        aq_desc.param0 = (config['tx_priority'] << 24) | (config['pacing_rate'] << 23) | (config['pacing_type'] << 19) | config['max_frame']
        aq_desc.param1 = (config['fc_refr_thresh'] << 16) | (config['tx_value'])
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.flags = 0x0
        
        status = driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Set MAC Config Admin Command, status: ', status, ', FW ret value: ', aq_desc.retval)
        err_flag = (aq_desc.flags & 0x4) >> 2 #isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)
        return status

    def GetPhyAbilities(self, args, debug = False):
        '''
            Description:  Get various PHY abilities supported on the port.
            input:
                args -- type(dict)
                    rep_active -- int[1 bit] -- report the active values.
            return:
                bool -- Indication if Admin command was successful, False if so, True if not
                    if bool is True, dict becomes in with Admin command retval
                dict -- data
        '''
        driver = self.driver

        aq_desc = AqDescriptor()
        data_len = 0x1000
        aq_desc.flags = 0x1200 #Set the buffer flag & long buffer flag
        aq_desc.opcode = 0x0600 
        aq_desc.datalen = data_len
        buffer = [0] * data_len
        aq_desc.param0 = (args.get('rep_active',1) << 1) | args.get('report_qualified_modules',1)
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0

        status = driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Get PHY Abilities Admin Command, status: {} FW ret value: {}'.format(status, aq_desc.retval))

        err_flag = (aq_desc.flags & 0x4) >> 2 #isolate the error flag

        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            data = {}
            data['phy_type'] = compose_num_from_array_slice(buffer, 0, 4)
            data['link_speed_abil'] = compose_num_from_array_slice(buffer, 4, 1) 
            data['pause_abil'] = compose_num_from_array_slice(buffer, 5, 1) & 0x3
            data['low_pwr_abil'] = (compose_num_from_array_slice(buffer, 5, 1) & 0x4) >> 2
            data['link_mode'] = (compose_num_from_array_slice(buffer, 5, 1) & 0x8) >> 3
            data['an_mode'] = (compose_num_from_array_slice(buffer, 5, 1) & 0x10) >> 4
            data['en_module_qualification'] = (compose_num_from_array_slice(buffer, 5, 1) & 0x20) >> 5
            data['reserved_5_6'] = (compose_num_from_array_slice(buffer, 5, 1) & 0xc0) >> 6
            data['eee_capability'] = compose_num_from_array_slice(buffer, 6, 2) & 0xffff
            data['eeer'] = compose_num_from_array_slice(buffer, 8, 4) 
            data['low_pwr_ctrl'] = compose_num_from_array_slice(buffer, 12, 1)
            data['phy_type_extension'] = compose_num_from_array_slice(buffer, 13, 1) 
            data['fc_fec_abil'] = compose_num_from_array_slice(buffer, 14, 1) & 0x1 
            data['rs_fec_abil'] = (compose_num_from_array_slice(buffer, 14, 1) & 0x2) >> 1
            data['fc_fec_req'] = (compose_num_from_array_slice(buffer, 14, 1) & 0x4) >> 2
            data['rs_fec_req'] = (compose_num_from_array_slice(buffer, 14, 1) & 0x8) >> 3
            data['en_auto_fec_mode'] = (compose_num_from_array_slice(buffer, 14, 1) & 0x10) >> 4
            data['current_module_type_ext'] = (compose_num_from_array_slice(buffer, 14, 1) & 0xe0) >> 2
            data['current_module_type_compliance_code'] = compose_num_from_array_slice(buffer, 15, 1) 
            data['current_phy_id_vendor'] = compose_num_from_array_slice(buffer, 16, 4) 
            data['current_module_type'] = compose_num_from_array_slice(buffer, 20, 3) 
            data['qualified_module_count'] = compose_num_from_array_slice(buffer, 23, 3) 
            data['qualified_module_id_n'] = buffer[24:55] 
            status = (False, data)
        return status

    def GetLinkStatus(self, args, debug = False):
        '''
            Description:  Get link status of the port.
            input:
                args -- dict
                    'en_lse' : int[2 bits] -- Bytes 16.0:16.1
            return:
                status -- type(tuple) (bool, dict)
                    bool -- Indication if Admin command was successful, False if so, True if not
                        if bool is True, dict becomes int with Admin command retval
                    dict -- data
        '''
        driver = self.driver
        aq_desc = AqDescriptor()
        aq_desc.flags = 0 #Set the buffer and long buffer flags
        aq_desc.opcode = 0x0607 
        aq_desc.datalen = 0 
        buffer = []
        aq_desc.param0 = args.get('en_lse',0)  
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0

        status = driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Get Link Status Admin Command, status: {} FW ret value: {}'.format(status, aq_desc.retval))

        err_flag = (aq_desc.flags & 0x4) >> 2 #isolate the error flag

        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            data = {}
            data['en_lse'] = aq_desc.param0 & 0x1
            data['phy_type'] = (aq_desc.param0 >> 16) & 0xff
            data['link_speed'] = (aq_desc.param0 >> 24) & 0xff
            data['link_status'] = aq_desc.param1 & 0x1
            data['link_fault'] = (aq_desc.param1 & 0x1c) >> 1
            data['ext_port_link_status'] = (aq_desc.param1 & 0x20) >> 5
            data['media_avail'] = (aq_desc.param1 & 0x40) >> 6
            data['signal_detect'] = (aq_desc.param1 & 0x80) >> 7
            data['an_completed'] = (aq_desc.param1 >> 8) & 0x1
            data['lp_an_abil'] = ((aq_desc.param1 >> 8) & 0x2) >> 1 
            data['parallel_detection_fault'] = ((aq_desc.param1 >> 8) & 0x4) >> 2
            data['fec_en'] = ((aq_desc.param1 >> 8) & 0x8) >> 3
            data['low_pwr_state'] = ((aq_desc.param1 >> 8) & 0x10) >> 4
            data['link_pause_status'] = ((aq_desc.param1 >> 8) & 0x60) >> 5
            data['qualified_module'] = ((aq_desc.param1 >> 8) & 0x80) >> 7
            data['phy_temp_alarm'] = (aq_desc.param1 >> 16) & 0x1
            data['excessive_link_err'] = ((aq_desc.param1 >> 16) & 0x2) >> 1
            data['port_tx_suspended'] = ((aq_desc.param1 >> 16) & 0xc0) >> 2
            data['force_40g_en'] = ((aq_desc.param1 >> 16) & 0x10) >> 4
            data['unionvale_err_code'] = ((aq_desc.param1 >> 16) & 0xe0) >> 5
            data['lpbk_lvl'] = ((aq_desc.param1 >> 24) & 0xf)
            data['lpbk_type_status'] = ((aq_desc.param1 >> 24) & 0x10) >> 4
            data['reserved_5_5'] = ((aq_desc.param1 >> 24) & 0x20) >> 5
            data['external_debice_pwr_abil'] = ((aq_desc.param1 >> 24) & 0xc0) >> 6
            data['max_frame_size'] = aq_desc.addr_high & 0xffff
            data['25g_kr_fec_en'] = ((aq_desc.addr_high >> 16) & 0x1)
            data['25g_rs_fec_en'] = ((aq_desc.addr_high >> 16) & 0x2) >> 1
            data['crc_en'] = ((aq_desc.addr_high >> 16) & 0x4) >> 2
            data['pacing_cfg'] = ((aq_desc.addr_high >> 16) & 0x78) >> 3
            data['reserved_8_7'] = ((aq_desc.addr_high >> 16) & 0x80) >> 7
            data['link_type'] = (aq_desc.addr_low & 0xffffff) | ((aq_desc.addr_high >> 24) & 0xff)
            data['link_type_ext'] = (aq_desc.addr_low >> 24) & 0xff
            status = (False, data)
        return status

    def _RestartAn(self, args, debug = False):
        driver = self.driver
        aq_desc = AqDescriptor()
        aq_desc.flags = 0 
        aq_desc.opcode = 0x0605 
        aq_desc.datalen = 0 
        buffer = []
        aq_desc.param0 = args.get('en_link',1) | 1 << 1  
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0

        status = driver.send_aq_command(aq_desc, buffer, debug)
        err_flag = (aq_desc.flags & 0x4) >> 2 #isolate the error flag
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Get Link Status Admin Command, status: {} FW ret value: {}'.format(status, aq_desc.retval))
            return (True, aq_desc.retval)
        else:
            return (False, None)

    def SetPhyLoopback(self,phy_lpbk_args,debug=False):
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
        driver = self.driver
        opCodes = AqOpCodes()
        aq_desc = AqDescriptor() # helper._debug('SetPhyLoopback Admin Command')
        data_len = 0x0
        aq_desc.opcode = opCodes.set_phy_loopback
        aq_desc.datalen = data_len
        buffer = [0] * data_len
        aq_desc.param0 = (phy_lpbk_args['level'] << 26) | (phy_lpbk_args['type'] << 25) | (phy_lpbk_args['enable'] << 24) | (phy_lpbk_args['index'] << 16) | phy_lpbk_args['port']
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

    def SetPhyDebug(self, debug_args,debug=False):
        '''
            Description:  Resets PHYs or disables Link Management Firmware
            input:
                debug_args -- type : dict
                    'reset_internal_phy' : int[1 bit] -- Byte 16.1
                    'reset_external_phy' : int[2 bit] -- Byte 16.2:16.3
                    'disable_lm' : int[1 bit] -- Byte 16.4
            return:
                status -- type : tuple (bool, int)
                    bool -- Indication if Admin command was successful, False if so, True if not
                    int -- if bool is False, None, else int is Admin command retval
        '''

        driver = self.driver
        aq_desc = AqDescriptor()
        aq_desc.flags = 0x0
        aq_desc.opcode = 0x0622
        aq_desc.datalen = 0x0
        aq_desc.param0 = (debug_args['disable_lm'] << 4) | (debug_args['reset_external_phy'] << 2) | (debug_args['reset_internal_phy'] << 1) | 0
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0

        status = driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Set Phy Debug Admin Command, status: ', status, ', FW ret value: ', aq_desc.retval)
        err_flag = (aq_desc.flags & 0x4) >> 2 #isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)
        return status

    def SetPhyRegister(self, args, debug = False):
        '''
            Description:  This commad is used by the device driver to write to an internal or external PHY register
            input:
                args -- type : dict
                    'interface_sel': int[1 byte] : -- Byte 16
                    'dev_addr' : int[1 byte] -- Byte 17
                    'recall_qsfp_page' : int[1 bit] -- Byte 18.0
                    'reserved' : Byte 18.1:19 vlaue must be 0
                    'reg_addr' : int[4 byte] -- Bytes 20:23
                    'reg_w_data' : int[4 byte] -- Bytes 24-27
                    'reserved' :Bytes 28:31 value must be 0
            return:
                data -- type : dict
                    'interface_sel': int[1 byte] 
                    'dev_addr' : int[1 byte] 
                    'recall_qsfp_page' : int[1 bit] 
                    'reg_addr' : int[4 byte]
                    'reg_w_data' : int[4 byte]
                status -- type : tuple (bool, int)
                    bool -- Indication if Admin command was successful, False if so, True if not
                    int -- if bool is False, None, else int is Admin command retval
        '''

        driver = self.driver

        aq_desc = AqDescriptor()
        aq_desc.flags = 0x0
        aq_desc.opcode = 0x0629
        aq_desc.datalen = 0x0
        aq_desc.param0 = (debug_args['cmd_flags'] << 24) | (debug_args['reset_external_phy'] << 2) | (debug_args['reset_internal_phy'] << 1) | 0
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0

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

    def SetupLink(self, slu_args,debug=False):
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
        driver = self.driver
        opCodes = AqOpCodes()
        aq_desc = AqDescriptor()
        data_len = 0x0
        aq_desc.opcode = opCodes.setup_link
        aq_desc.datalen = data_len
        buffer = [0] * data_len
        aq_desc.param0 = (slu_args['enable'] << 18) | (slu_args['restart'] << 17) | slu_args['port']
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.flags = 0x0
        
        status = driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Setup Link Admin Command, status: ', status, ', FW ret value: ', aq_desc.retval)
        err_flag = (aq_desc.flags & 0x4) >> 2 #isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)
        return status

    def StopLLDP(self):
        driver = self.driver

        aq_desc = AqDescriptor()    
        aq_desc.flags = 0x0200 
        aq_desc.opcode = 0x0A05
        aq_desc.datalen = 0
        aq_desc.param0 = 0
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0

        status = driver.send_aq_command(aq_desc)

