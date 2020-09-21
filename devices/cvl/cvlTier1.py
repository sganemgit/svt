from core.utilities.BitManipulation import *
from devices.cvl.cvlDefines import cvlDefines
from core.structs.AqDescriptor import AqDescriptor
from devices.cvl.temp import *


class cvlTier1(cvlDefines):

    ###############################################################################
    #                                Admin Queue Commands                         #
    ###############################################################################

    def SetPhyConfig(self, config, debug=False):
        # Updated for HAS 1.3
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
        # Generic AQ descriptor --> Set PHY Config Admin command translation
        aq_desc = AqDescriptor()
        buffer = list()
        # Add PHY Type to buffer (bytes 0-15)
        buffer.extend(turn_arg_to_bytes(config['phy_type_0']))
        buffer.extend(turn_arg_to_bytes(config['phy_type_1']))
        buffer.extend(turn_arg_to_bytes(config['phy_type_2']))
        buffer.extend(turn_arg_to_bytes(config['phy_type_3']))
        byte_16 = (config['auto_fec_en'] << 7) | (config['lesm_en'] << 6) | (config['en_auto_update'] << 5) | (
                    config.get('an_mode', 0) << 4) | (config['en_link'] << 3) | (config['low_pwr_abil'] << 2) | (
                              config['rx_pause_req'] << 1) | config['tx_pause_req']
        byte_17 = config['low_pwr_ctrl'] & 0xff
        byte_18 = config['eee_cap_en'] & 0xff
        byte_19 = (config['eee_cap_en'] >> 8) & 0xff
        byte_20 = config['eeer'] & 0xff
        byte_21 = (config['eeer'] >> 8) & 0xff
        byte_22 = (config['fec_firecode_25g_abil'] << 7) | (config['fec_rs528_abil'] << 6) | (
                    config['fec_rs544_req'] << 4) | (config['fec_firecode_25g_req'] << 3) | (
                              config['fec_rs528_req'] << 2) | (config['fec_firecode_10g_req'] << 1) | config[
                      'fec_firecode_10g_abil']
        byte_23 = 0 & 0xFF  # FW requires buffer to be 24 bytes long, appending empty byte at the end of data structure to achieve this
        buffer.append(byte_16)
        buffer.append(byte_17)
        buffer.append(byte_18)
        buffer.append(byte_19)
        buffer.append(byte_20)
        buffer.append(byte_21)
        buffer.append(byte_22)
        buffer.append(byte_23)
        buffer.extend([0] * (0x100 - len(buffer)))
        aq_desc.opcode = 0x0601
        aq_desc.flags = 0x1400  # Include buffer and read flags for this command
        aq_desc.param0 = config['port']
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.datalen = len(buffer)
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Set PHY Config Admin Command, status: {} , FW ret value: {}'.format(status,
                                                                                                      aq_desc.retval))
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)

        return status

    def SetMacConfig(self, config, debug=False):
        # Update for HAS 1.3
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
        byte_6 = config['fc_refr_thresh'] & 0xff
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
            print('Failed to send Set MAC Config Admin Command, status: {}, FW ret value: {}'.format(status,
                                                                                                     aq_desc.retval))
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)
        return status

    def SetupLink(self, slu_args, debug=False):
        # Updated for HAS 1.3
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
        # Generic AQ descriptor --> Setup Link and Retart Auto-negotiation Admin command translation
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
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)
        return status

    def GetPhyAbilities(self, get_abils, debug=False):
        # Updated for HAS 1.3
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

        # Generic AQ descriptor --> Get PHY Abilities Admin command translation
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
        aq_desc.flags = 0x1200  # Set the buffer flag & long buffer flag
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Get PHY Abilities Admin Command, status: ', status, ', FW ret value: ',
                  aq_desc.retval)
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            # The static section of Get PHY Abilities is 32 bytes
            # ut.compose_num_from_array_slice(input, index, width)
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
            # TODO: change code base to not rely on this field. This Field will be deleted
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
            # TODO: remove these fiedlds from code
            data['mod_id'] = compose_num_from_array_slice(buffer, 37, 1)  # TODO to be deleted
            data['mod_sfp_cu_passive'] = compose_num_from_array_slice(buffer, 38, 1) & 0x1  # TODO to be deleted
            data['mod_sfp_cu_active'] = (compose_num_from_array_slice(buffer, 38, 1) & 0x2) >> 1  # TODO to be deleted
            data['mod_10g_sr'] = (compose_num_from_array_slice(buffer, 38, 1) & 0x10) >> 4  # TODO to be deleted
            data['mod_10g_lr'] = (compose_num_from_array_slice(buffer, 38, 1) & 0x20) >> 5  # TODO to be deleted
            data['mod_10g_lrm'] = (compose_num_from_array_slice(buffer, 38, 1) & 0x40) >> 6  # TODO to be deleted
            data['mod_10g_er'] = (compose_num_from_array_slice(buffer, 38, 1) & 0x80) >> 7  # TODO to be deleted
            data['mod_1g_comp_code'] = compose_num_from_array_slice(buffer, 39, 1)  # TODO to be deleted

            data['qual_mod_count'] = compose_num_from_array_slice(buffer, 40, 1)
            data['qual_mod_ids'] = 0  # TODO - read CVL HAS TABLE:3-104
            status = (False, data)
        return status

    def GetLinkStatus(self, gls, debug=False):
        # Updated for HAS 1.3
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
        # Generic AQ descriptor --> Get Link Status Admin command translation
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
        aq_desc.flags = 0x1200  # Set the buffer and long buffer flags
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Get Link Status Admin Command, status: ', status, ', FW ret value: ', aq_desc.retval)
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            # The static section of Get PHY Abilities is 32 bytes
            # ut.compose_num_from_array_slice(input, index, width)
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

            data['pacing_type'] = (compose_num_from_array_slice(buffer, 8, 1) & 0x80) >> 7  # TODO - to be deleted
            data['pacing_rate'] = (compose_num_from_array_slice(buffer, 8, 1) & 0x78) >> 3  # TODO - to be deleted
            data['current_link_speed'] = compose_num_from_array_slice(buffer, 10, 2)

            data['link_speed_10m'] = compose_num_from_array_slice(buffer, 10, 1) & 0x1  # TODO - to be deleted
            data['link_speed_100m'] = (compose_num_from_array_slice(buffer, 10, 1) & 0x2) >> 1  # TODO - to be deleted
            data['link_speed_1000m'] = (compose_num_from_array_slice(buffer, 10, 1) & 0x4) >> 2  # TODO - to be deleted
            data['link_speed_1000m'] = (compose_num_from_array_slice(buffer, 10, 1) & 0x4) >> 2  # TODO - to be deleted
            data['link_speed_2p5g'] = (compose_num_from_array_slice(buffer, 10, 1) & 0x8) >> 3  # TODO - to be deleted
            data['link_speed_5g'] = (compose_num_from_array_slice(buffer, 10, 1) & 0x10) >> 4  # TODO - to be deleted
            data['link_speed_10g'] = (compose_num_from_array_slice(buffer, 10, 1) & 0x20) >> 5  # TODO - to be deleted
            data['link_speed_20g'] = (compose_num_from_array_slice(buffer, 10, 1) & 0x40) >> 6  # TODO - to be deleted
            data['link_speed_25g'] = (compose_num_from_array_slice(buffer, 10, 1) & 0x80) >> 7  # TODO - to be deleted
            data['link_speed_40g'] = compose_num_from_array_slice(buffer, 11, 1) & 0x1  # TODO - to be deleted
            data['link_speed_50g'] = (compose_num_from_array_slice(buffer, 11, 1) & 0x2) >> 1  # TODO - to be deleted
            data['link_speed_100g'] = (compose_num_from_array_slice(buffer, 11, 1) & 0x4) >> 2  # TODO - to be deleted
            data['link_speed_200g'] = (compose_num_from_array_slice(buffer, 11, 1) & 0x8) >> 3  # TODO - to be deleted

            data['phy_type_0'] = compose_num_from_array_slice(buffer, 16, 4)
            data['phy_type_1'] = compose_num_from_array_slice(buffer, 20, 4)
            data['phy_type_2'] = compose_num_from_array_slice(buffer, 24, 4)
            data['phy_type_3'] = compose_num_from_array_slice(buffer, 28, 4)
            data['phy_type'] = compose_num_from_array_slice(buffer, 16, 16)

            phy_type_list = []  # TODO - to be deleted
            phy_type_list.extend(get_all_phy_types(data['phy_type_0'], 0))  # TODO - to be deleted
            phy_type_list.extend(get_all_phy_types(data['phy_type_1'], 1))  # TODO - to be deleted
            phy_type_list.extend(get_all_phy_types(data['phy_type_2'], 2))  # TODO - to be deleted
            phy_type_list.extend(get_all_phy_types(data['phy_type_3'], 3))  # TODO - to be deleted
            data['phy_type_list'] = phy_type_list  # TODO - to be deleted

            status = (False, data)
        return status

    def SetPhyLoopback(self, phy_lpbk_args, debug=False):
        # Updated for HAS 1.3
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
        # Generic AQ descriptor --> Set PHY Loopback Admin command translation
        # e.g. descriptor_term = (most_significant bytes .. least_significant_bytes)
        # param0 = (level + type + enable + phy_index + logical_port_number)
        # param1 = (0)
        # addr_high = (0)
        # addr_low = (0)
        # helper = LM_Validation()
        aq_desc = AqDescriptor()  # helper._debug('SetPhyLoopback Admin Command')
        data_len = 0x0
        aq_desc.opcode = 0x0619
        aq_desc.datalen = data_len
        buffer = [0] * data_len
        aq_desc.param0 = (phy_lpbk_args['level'] << 26) | (phy_lpbk_args['type'] << 25) | (
                    phy_lpbk_args['enable'] << 24) | (phy_lpbk_args['index'] << 16) | phy_lpbk_args['port']
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.flags = 0x0

        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Set Phy Loopback Admin Command, status: ', status, ', FW ret value: ', aq_desc.retval)
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)
        return status

    def SetPhyDebug(self, debug_args, debug=False):
        # Updated for HAS 1.3
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

        # helper = LM_Validation()
        aq_desc = AqDescriptor()
        # helper._debug('SetPhyDebug Admin Command')
        data_len = 0x0
        aq_desc.opcode = 0x0622
        aq_desc.datalen = data_len
        buffer = [0] * data_len
        aq_desc.param0 = (debug_args['cmd_flags'] << 24) | (debug_args['index'] << 16) | debug_args['port']
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.flags = 0x0

        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Set Phy Debug Admin Command, status: ', status, ', FW ret value: ', aq_desc.retval)
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)
        return status

    def SetMacLoopback(self, args, debug=False):
        '''
            This method sends a Set MAC Loopback addmin command
        '''
        aq_desc = AqDescriptor()
        data_len = 0x0
        aq_desc.opcode = 0x0620
        aq_desc.datalen = data_len
        buffer = [0] * data_len
        aq_desc.param0 = args["loopback mode"]
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.flags = 0x0

        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Set Phy Loopback Admin Command, status: ', status, ', FW ret value: ', aq_desc.retval)
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)
        return status

    def DisableLldp(self, shutdown=0, persistent=0, debug=0):
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
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)

    def EnableLldp(self, persistent=0, debug=0):
        driver = self.driver
        # helper = LM_Validation()
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
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)

    ######################################################################################################
    ###############################           Debug section             ##################################
    ######################################################################################################

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

        self.driver.send_aq_command(aq_desc,buffer)

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

    def _DnlCallActivity(self, activity_id, context, sto_0, sto_1, sto_2, sto_3, debug=False):
        '''
            This function is an indirect admin command used to call a DNL activity in the specified context.
            arguments:
                activity_id - The ID of the activity to be called
                context - port number
                sto_0, sto_1, sto_2, sto_3
            return: tuple contain-- sto_0, sto_1, sto_2, sto_3
        '''
        param0 = 0  # Activity id - 2 bytes, reserved - 1 byte, context 1 byte
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

        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send DNL CALL ACTIVITY AQ command, status:', status, ', FW ret value: ', aq_desc.retval)

        sto_0 = compose_num_from_array_slice(buffer, 0, 4)
        sto_1 = compose_num_from_array_slice(buffer, 4, 4)
        sto_2 = compose_num_from_array_slice(buffer, 8, 4)
        sto_3 = compose_num_from_array_slice(buffer, 12, 4)

        return (sto_0, sto_1, sto_2, sto_3)

    def _DnlReadPstore(self, context, psto_index_to_read, debug=False):
        '''
            Function that returns the value of the specific PSTO requested
            arguments:
                context - context number
                pstores_number_to_read - PSTO number to read
            return: pstores
        '''
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
        aq_desc.param0 = psto_select | context  # byte 16 - context, 17 - store select

        buffer = [0] * data_len

        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send DNL READ STORE AQ command, status:', status, ', FW ret value: ', aq_desc.retval)

        pstores = []
        index = 0
        for i in range(0, psto_actual_index):
            pstores.append(compose_num_from_array_slice(buffer, index, psto_size))
            index += psto_size

        return pstores[-1]

    def _DnlWriteStore(self, context, store_type, store_index, value, debug=False):
        '''
            Function that write the value to specific PSTO.
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

        store_index = (store_index & 0xffff) << 16
        sto_select = (sto_select & 0xff) << 8
        context = context & 0xff

        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x684
        aq_desc.param0 = store_index | sto_select | context  # byte 16 - context, 17 - store select, 18:19 - offset
        aq_desc.param1 = value & 0xffffffff

        status = driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send DNL WRITE STORE AQ command, status:', status, ', FW ret value: ', aq_desc.retval)

    #########################################################################################################
    ######################           Support SECTION               ##########################################
    #########################################################################################################

    def _NeighborDeviceRequestAq(self, opcode,Massage):
        '''
            this function support Neighbor Device Request via AQ (CVL spec B.2.1.2)
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
        aq_desc = AqDescriptor()
        byte16 = 0x0
        byte18 = 0x0
        if enable:
            byte16 = 0x1  # bit 0 is 1 to enable AQ logging
            byte18 = 0x1
            # print "enable configure_logging_dnl"
        else:
            byte16 = 0x0  # bit 0 is 1 to enable AQ logging
            byte18 = 0x1
            # print "disable configure_logging_dnl"
        param0 = (byte18 & 0xff) << 16
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

        status = self.driver.send_aq_command(aq_desc, buf)
        if status != 0 or aq_desc.retval != 0:
            raise RuntimeError(
                'Failed to configure logging, failed to send aq command, status={}, retval={}'.format(status,
                                                                                                      aq_desc.retval))

        # print 'configure logging aq command has been sent successfully'

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

    def WriteI2C(self, port, node_handle, memory_offset, data):
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
        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x6E3
        aq_desc.flags = 0
        aq_desc.datalen = 0
        aq_desc.param0 = (0x2 << 20 | 0x6 << 16 | 1 << 8 | port)
        aq_desc.param1 = 0
        aq_desc.param1 = (memory_offset << 16 | node_handle)
        aq_desc.addr_high = 0
        I2C_data = data & 0xff
        aq_desc.addr_high = (I2C_data << 8 | 1)
        aq_desc.addr_low = 0
        buffer = []
        status = self.driver.send_aq_command(aq_desc)
        return [status, aq_desc.retval]