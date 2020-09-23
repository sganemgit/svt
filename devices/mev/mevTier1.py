from devices.mev.mevDefines import mevDefines
from core.utilities.BitManipulation import *

class mevTier1(mevDefines):
        
    def SetPhyConfig(self, args, debug = False):
        '''
            Sets various PHY configuration parameters of a por
            input:
                args -- type(dict)
                    'logical_prt_num' : int[1 byte] -- Logical Port Number
                    'phy_type_0' : int[4 bytes] -- Bytes 7:4 
                    'phy_type_1' : int[4 bytes] -- Bytes 11:8 
                    'phy_type_2' : int[4 bytes] -- Bytes 15:12 
                    'phy_type_3' : int[4 bytes] -- Bytes 19:16 
                    'tx_pause_en' : int[1 bit] -- Enable / Disable TX Pause ability
                    'rx_pause_en' : int[1 bit] -- Enable / Disable RX Pause ability
                    'auto_fec_en' :int[1 bit] -- 1 to enable LESM AutoFec, 0 to disable
                    'lesm_en' : int[1 bit] -- 1 to enable LESM, 0 to disable
                    'en_auto_update' : int[1 bit] -- 1 to enable Automatic link update
                    'en_link': int[1 bit] -- 1 to enable link, 0 to disable
                    'low_pwr_mod' : int[1 bit] -- 1 to low power mode , 0 to High power mode
                    'lplu_en' : int[1 byte] --  1 to enable Low Power Link Up
                    '25g_kr_fec_abil' : int[1 bit] -- 1 to enable 25G KR FEC capability
                    'rs_fec528_abil' : int[1 bit] -- 1 to enable Rs FEC 528 capability
                    'no_fec_abil' : int[1 bit] -- 1 to enable NO FEC capability
                    'rs_fec544_req': int[1 bit] -- 1 to enable Rs FEC 544 capability request
                    '25g_kr_fec_req': int[1 bit] -- 1 to enable 25G KR FEC capability request
                    'rs_fec528_req': int[1 bit] -- 1 to enable Rs FEC 528 capability request
                    '10g_kr_fec_req': int[1 bit] -- 1 to enable 10G KR FEC capability request
                    '10g_kr_fec_abil': int[1 bit] -- 1 to enable 10G KR FEC capability
                    'll_rc_fec272_req': int[1 bit] -- 1 to enable LL RS FEC 272 capability request for 50G KR/CR,100G KR2/CR2, 200G KR4/CR4
                    'll_rc_fec272_200g_abil' : int[1 bit] -- 1 to enable LL RS FEC 272 capability advertisement for 200G KR4/CR4
                    'll_rc_fec272_100g_abil':int[1 bit] -- 1 to enable LL RS FEC 272 capability advertisement for 100G KR2/CR2
                    'll_rc_fec272_50g_abil' : int[1 bit] -- 1 to enable LL RS FEC 272 capability advertisement for 50G KR/CR
        '''
        print("SetPHyconfig")
        buffer = list()
        buffer.append(byte_0)
        # Add PHY Type to buffer (bytes 4-19)
        buffer.extend(turn_arg_to_bytes(config['phy_type_0']))
        buffer.extend(turn_arg_to_bytes(config['phy_type_1']))
        buffer.extend(turn_arg_to_bytes(config['phy_type_2']))
        buffer.extend(turn_arg_to_bytes(config['phy_type_3']))
        byte_0 = args["logical_prt_num"] & 0xff
        byte_20 = (args["auto_fec_en"] << 7) | (args["lesm_en"] << 6) | (args["en_auto_update"] << 5) | (args["en_link"] << 3) | (args["low_pwr_mod"] << 2) | (args["rx_pause_en"] << 1) | args["tx_pause_en"]
        byte_21 = args["lplu_en"] & 0xff
        byte_26 = (args["25g_kr_fec_abil"] << 7) | (args["rs_fec528_abil"] << 6) | (args["no_fec_abil"] << 5) | (args["rs_fec544_req"] << 4) | (args["25g_kr_fec_req"] << 3) | (args["rs_fec528_req"] << 2) | (args["10g_kr_fec_req"] << 1) | args["10g_kr_fec_abil"]
        byte_27 = (args["ll_rc_fec272_req"] << 4) |(args["ll_rc_fec272_200g_abil"] << 3) | (args["ll_rc_fec272_100g_abil"] << 2) | (args["ll_rc_fec272_50g_abil"] << 1)
        buffer.append(byte_20)
        buffer.append(byte_21)
        buffer.append(byte_26)
        buffer.append(byte_27)

    def SetMacConfig(self,  args, debug = False):
        '''
            Set various MAC configuration parameters supported on a specific port
            input:
                args -- type(dict)
                    'logical_prt_num' : int[1 byte] -- Logical Port Number
                    'max_frame' : int[2 bytes]  -- Sets the maximum ethernet frame size on a port
                    'pacing_type' : int[1 bit] -- 1 enables fixed IPG rate pacing, 0 is  data-based rate pacing -- Bytes 4.7
                    'pacing_config' : int[4 bits] -- allows configuring PACE parameter in the MAC to slow down the effective data rate
                    'transmit_timer_priority':  int[1 bytes]  
                    'transmit_timer_value':  int[2 bytes]  
                    'fc_refresh_threshold':  int[2 bytes]  
                    'auto_drop_blocking_packets':  int[1 bytes]  -- 1 The blocking packet is dropped and then the PF driver is notified, 0 the PF driver is notified
        '''
        buffer = list()
        byte_0 = args["logical_prt_num"] & 0xff
        byte_2 = args["max_frame"] & 0xff
        byte_3 = (args["max_frame"] >> 8) & 0xff
        byte_4 = (args["pacing_type"] << 7) | (args["pacing_config"] << 3)
        byte_5 = args["transmit_timer_priority"] & 0xff
        byte_6 = args["transmit_timer_value"] & 0xff
        byte_7 = (args["transmit_timer_value"] >> 8) & 0xff
        byte_8 = args["fc_refresh_threshold"] & 0xff
        byte_9 = (args["fc_refresh_threshold"] >> 8) & 0xff
        byte_10 = args["auto_drop_blocking_packets"] & 0xff
        buffer.append(byte_0)
        buffer.append(byte_2)
        buffer.append(byte_3)
        buffer.append(byte_4)
        buffer.append(byte_5)
        buffer.append(byte_6)
        buffer.append(byte_7)
        buffer.append(byte_8)
        buffer.append(byte_9)
        buffer.append(byte_10)

    def LinkSetupAndRestartAn(Self, args, debug = False):
        '''
            Sets up the link and restarts link auto-negotioation
            This command needs to be executed for other set link parameters to take effect on the link
            input:
                args -- type(dict)
                    'logical_prt_num' : int[1 byte] -- Logical Port Number
                    'link_restart' : int[1 bit] -- 1 to restart the link
                    'link_enable' : int[1 bit] -- 1 to enable the link, 0 to disable the link
        '''
        buffer = list()
        byte_0 = args["logical_prt_num"] & 0xff
        byte_2 = (args["link_enable"] << 2) | (args["link_restart"] << 1)
        buffer.append(byte_0)
        buffer.append(byte_2)

    def GetPhyCapabilities(self, args, debug = False):
        '''
            Get various PHY capabilites supported by a port
            input:
                args -- type(dict)
                    'logical_prt_num' : int[1 byte] -- Logical Port Number
                    'report_mode' : int[2 bits] -- 00b reports capabilities without media, 01b reports capabilities including media, 10b report active configuration, 11b media capabilities
            returns: 
                data -- type(dict)
                'logical_prt_num' : int[1 byte] -- Logical Port Number
                'phy_type_0' : int[4 byte] -- Bytes 3:0 of PHY capabilities
                'phy_type_1' : int[4 byte] -- Bytes 7:4 of PHY capabilities
                'phy_type_2' : int[4 byte] -- Bytes 11:8 of PHY capabilities
                'phy_type_3' : int[4 byte] -- Bytes 15:12 of PHY capabilities
                'phy_types' : int[16 byte] -- Bytes 15:0 of PHY capabilities
                'tx_pause_abil': int[1 bit] -- 1 if port does advertise TX Pause ability
                'rx_pause_abil': int[1 bit] -- 1 if port does advertise RX Pause ability
                'low_pwr_mod': int[1 bit] -- 1 Low power , 0 High power
                'link_mode': int[1 bit] -- 1 if link is enabled
                'lesm_en': int[1 bit] -- 1 if  Link Establishment State Machine is enabled
                'auto_fec_en': int[1 bit] -- 1 if the automatic selection of FEC mode is enabled
                'lplu_en': int[1 bit] -- 1 if Low Power Link Up is enabled
                'an_28_en': int[1 bit] --1 if AN28 is enabled
                'an_73_en': int[1 bit] --1 if AN73 is enabled
                'an_37_en': int[1 bit] --1 if AN37 is enabled
                'phy_id' : int[4 byte] -- PHY ID / SFF Vendor OUI
                'phy_fw_version' : int[8 byte] -- This 8 bytes field represents the FW version of the outermost PHY
                '10g_kr_fec_abil': int[1 bit] --Reflects the 10G KR FEC capability advertisement
                '10g_kr_fec_req': int[1 bit] --Reflects the 10G KR FEC capability request
                'rs_fec528_req': int[1 bit] -- Reflects the RS FEC 528 capability request
                '25g_kr_fec_req': int[1 bit] -- Reflects the 25G KR FEC capability request 
                'rs_fec544_req' : int[1 bit] -- Reflects the RS FEC 544 capability request 
                'no_fec_abil': int[1 bit] --Reflects the No FEC capability for AUI modes
                'rs_fec528_abil' : int[1 bit] -- Reflects the RS FEC 528 capability advertisement
                '25g_kr_fec_abil' : int[1 bit] --Reflects the 25G KR FEC capability advertisement
                'll_rc_fec272_50g_abil': int[1 bit] -- Reflects the LL RS FEC 272 capability advertisement for 50G KR/CR
                'll_rc_fec272_100g_abil': int[1 bit] --Reflects the LL RS FEC 272 capability advertisement for 100G KR2/CR2
                'll_rc_fec272_200g_abil' : int[1 bit] -- Reflects the LL RS FEC 272 capability advertisement for 200G KR4/CR4
                'll_rc_fec272_req' : int[1 bit] --Reflects the LL RS FEC 272 capability request for 50G KR/CR, 100G KR2/CR2 and 200G KR4/CR4
                'sff_extended_comp_code': int[1 byte] -- Returns the extended compliance code of the module as defined in SFF specifications
                'sff_module_ident': int[1 byte] --Returns the SFF module identifier as defined by the SFF specifications  
                'sff_module_type' : int[1 byte] --0 SFP+ Cu Passive , 1 SFP+ Cu Active, 4 10G Base-SR, 5 10G Base-LR, 6 10G Base-LRM, 7 10G Base-ER
                'sff_gbe_comp_code' : int[1 byte] --Returns the GbE Compliance Code as defined by the SFF sepcifications 
                'cage_type': int[3 bit] -- 0 NO Cage, 1 SEF+/SFP28, 2 QSFP+/QSFP28
        '''
        buffer = list()
        byte_0 = args["logical_prt_num"] & 0xff
        byte_2 = (args["link_restart"] << 1) & 0xff
        buffer.append(byte_0)
        buffer.append(byte_2)
        # Get PHY Capabilities Command Outputs:
        data = dict()
        data['logical_prt_num'] = compose_num_from_array_slice(buffer, 0, 1)
        data['phy_type_0'] = compose_num_from_array_slice(buffer, 4, 4)
        data['phy_type_1'] = compose_num_from_array_slice(buffer, 8, 4)
        data['phy_type_2'] = compose_num_from_array_slice(buffer, 12, 4)
        data['phy_type_3'] = compose_num_from_array_slice(buffer, 16, 4)
        data['phy_types'] = compose_num_from_array_slice(buffer, 4, 16)
        data['tx_pause_abil'] = (compose_num_from_array_slice(buffer, 20, 1) & 0x1) 
        data['rx_pause_abil'] = (compose_num_from_array_slice(buffer, 20, 1) & 0x2) >> 1 
        data['low_pwr_mod'] = (compose_num_from_array_slice(buffer, 20, 1) & 0x4) >> 2 
        data['link_mode'] = (compose_num_from_array_slice(buffer, 20, 1) & 0x8) >> 3 
        data['lesm_en'] = (compose_num_from_array_slice(buffer, 20, 1) & 0x40) >> 6 
        data['auto_fec_en'] = (compose_num_from_array_slice(buffer, 20, 1) & 0x80) >> 7 
        data['lplu_en'] = (compose_num_from_array_slice(buffer, 21, 1) & 0x1) 
        data['an_28_en'] = (compose_num_from_array_slice(buffer, 21, 1) & 0x2) >> 1 
        data['an_73_en'] = (compose_num_from_array_slice(buffer, 21, 1) & 0x4) >> 2 
        data['an_37_en'] = (compose_num_from_array_slice(buffer, 21, 1) & 0x8) >> 3 
        data['phy_id'] = compose_num_from_array_slice(buffer, 26, 4) # PHY ID/ SFF Vendor OUI
        data['phy_fw_version'] = compose_num_from_array_slice(buffer, 30, 8)
        data['10g_kr_fec_abil'] = (compose_num_from_array_slice(buffer, 38, 1) & 0x1)
        data['10g_kr_fec_req'] = (compose_num_from_array_slice(buffer, 38, 1) & 0x2) >> 1 
        data['rs_fec528_req'] = (compose_num_from_array_slice(buffer, 38, 1) & 0x4) >> 2 
        data['25g_kr_fec_req'] = (compose_num_from_array_slice(buffer, 38, 1) & 0x8) >> 3 
        data['rs_fec544_req'] = (compose_num_from_array_slice(buffer, 38, 1) & 0x10) >> 4 
        data['no_fec_abil'] = (compose_num_from_array_slice(buffer, 38, 1) & 0x20) >> 5 
        data['rs_fec528_abil'] = (compose_num_from_array_slice(buffer, 38, 1) & 0x40) >> 6 
        data['25g_kr_fec_abil'] = (compose_num_from_array_slice(buffer, 38, 1) & 0x80) >> 7 
        data['ll_rc_fec272_50g_abil'] = (compose_num_from_array_slice(buffer, 39, 1) & 0x2) >> 1 
        data['ll_rc_fec272_100g_abil'] = (compose_num_from_array_slice(buffer, 39, 1) & 0x4) >> 2
        data['ll_rc_fec272_200g_abil'] = (compose_num_from_array_slice(buffer, 39, 1) & 0x8) >> 3 
        data['ll_rc_fec272_req'] = (compose_num_from_array_slice(buffer, 39, 1) & 0x10) >> 4 
        data['sff_extended_comp_code'] = compose_num_from_array_slice(buffer, 40, 1)
        data['sff_module_ident'] = compose_num_from_array_slice(buffer, 41, 1)
        data['sff_module_type'] = compose_num_from_array_slice(buffer, 42, 1)
        data['sff_gbe_comp_code'] = compose_num_from_array_slice(buffer, 43, 1)
        data['cage_type'] = (compose_num_from_array_slice(buffer, 45, 1) & 0x7) << 5

    def GetLinkStatus(self, args, debug = False):
        '''
            Get the current status of a port
            input:
                args -- type(dict)
                    'logical_prt_num' : int[1 byte] -- Logical Port Number
            returns: 
                data -- type(dict)
                    'logical_prt_num' : int[1 byte] -- Logical Port Number
                    'topologe_and_media_conflicts' : int[i byte] -- 1 Unresolved media conflict detects, 
                                                                    2 LOM topology,
                                                                    5 Topology net-list load detected underutilized port
                                                                    6 Topology net-list load detected underutilized media
                                                                    7 Unsuported media detected
                    'link_config_error' :  int[i bit] -- 0 No error, 1 link config error
                    'module_pwr_error'  :  int[i bit] -- 0 current module power consumption  is below the allowed, 1 current module power consumption  is exceeds the allowed
                    'link_status' : int [i bit] -- 0 link down , 1 link up
                    'link_fault'  : int [4 bit] -- 0001 PHY has detected  a local fault
                                                   0010 transmit link fault
                                                   0100  receive link fault
                                                   1000 remote fault
                    'phy_link_status' :  int [i bit] -- 0 link down , 1 link up
                    'media_available': int [i bit] -- 1 media is available
                    'signal_detect': int [i bit] -- 1 receive signal is detected
                    'an_completed': int [i bit] -- 1  auto-negotiation completed successfully
                    'lp_an_ability': int [i bit] -- 1 link partner is able to perform auto-negotiation
                    'parallel_detection_fault': int [i bit] -- 1 PHY detects parallel detection fault 
                    'fec_enabled': int [i bit] -- 1 FEC is enabled
                    'low_pwr_state': int [i bit] -- 1  low power mode , 0 High power mode
                    'tx_pause_status': int [i bit] -- 1 TX link pause is anabled
                    'rx_pause_status': int [i bit] -- 1 RX link pause is anabled
                    'phy_temp_alarm': int [i bit] -- 1 temperature alarm condition is reported by the PHY
                    'excessive_link_errors': int [i bit] -- 1 an excessive errors over the link condition is reported
                    'port_tx_suspended':int [2 bit] -- 0 Port's Tx active , 1 Port's Tx suspended and drained
                    'loopback_status': int [6 bit] -- 0 PHY local loopback , 1 PHY remote, 2 MAC local, [3:5] PHY index to perform loopback 
                    'max_frame_size' : int [2 byte] -- maximum frame size
                    'kr_fec_enabled' : int [1 bit] -- 1 KR FEC was negotiated on the link 
                    'rs_fec528_enabled' : int [1 bit] -- 1 RS FEC 528 was negotiated on the link
                    'rs_fec544_enabled' : int [1 bit] -- 1 RS FEC 544 was negotiated on the link
                    'pacing_config' : int [5 bit] -- first 4 bits- enables configuring an average rate pace parameter, bit 5 - 0 Data rate pacing / 1 Fixed IPG pacing
                    'sff_module_pwr': int [1 byte] -- Reflects the SFP+/SFP28/QSFP+/QSFP28 module power in 0.5 W increments
                    'current_link_speed': int [2 byte] --Current Link Speed
                    'link_config_error_code': int [2 byte] -- reflects the error code returned by the Dreadnought Lake (DNL) scripts 
                    'rs_fec272_enabled': int [1 bit] -- 1 LL RS FEC 272 was negotiated on the link
                    'link_attempt_counter': int [1 byte] -- number of iterations the Link Establishment State Machine has made since the last Setup Link
                    'current_phy_type' : int [4 byte] -- PHY types
                    'link_partners_phy_types' : int [4 byte] --The Phy types advertised by the link parnter
                    'link_part_10g_kr_fec_abil' : int [1 bit] -- Reflects the Link Partner's 10G KR FEC capability advertisement 
                    'link_part_25g_kr_fec_abil' : int [1 bit] -- Reflects the Link Partner's 25G KR FEC capability advertisement
                    'link_part_rs_fec528_abil': int [1 bit] -- Reflects the Link Partner's RS FEC 528 capability
                    'link_part_ll_rs_fec272_50g_abil': int [1 bit] -- Reflects the Link Partner's LL RS FEC 272 capability advertisement for 50G KR/CR
                    'link_part_ll_rs_fec272_100g_abil' : int [1 bit] --Reflects the Link Partner's LL RS FEC 272 capability advertisement for 100G KR2/CR2
                    'link_part_ll_rs_fec272_200g_abil' : int [1 bit] --Reflects the Link Partner's LL RS FEC 272 capability advertisement for 200G KR4/CR4
                    'link_part_10g_kr_fec_req' : int [1 bit] --Reflects the Link Partner's 10G KR FEC capability request
                    'link_part_25g_kr_fec_req': int [1 bit] -- Reflects the Link Partner's 25G KR FEC capability request
                    'link_part_rs_fec528_req'  : int [1 bit] --Reflects the Link Partner's RS FEC 528 capability request
                    'link_part_ll_rs_fec272_req': int [1 bit] -- Reflects the Link Partner's LL RS FEC 272 capability request for 50G KR/CR, 100G KR2/CR2 and 200G KR4/CR4
                   
        '''
        port = args["logical_prt_num"] & 0xff
        # Get Link Status Command Outputs
        data = dict()
        data['logical_prt_num'] = compose_num_from_array_slice(buffer, 0, 1)
        data['topologe_and_media_conflicts'] = compose_num_from_array_slice(buffer,4, 1)      
        data['link_config_error'] = (compose_num_from_array_slice(buffer, 5, 1) & 0x1)
        data['module_pwr_error'] = (compose_num_from_array_slice(buffer, 5, 1) & 0x20) >> 5 
        data['link_status'] = (compose_num_from_array_slice(buffer, 6, 1) & 0x1)
        data['link_fault'] = (compose_num_from_array_slice(buffer, 6, 1) & 0xf) << 4
        data['phy_link_status'] = (compose_num_from_array_slice(buffer, 6, 1) & 0x20) >> 5 
        data['media_available'] = (compose_num_from_array_slice(buffer, 6, 1) & 0x40) >> 6 
        data['signal_detect'] = (compose_num_from_array_slice(buffer, 6, 1) & 0x80) >> 7 
        data['an_completed'] = (compose_num_from_array_slice(buffer, 7, 1) & 0x1)
        data['lp_an_ability'] = (compose_num_from_array_slice(buffer, 7, 1) & 0x2) >> 1 
        data['parallel_detection_fault'] = (compose_num_from_array_slice(buffer, 7, 1) & 0x4) >> 2 
        data['fec_enabled'] = (compose_num_from_array_slice(buffer, 7, 1) & 0x8) >> 3 
        data['low_pwr_state'] = (compose_num_from_array_slice(buffer, 7, 1) & 0x10) >> 4 
        data['tx_pause_status'] = (compose_num_from_array_slice(buffer, 7, 1) & 0x20) >> 5 
        data['rx_pause_status'] = (compose_num_from_array_slice(buffer, 7, 1) & 0x40) >> 6  
        data['phy_temp_alarm'] = (compose_num_from_array_slice(buffer, 8, 1) & 0x1)
        data['excessive_link_errors'] = (compose_num_from_array_slice(buffer, 8, 1) & 0x2) >> 1 
        data['port_tx_suspended'] = (compose_num_from_array_slice(buffer, 8, 1) & 0xc) >> 2 
        data['loopback_status'] = (compose_num_from_array_slice(buffer, 9, 1) & 0x3f)  
        data['max_frame_size'] = compose_num_from_array_slice(buffer, 10, 2)  
        data['kr_fec_enabled'] = (compose_num_from_array_slice(buffer, 12, 1) & 0x1)
        data['rs_fec528_enabled'] = (compose_num_from_array_slice(buffer, 12, 1) & 0x2) >> 1 
        data['rs_fec544_enabled'] = (compose_num_from_array_slice(buffer, 12, 1) & 0x4) >> 2 
        data['pacing_config'] = (compose_num_from_array_slice(buffer, 12, 1) & 0xf8) >> 3 
        data['sff_module_pwr'] = (compose_num_from_array_slice(buffer, 13, 1) & 0x3f) 
        data['current_link_speed'] = compose_num_from_array_slice(buffer, 14, 2) 
        data['link_config_error_code'] = compose_num_from_array_slice(buffer, 16, 2)
        data['rs_fec272_enabled'] = (compose_num_from_array_slice(buffer, 18, 1) & 0x1)
        data['link_attempt_counter'] = compose_num_from_array_slice(buffer, 19, 1)
        data['current_phy_type'] = compose_num_from_array_slice(buffer, 20, 16)
        data['link_partners_phy_types'] = compose_num_from_array_slice(buffer, 36 16)
        data['link_part_10g_kr_fec_abil'] = (compose_num_from_array_slice(buffer, 52, 1) & 0x1)
        data['link_part_25g_kr_fec_abil'] = (compose_num_from_array_slice(buffer, 52, 1) & 0x2) >> 1 
        data['link_part_rs_fec528_abil'] = (compose_num_from_array_slice(buffer, 52, 1) & 0x4) >> 2 
        data['link_part_ll_rs_fec272_50g_abil'] = (compose_num_from_array_slice(buffer, 52, 1) & 0x8) >> 3 
        data['link_part_ll_rs_fec272_100g_abil'] = (compose_num_from_array_slice(buffer, 52, 1) & 0x10) >> 4 
        data['link_part_ll_rs_fec272_200g_abil'] = (compose_num_from_array_slice(buffer, 52, 1) & 0x20) >> 5 
        data['link_part_10g_kr_fec_req'] = (compose_num_from_array_slice(buffer, 53, 1) & 0x1)
        data['link_part_25g_kr_fec_req'] = (compose_num_from_array_slice(buffer, 53, 1) & 0x2) >> 1 
        data['link_part_rs_fec528_req'] = (compose_num_from_array_slice(buffer, 53, 1) & 0x4) >> 2 
        data['link_part_ll_rs_fec272_req'] = (compose_num_from_array_slice(buffer, 53, 1) & 0x8) >> 3 

    def SetPhyLoopback(self, args, debug = False):
        '''
            sets the PHY to a loopback mode
                input:
                    args -- type(dict)
                        'logical_prt_num' : int[1 byte] -- Logical Port Number
                        'phy_index' : int[1 byte] -- the requested phy index
                        'loopback_level' : int[1 bit] -- 0 PMD level, 1 PCS level
                        'loopback_type'  : int[1 bit] -- 0 local (host side) , 1 Remote (line side)
                        'loopback_enable' : int[1 bit] -- 0 turn off , 1 turn on
        '''
        buffer = list()
        byte_0 = args["logical_prt_num"] & 0xff
        byte_2 = args["phy_index"] & 0xff
        byte_3 = (args["loopback_level"] << 2) | (args["loopback_type"] << 1) | args["loopback_enable"]
        buffer.append(byte_0)
        buffer.append(byte_2)
        buffer.append(byte_3)

    def SetMacLoopback(self, args, debug = False):
        '''
            sets the MAC to a loopback mode
             input:
                    args -- type(dict)
                        'logical_prt_num' : int[1 byte] -- Logical Port Number
                        'loopback_enable' : int[1 bit] -- 0 turn off , 1 turn on
        '''
        buffer = list()
        byte_0 = args["logical_prt_num"] & 0xff
        byte_1 = args["loopback_enable"] & 0x1
        buffer.append(byte_0)
        buffer.append(byte_1)


    def SetPhyDebug(self, args, debug = False):
        '''
            resets the PHY, enables/disables the ENI link Manager
             input:
                    args -- type(dict)
                        'logical_prt_num' : int[1 byte] -- Logical Port Number
                        'phy_index' : int[1 byte] -- the requested phy index
                        'phy_reset' :  int[3 bit] -- PHY reset type: 0 Nop, 1 Hard reset, 2 soft reset
                        'en_link_manager_port_disable' : int[1 bit] -- 0 Enable ENI link , 1 Disable ENI link (for specified port)
                        'en_link_manager_all_disable' : int[1 bit] --  0 Enable ENI link , 1 Disable ENI link (for all ports)
        '''

        buffer = list()
        byte_0 = args["logical_prt_num"] & 0xff
        byte_1 = args["logical_prt_num"] & 0x1
        byte_2 = args["phy_index"] & 0xff
        byte_3 = (args["en_link_manager_all_disable"] << 4) | (args["en_link_manager_port_disable"] << 3) | args["phy_reset"]
        buffer.append(byte_0)
        buffer.append(byte_1)
        buffer.append(byte_2)
        buffer.append(byte_3)



    def GetPhyDebug(self, args, debug = False):
        '''
            returns the state of the ENI link manger
            input:
                    args -- type(dict)
                        'logical_prt_num' : int[1 byte] -- Logical Port Number
                        'en_link_manager_port_disable' : int[1 bit] -- 0 Enable ENI link , 1 Disable ENI link (for specified port)
                        'en_link_manager_all_disable' : int[1 bit] --  0 Enable ENI link , 1 Disable ENI link (for all ports)
        '''
        buffer = list()
        byte_0 = args["logical_prt_num"] & 0xff
        byte_3 = (args["en_link_manager_all_disable"] << 4) | (args["en_link_manager_port_disable"] << 3) 
        buffer.append(byte_0)
        buffer.append(byte_3)

