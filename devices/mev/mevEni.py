
class mevEni:
    
    def __init__(self, driver):
        self.driver = driver


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
        buffer = list()
        byte_0 = args["logical_prt_num"] & 0xff
        byte_2 = (args["link_enable"] << 2) | (args["link_restart"] << 1)
        buffer.append(byte_0)
        buffer.append(byte_2)

    def GetPhyCapabilities(self, args, debug = False):
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
        buffer = list()
        byte_0 = args["logical_prt_num"] & 0xff
        byte_2 = args["phy_index"] & 0xff
        byte_3 = (args["loopback_level"] << 2) | (args["loopback_type"] << 1) | args["loopback_enable"]
        buffer.append(byte_0)
        buffer.append(byte_2)
        buffer.append(byte_3)

    def SetMacLoopback(self, args, debug = False):
        buffer = list()
        byte_0 = args["logical_prt_num"] & 0xff
        byte_1 = args["loopback_enable"] & 0x1
        buffer.append(byte_0)
        buffer.append(byte_1)


    def SetPhyDebug(self, args, debug = False):
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
        buffer = list()
        byte_0 = args["logical_prt_num"] & 0xff
        byte_3 = (args["en_link_manager_all_disable"] << 4) | (args["en_link_manager_port_disable"] << 3) 
        buffer.append(byte_0)
        buffer.append(byte_3)

