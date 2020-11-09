
from core.utilities.BitManipulation import *
from core.structs.AqDescriptor import AqDescriptor
from devices.cvl.temp import *

class AdminCommandHandler:
    '''
        This class handles sending Admin commnads to CVL
        this class depends only on the driver object. no other dependencies should be interduces
    '''
    def __init__(self, driver_reference):
        self.driver = driver_reference

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
        byte_16 = (config['auto_fec_en'] << 7) | (config['lesm_en'] << 6) | (config['en_auto_update'] << 5) | (config.get('an_mode', 0) << 4) | (config['en_link'] << 3) | (config['low_pwr_abil'] << 2) | (config['rx_pause_req'] << 1) | config['tx_pause_req']
        byte_17 = config['low_pwr_ctrl'] & 0xff
        byte_18 = config['eee_cap_en'] & 0xff
        byte_19 = (config['eee_cap_en'] >> 8) & 0xff
        byte_20 = config['eeer'] & 0xff
        byte_21 = (config['eeer'] >> 8) & 0xff
        byte_22 = (config['fec_firecode_25g_abil'] << 7) | (config['fec_rs528_abil'] << 6) | (config['fec_rs544_req'] << 4) | (config['fec_firecode_25g_req'] << 3) | (config['fec_rs528_req'] << 2) | (config['fec_firecode_10g_req'] << 1) | config['fec_firecode_10g_abil']
        byte_23 = config.get('module_compliance_mode',1)
        buffer.append(byte_16)
        buffer.append(byte_17)
        buffer.append(byte_18)
        buffer.append(byte_19)
        buffer.append(byte_20)
        buffer.append(byte_21)
        buffer.append(byte_22)
        buffer.append(byte_23)
        buffer.extend([0] * (0x1000 - len(buffer)))
        aq_desc.opcode = 0x0601
        aq_desc.flags = 0x1600  # Include buffer and read flags for this command
        aq_desc.param0 = config['port']
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.datalen = len(buffer)
        status = self.driver.send_aq_command(aq_desc, buffer, debug, False)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Set PHY Config Admin Command, status: {} , FW ret value: {}'.format(status, aq_desc.retval))
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
        status = self.driver.send_aq_command(aq_desc, buffer, debug, False)
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
            data['module_compliance_enforcement'] = compose_num_from_array_slice(buffer, 35, 1) & 0x1 #from CPK DCR 102 aka persistent mode
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
        aq_desc.param0 = (gls.get('cmd_flag', 0) << 16) | gls.get('port', 0)
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

    def NeighborDeviceRead(self, dest,opcode,addrlen, address):
        '''
            this function support Neighbor Device Request via AQ (CVL spec B.2.1.2)
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

        return_buffer = self.NeighborDeviceRequestAq(1,buffer)
        return_val = hex((return_buffer[7] << 24) | (return_buffer[6] << 16) | (return_buffer[5] << 8) |return_buffer[4])# print second DW
        #print "return val: ", return_val
        return return_val.replace("L","")

###############################################################################
#                          LLDP admin commands                                #
###############################################################################

    def StopLldpAgent(self, shutdown=0, persistent=0, debug=0):
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
            print('Failed to send Stop LLDP Agent admin command status: ', status, ', FW ret value: ', aq_desc.retval)
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)

    def StartLldpAgent(self, persistent=0, debug=0):
        driver = self.driver
        aq_desc = AqDescriptor()
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
            print('Failed to send Start LLDP Agent admin command status: ', status, ', FW ret value: ', aq_desc.retval)
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

        self.driver.send_aq_command(aq_desc, buffer, debug)

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
#                                  DNL section                                                       # 
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

    def NeighborDeviceRequestAq(self, opcode,Massage):
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
        else:
            byte16 = 0x0  # bit 0 is 1 to enable AQ logging
            byte18 = 0x1
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

################################################################################
#                            link topology admin commands                      #  
################################################################################

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
        aq_desc.opcode = 0x06E0
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

    def GetLinkTopologyPin(self, config, debug=False):
        '''
            input:
            config -- type(dict):
            
                'logical_prt_num' : int[2 byte] -- Logical Port Number
                'node_type_context': int[1 byte]-- the context within which the handle should be identified
                'index':int[1 byte]-- requested node index
                'node_handle' :int[2 byte]--  Reference node handle / Node handle
                'io_function': int[5 bit] --  The I/O function or number
                'io_type':  int[3 bit] --The type of the I/O
                'driving_io_number': int[5 bits] --  The driving I/O Number
              

            return:
                list --
                    list[0] - status : this the drivers return vlaue 0 = succefull admin command
                    list[1] - 
        '''
        byte_16 = config["logical_port_number"] & 0xff
        byte_17 = config.get("port_nubmer_valid", 1) & 0x1
        byte_18 = ((config.get("node_type_context", 0x2) & 0xff) << 4) | (config.get('node_type', 0x6) & 0xf)
        byte_19 = config.get("index",0) & 0xff
        byte_20 = config["node_handle"] & 0xff
        byte_21 = (config["node_handle"] >> 8) & 0x3
        byte_22 = ((config["io_type"] & 0x7) <<5) | (config["io_function"]& 0x1f)

        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x06E1
        aq_desc.flags = 0
        aq_desc.param0 = (byte_19 << 24 | byte_18 << 16 | byte_17 << 8 | byte_16)
        aq_desc.param1 = (byte_22 << 16 | byte_21 << 8 | byte_20)
        aq_desc.addr_high = 0 
        aq_desc.addr_low = 0
        buffer = []
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print("Failed to send GetLinkTopologyPin Command, status: {}, FW ret value: {}".format(status,aq_desc.retval))
        else:
            data = dict()
            data['node_handle'] = aq_desc.param1 & 0x3ff
            data['driving_io_number'] = aq_desc.param1 & 0x1f000000
            data['io_type'] = aq_desc.param1 & 0xE0000000
            data['speed'] = aq_desc.addr_high & 0x7
            data['int'] = aq_desc.addr_high & 0x18
            data['polarity'] = aq_desc.addr_high & 0x20  
            data['value'] = aq_desc.addr_high & 0x40  
            data['driven'] = aq_desc.addr_high & 0x80 
            status = (False, data)
        return status

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
        aq_desc.param0 = (0x2 << 20) | (0x6 << 16) | (1 << 8) | port
        aq_desc.param1 = 0
        aq_desc.param1 = (memory_offset << 16 | node_handle)
        aq_desc.addr_high= 0
        aq_desc.addr_high = (1 << 7 | 0xf)
        aq_desc.addr_low = 0
        buffer = []
        status  = driver.send_aq_command(aq_desc)
        data =  intgerTo4ByteList(aq_desc.param0)
        data += intgerTo4ByteList(aq_desc.param1)
        data += intgerTo4ByteList(aq_desc.addr_high)
        data += intgerTo4ByteList(aq_desc.addr_low)
        return [status,aq_desc.retval,data]

    def WriteI2C(self, config, debug=False):
        '''
            This function write 1 bytes of I2C data. see HAS Table 3-135. write  I2C admin command (Opcode: 0x06E3)
            arguments:
            config -- type(dict):
            
                'logical_prt_num' : int[2 byte] -- Logical Port Number
                'node_type_context': int[1 byte]-- the context within which the handle should be identified
                'index':int[1 byte]-- requested node index
                'node_handle' :int[2 byte]--  Reference node handle / Node handle
                'i2c_memory_offset': int[2 byte] --  I2C memory address (I2C offset) 
                'i2c_parameters':  int[1 byte] -- bit 4= I2C address type ,bit[3:0]= data size to write (1-4 bytes)
                'i2c_bus_address': int[10 bits] -- Slave address (10 bits)
                'i2c_data':int[4 byte] -- the write data (1 to 4 bytes) to be written to the I2C

            return:
                list --
                    list[0] - status : this the drivers return vlaue 0 = succefull admin command
                    list[1] - retval : this the FW return value 0 = succefull admin command
        '''
        byte_16 = config.get("logical_port_number", 0) & 0xff
        byte_17 = config.get("port_nubmer_valid", 0) & 0x1
        byte_18 = ((config.get("node_type_context", 0x2) & 0xff) << 4) | (config.get('node_type', 0x6) & 0xf)
        byte_19 = config.get("index",0) & 0xff
        byte_20 = config["node_handle"] & 0xff
        byte_21 = (config["node_handle"] >> 8) & 0x3
        byte_22 = config["i2c_memory_offset"] & 0xff
        byte_23 = (config["i2c_memory_offset"] >> 8) & 0xff
        byte_24 = ((config.get("i2c_address type", 0) & 0x1) <<4) | (config.get("data_size_to_write", 0x1)& 0xf)
        byte_26 = config.get("i2c_bus_address",0) & 0xff
        byte_27 = (config.get("i2c_bus_address", 0) >> 8) & 0x3
        byte_28 = config["i2c_data"] & 0xff
        byte_29 = (config["i2c_data"] >> 8) & 0xff
        byte_30 = (config["i2c_data"] >> 16) & 0xff
        byte_31 = (config["i2c_data"] >> 24) & 0xff

        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x6e3
        aq_desc.flags = 0
        aq_desc.param0 = (byte_19 << 24) | (byte_18 << 16) | (byte_17 << 8) | byte_16
        aq_desc.param1 = (byte_23 << 24) | (byte_22 << 16) | (byte_21 << 8) | byte_20
        aq_desc.addr_high = (byte_27 << 24) | (byte_26 << 16) | byte_24  
        aq_desc.addr_low = (byte_31 << 24) | (byte_30 << 16) | (byte_29 << 8) | byte_28
        buffer = list() 
        status = self.driver.send_aq_command(aq_desc, buffer, debug, False)
        if status != 0 or aq_desc.retval != 0:
            print("Failed to send Write I2C Command, status: {}, FW ret value: {}".format(status,aq_desc.retval))
            return (status, aq_desc.retval)
        return (status, None)

    def testGetPortOptions(self):
        config = dict()
        #config['logical_port_number'] = self.driver.port_number()
        self.GetPortOptions(config, True)

    def GetPortOptions(self, config, debug=False):
        '''
        Retrieve the available port options that are defined for the innermost PHY that is associated with the logical port number
        input:
             config -- type(dict):
            
                'logical_port_number' : int[2 byte] -- Logical Port Number
                'port_nubmer_valid':  int[1 bit] -- Logical Port number is valid

        '''
        #TODO failded to send this aq. driver reports unknow opcode 

        byte_16 = config.get("logical_port_number", 0) & 0xff
        byte_17 = config.get("port_nubmer_valid", 0) & 0x1
        buffer = [0]*0x1000

        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x06EA
        aq_desc.flags = 0x1200
        aq_desc.datalen = len(buffer)
        aq_desc.param0 = ((byte_17 & 1) << 8)| byte_16
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        status = self.driver.send_aq_command(aq_desc, buffer, debug, False)
        if status != 0 or aq_desc.retval != 0:
            raise RuntimeError("Failed to send GetPortOptions Command, status: {}, FW ret value: {}".format(status,aq_desc.retval))
        else:
            data = dict()
            data['port_options_count'] = aq_desc.param0 & 0xf0000
            data['innermost_phy_index'] = aq_desc.param0 & 0xff000000
            data['active_port_option'] = aq_desc.param1 & 0xf
            data['active_port_option_valid'] = aq_desc.param1 & 0x80
            data['active_port_option_is_forced'] = aq_desc.param1 & 0x40

    def SetPortOptioins(self, config, debug=False):
        '''
             input : config -- type(dict):
            
                'logical_port_number' : int[2 byte] -- Logical Port Number
                'port_nubmer_valid':  int[1 bit] -- Logical Port number is valid
                'selected_port_option':  int[4 bit] -- Selected Port option index
        '''
        byte_16 = config.get("logical_port_number", 0) & 0xff
        byte_17 = config.get("port_nubmer_valid", 0) & 0x1
        byte_18 = config["selected_port_option"] & 0xf

        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x06EB
        aq_desc.flags = 0
        aq_desc.param0 = (byte_18 << 16 | byte_17 << 8 | byte_16)
        buffer = []
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print("Failed to send Read Write SffEeprom Command, status: {}, FW ret value: {}".format(status,aq_desc.retval))
        return [status, aq_desc.retval]

    def testReadWriteSffEeprom(self):
        config = dict()
        config["logical_port_number"] = self.driver.port_number()
        config["i2c_memory_offset"] = 0
        self.ReadWriteSffEeprom(config,True)
        
    def ReadWriteSffEeprom(self, config, debug=False):
        '''
        input:
             config -- type(dict):
            
                'logical_port_number' : int[2 byte] -- Logical Port Number
                'port_nubmer_valid':  int[1 bit] -- Logical Port number is valid
                'i2c_bus_address': int[10 bits] -- Slave address (10 bits)
                '10_bit_assress_select' :int[1 bit] -- 0- 7 bit address used, 1- 10 bit address used
                'set_eeprom_page' : int[2 bit] -- 00- Do not change page , 
                                                  01: Read offset 127 of EEPROM, set it to Byte 23 on mismatch
                                                  10: Read offset 126 of EEPROM, set it to Byte 22 on mismatch
                                                  11: Reserved
                'command': int[1 bit] -- 0-Read, 1-Write
                'i2c_memory_offset': int[2 byte] -- Offset within the RRPROM to start reading from, up to 16 bits 
                'eeprom_page' :int [2 byte]-- sirst byte : Set offset 126 to this value,  second byte : Set offset 127 to this value
        '''
        byte_16 = config.get("logical_port_number", 0) & 0xff
        byte_17 = config.get("port_nubmer_valid", 0) & 0x1
        byte_18 = config.get("i2c_bus_address",0) & 0xff
        byte_19 = ((config.get("command", 0) & 0x1) << 7)|((config.get("set_eeprom_page", 0) & 0x3) << 3)|((config.get("10_bit_assress_select", 0) & 0x1) << 2)|(config.get("i2c_bus_address", 0) >> 8) & 0x3
        byte_20 = config["i2c_memory_offset"] & 0xff
        byte_21 = 0
        byte_22 = config.get("eeprom_page", 0) & 0xff
        byte_23 = (config.get("eeprom_page", 0) >> 8) & 0xff


        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x06EE
        aq_desc.flags = 0x1000 
        aq_desc.param0 = (byte_19 << 24 | byte_18 << 16 | byte_17 << 8 | byte_16)
        aq_desc.param1 = (byte_23 << 24 | byte_22 << 16 | byte_21 << 8 | byte_20)
        aq_desc.addr_high = 0 
        aq_desc.addr_low = 0
        buffer = [0]*16
        aq_desc.datalen = len(buffer)
        status = self.driver.send_aq_command(aq_desc, buffer, debug, False)
        if status != 0 or aq_desc.retval != 0:
            print("Failed to send Read Write SffEeprom Command, status: {}, FW ret value: {}".format(status,aq_desc.retval))
        return [status, aq_desc.retval]


    def ReadMdio(self, config, debug=False):
        # '''
        #    input:
        #    config -- type(dict):
        #    
        #        'logical_prt_num' : int[2 byte] -- Logical Port Number
        #        'node_type_context': int[1 byte]-- the context within which the handle should be identified
        #        'index':int[1 byte]-- requested node index
        #        'node_handle' :int[2 byte]--  Reference node handle / Node handle
        #        'mdio_device_address': int[5 bit] --  MDIO device address
        #        'clause_22_mdio_formating':  int[1 bit] -- use Clause 22 MDIO formating
        #        'clause_45_mdio_formating': int[1 bit] --   use Clause 45 MDIO formating
        #        'mmd_offset_address':int[2 byte] --  MMD offset address (MDIO offset)

        #    return:
        #        list --
        #            list[0] - status : this the drivers return vlaue 0 = succefull admin command
        #            list[1] -data : 16 bytes of  data read from the MDIO device
        #'''
        byte_16 = config["logical_port_number"] & 0xff
        byte_17 = config.get("port_nubmer_valid", 1) & 0x1
        byte_18 = ((config.get("node_type_context", 0x2) & 0xff) << 4) | (config.get('node_type', 0x6) & 0xf)
        byte_19 = config.get("index",0) & 0xff
        byte_20 = config["node_handle"] & 0xff
        byte_21 = (config["node_handle"] >> 8) & 0x3
        byte_22 = ((config["clause_45_mdio_formating"] & 0x1) <<6) |((config["clause_22_mdio_formating"] & 0x1) <<5) | (config["mdio_device_address"]& 0x1f)
        byte_24 = config["mmd_offset_address"] & 0xff
        byte_25 = (config["mmd_offset_address"] >> 8) & 0xff


        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x06E4
        aq_desc.flags = 0
        aq_desc.param0 = (byte_19 << 24 | byte_18 << 16 | byte_17 << 8 | byte_16)
        aq_desc.param1 = (byte_22 << 16 | byte_21 << 8 | byte_20)
        aq_desc.addr_high = (byte_25 << 8 | byte_24) 
        aq_desc.addr_low = 0
        buffer = []
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print("Failed to send Read MDIO Command, status: {}, FW ret value: {}".format(status,aq_desc.retval))
        else:
            data = dict()     
            data['mdio_data'] = (aq_desc.addr_high >> 16) & 0xff
            status = (False, data)
        return status

    def WriteMdio(self, config, debug=False):
        '''
            input:
            config -- type(dict):
            
                'logical_prt_num' : int[2 byte] -- Logical Port Number
                'node_type_context': int[1 byte]-- the context within which the handle should be identified
                'index':int[1 byte]-- requested node index
                'node_handle' :int[2 byte]--  Reference node handle / Node handle
                'mdio_device_address': int[5 bit] --  MDIO device address
                'clause_22_mdio_formating':  int[1 bit] -- use Clause 22 MDIO formating
                'clause_45_mdio_formating': int[1 bit] --   use Clause 45 MDIO formating
                'mmd_offset_address':int[2 byte] --  MMD offset address (MDIO offset)
                'mdio_data':int[2 byte] -- 16 bits data that needs to be written to the MDIO device.

            return:
                list --
                    list[0] - status : this the drivers return vlaue 0 = succefull admin command
                    list[1] -
        '''
        byte_16 = config["logical_port_number"] & 0xff
        byte_17 = config.get("port_nubmer_valid", 1) & 0x1
        byte_18 = ((config.get("node_type_context", 0x2) & 0xff) << 4) | (config.get('node_type', 0x6) & 0xf)
        byte_19 = config.get("index",0) & 0xff
        byte_20 = config["node_handle"] & 0xff
        byte_21 = (config["node_handle"] >> 8) & 0x3
        byte_22 = ((config["clause_45_mdio_formating"] & 0x1) <<6) |((config["clause_22_mdio_formating"] & 0x1) <<5) | (config["mdio_device_address"]& 0x1f)
        byte_24 = config["mmd_offset_address"] & 0xff
        byte_25 = (config["mmd_offset_address"] >> 8) & 0xff
        byte_26 = config["mdio_data"] & 0xff
        byte_27 = (config["mdio_data"] >> 8) & 0xff

        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x06E5
        aq_desc.flags = 0
        aq_desc.param0 = (byte_19 << 24 | byte_18 << 16 | byte_17 << 8 | byte_16)
        aq_desc.param1 = (byte_22 << 16 | byte_21 << 8 | byte_20)
        aq_desc.addr_high = (byte_27 << 24 |byte_26 << 16 | byte_25 << 8 | byte_24) 
        aq_desc.addr_low = 0
        buffer = []
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print("Failed to send Write MDIO Command, status: {}, FW ret value: {}".format(status,aq_desc.retval))
        return [status, aq_desc.retval]

    def SetGpioByFunction(self, config, debug=False):
       #  '''
       #  Set a GPIO signal which is part of the topology structures. 
       #     input:
       #     config -- type(dict):
       #     
       #         'logical_prt_num' : int[2 byte] -- Logical Port Number
       #         'node_type_context': int[1 byte]-- the context within which the handle should be identified
       #         'index':int[1 byte]-- requested node index
       #         'node_handle' :int[2 byte]--  Reference node handle / Node handle
       #         'io_function': int[1 byte] -- IO Function of the GPIO that needs to be set (The 5 LSB are used)
       #         'io_value':  int[1 byte] --  IO value to set in the LSB 
       #         

       #     return:
       #         list --
       #             list[0] - status : this the drivers return vlaue 0 = succefull admin command
       #             list[1] -
       # '''
        byte_16 = config["logical_port_number"] & 0xff
        byte_17 = config.get("port_nubmer_valid", 1) & 0x1
        byte_18 = ((config.get("node_type_context", 0x2) & 0xff) << 4) | (config.get('node_type', 0x6) & 0xf)
        byte_19 = config.get("index",0) & 0xff
        byte_20 = config["node_handle"] & 0xff
        byte_21 = (config["node_handle"] >> 8) & 0x3
        byte_22 = config["io_function"] & 0xff
        byte_23 = config["io_value"] & 0xff

        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x06E6
        aq_desc.flags = 0
        aq_desc.param0 = (byte_19 << 24 | byte_18 << 16 | byte_17 << 8 | byte_16)
        aq_desc.param1 = (byte_23 << 24 | byte_22 << 16 | byte_21 << 8 | byte_20)
        buffer = []
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print("Failed to send Set GPIO By Function Command, status: {}, FW ret value: {}".format(status,aq_desc.retval))
        return [status, aq_desc.retval]

    def GetGpioByFunction(self, config, debug=False):
       #  '''
       #   get the value of a GPIO signal which is part of the topology structures

       #     input:
       #     config -- type(dict):
       #     
       #         'logical_prt_num' : int[2 byte] -- Logical Port Number
       #         'node_type_context': int[1 byte]-- the context within which the handle should be identified
       #         'index':int[1 byte]-- requested node index
       #         'node_handle' :int[2 byte]--  Reference node handle / Node handle
       #         'io_function': int[1 byte] -- IO Function of the GPIO that needs to be set (The 5 LSB are used)
       #         
       #     return:
       #         list --
       #             list[0] - status : this the drivers return vlaue 0 = succefull admin command
       #             list[1] -  'io_value':  int[1 byte] that was read in the LSB
       # '''
        byte_16 = config["logical_port_number"] & 0xff
        byte_17 = config.get("port_nubmer_valid", 1) & 0x1
        byte_18 = ((config.get("node_type_context", 0x2) & 0xff) << 4) | (config.get('node_type', 0x6) & 0xf)
        byte_19 = config.get("index",0) & 0xff
        byte_20 = config["node_handle"] & 0xff
        byte_21 = (config["node_handle"] >> 8) & 0x3
        byte_22 = config["io_function"] & 0xff


        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x06E7
        aq_desc.flags = 0
        aq_desc.param0 = (byte_19 << 24 | byte_18 << 16 | byte_17 << 8 | byte_16)
        aq_desc.param1 = (byte_22 << 16 | byte_21 << 8 | byte_20)
        buffer = []
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print("Failed to send Get GPIO By Function Command, status: {}, FW ret value: {}".format(status,aq_desc.retval))
        else:
            data = dict()     
            data['io_value'] = (aq_desc.param1 >> 24) & 0xff
            status = (False, data)
        return status

    def SetGpio(self, config, debug=False):
       #  '''
       #  Set a GPIO signal which is part of the topology structures. 
       #     input:
       #     config -- type(dict):
       #     
       #         'gpio_controller_node_handle' : int[10 bits] --  GPIO controller node handle
       #         'io_number': int[1 byte] -- IO number of the GPIO that needs to be set (The 5 LSB are used)
       #         'io_value':  int[1 byte] --  IO value to set in the LSB 
       #         
       #     return:
       #         list --
       #             list[0] - status : this the drivers return vlaue 0 = succefull admin command
       #             list[1] -
       # '''
        byte_16 = config["gpio_controller_node_handle"] & 0xff
        byte_17 = (config["gpio_controller_node_handle"] >>8 ) & 0x3
        byte_18 = config["io_number"] & 0xff
        byte_19 = config["io_value"] & 0xff

        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x06EC
        aq_desc.flags = 0
        aq_desc.param0 = (byte_19 << 24 | byte_18 << 16 | byte_17 << 8 | byte_16)
        buffer = []
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print("Failed to send Set GPIO Command, status: {}, FW ret value: {}".format(status,aq_desc.retval))
        return [status, aq_desc.retval]

    def GetGpio(self, config, debug=False):
       #  '''
       #  Get a GPIO signal which is part of the topology structures. 
       #     input:
       #     config -- type(dict):
       #     
       #         'gpio_controller_node_handle' : int[10 bits] --  GPIO controller node handle
       #         'io_number': int[1 byte] -- IO number of the GPIO that needs to be set (The 5 LSB are used)
       #        
       #         
       #     return:
       #         list --
       #             list[0] - status : this the drivers return vlaue 0 = succefull admin command
       #             list[1] - 'io_value':  int[1 byte] --  IO value to set in the LSB 
       # '''
        byte_16 = config["gpio_controller_node_handle"] & 0xff
        byte_17 = (config["gpio_controller_node_handle"] >>8 ) & 0x3
        byte_18 = config["io_number"] & 0xff

        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x06ED
        aq_desc.flags = 0
        aq_desc.param0 = (byte_18 << 16 | byte_17 << 8 | byte_16)

        buffer = []
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print("Failed to send Get GPIO Command, status: {}, FW ret value: {}".format(status,aq_desc.retval))
        else:
            data = dict()     
            data['io_value'] = (aq_desc.param0 >> 24) & 0xff
            status = (False, data)
        return status

    def SetLed(self, config, debug=False):
       #  '''
       #  set a LED signal which is part of the topology structures
       #     input:
       #     config -- type(dict):
       #     
       #         'logical_port_number' : int[1 byte] -- logical port number 
       #         'port_nubmer_valid': int[1 bit] -- logical port number is valid
       #         'node_type_context': int[1 byte]-- the context within which the handle should be identified
       #         'index':int[1 byte]-- requested node index
       #         'node_handle' :int[2 byte]--  Reference node handle / Node handle
       #         'color': int[3 bit] --  color of the LED 
       #          'blink_option': int[3 bit] --  Blink option
       #         
       #     return:
       #         list --
       #             list[0] - status : this the drivers return vlaue 0 = succefull admin command
       #             list[1] -  'io_value':  int[1 byte] that was read in the LSB
       # '''
        byte_16 = config["logical_port_number"] & 0xff
        byte_17 = config.get("port_nubmer_valid", 1) & 0x1
        byte_18 = ((config.get("node_type_context", 0x2) & 0xff) << 4) | (config.get('node_type', 0x6) & 0xf)
        byte_19 = config.get("index",0) & 0xff
        byte_20 = config["node_handle"] & 0xff
        byte_21 = (config["node_handle"] >> 8) & 0x3
        byte_22 = ((config["blink_option"] & 0x7) << 3 )| (config["color"] & 0x7)


        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x06E8
        aq_desc.flags = 0
        aq_desc.param0 = (byte_19 << 24 | byte_18 << 16 | byte_17 << 8 | byte_16)
        aq_desc.param1 = (byte_22 << 16 | byte_21 << 8 | byte_20)
        buffer = []
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print("Failed to send Set LED Command, status: {}, FW ret value: {}".format(status,aq_desc.retval))
        return [status, aq_desc.retval]


    def SetPortIdetificationLed(self, config, debug=False):
       #  '''
       # set the LED that is used to identify the port as indicated in the topology structures
       #     input:
       #     config -- type(dict):
       #     
       #         'logical_port_number' : int[1 byte] -- logical port number 
       #         'port_nubmer_valid': int[1 bit] -- logical port number is valid
       #         'set_ident_mode': int[1 bit]-- 0 - The LED is configured to its original mode, 
       #                                        1 - The LED is configured to identification mode and will blink
       #         
       #     return:
       #         list --
       #             list[0] - status : this the drivers return vlaue 0 = succefull admin command
       #             list[1] -  'io_value':  int[1 byte] that was read in the LSB
       # '''
        byte_16 = config["logical_port_number"] & 0xff
        byte_17 = config.get("port_nubmer_valid", 1) & 0x1
        byte_18 = config.get("set_ident_mode", 1) & 0x1

        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x06E9
        aq_desc.flags = 0
        aq_desc.param0 = (byte_18 << 16 | byte_17 << 8 | byte_16)
        buffer = []
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print("Failed to send Set Port Identification LED Command, status: {}, FW ret value: {}".format(status,aq_desc.retval))
        return [status, aq_desc.retval]

###############################################################################
#                     Generic FW admin commands                               # 
###############################################################################

    def GetVersion(self, config, debug):
        '''
        
        input:
             config -- type(dict):
             'rom_build_id' : int[4 bytes] -- device ROM Build version
             'fw_build_id' : int[4 bytes] --  Device FW build version
             'fw_branch' : int[1 byte] --  FW Branch Identifier
             'fw_major_version': int[1 bytes] -- FW major version
             'fw_minor_version': int[1 bytes] --FW minor version 
             'fw_patch_version': int[1 bytes] --FW patch version
             'aq_api_branch': int[1 bytes] --AQ API Branch Identifier
             'aq_api_major_version': int[1 bytes] --AQ API major version
             'aq_api_minor_version': int[1 bytes] --AQ API minor version
             'aq_api_patch_version': int[1 bytes] --AQ API patch version
                     
        '''
        byte_16 = config['rom_build_id'] & 0xff
        byte_17 =(config['rom_build_id'] >> 8) & 0xff
        byte_18 = (config['rom_build_id'] >> 16) & 0xff
        byte_19 = (config['rom_build_id'] >> 24) & 0xff
        byte_20 = config['fw_build_id'] & 0xff
        byte_21 = (config['fw_build_id'] >> 8) & 0xff
        byte_22 = (config['fw_build_id'] >> 16) & 0xff
        byte_23 = (config['fw_build_id'] >> 24) & 0xff
        byte_24 = config['fw_branch'] & 0xff
        byte_25 = config['fw_major_version'] & 0xff
        byte_26 = config['fw_minor_version'] & 0xff
        byte_27 = config['fw_patch_version'] & 0xff
        byte_28 = config['aq_api_branch'] & 0xff
        byte_29 = config['aq_api_major_version'] & 0xff
        byte_30 = config['aq_api_minor_version'] & 0xff
        byte_31 = config['aq_api_patch_version'] & 0xff
        
        buffer = list() 
        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x0001 
        aq_desc.flags = 0x0 
        aq_desc.param0 =  (byte_19 << 24 | byte_18 << 16 | byte_17 << 8| byte_16)  # config['rom_build_id']
        aq_desc.param1 = (byte_23 << 24 | byte_22 << 16 | byte_21 << 8| byte_20) # config['fw_build_id']
        aq_desc.addr_high = (byte_27 << 24 | byte_26 << 16 | byte_25 << 8| byte_24)
        aq_desc.addr_low = (byte_31 << 24 | byte_30 << 16 | byte_29 << 8| byte_28)
        aq_desc.datalen = len(buffer)
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Get Version Command, status: {} , FW ret value: {}'.format(status, aq_desc.retval))
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)
        return status

    def DriverVersion(self, config, debug):
        '''
        
        input:
             config -- type(dict):
             'major_version' : int[1 bytes] --  major version, 
             'minor_version' : int[1 bytes] -- minor version,
             'build_version' : int[1 bytes] -- build version, 
             'sub_build_version' : int[1 bytes] -- sub-build version
                     
        '''
        byte_16 = config['major_version'] & 0xff
        byte_17 = config['minor_version']  & 0xff
        byte_18 = config['build_version'] & 0xff
        byte_19 = config['sub_build_version']  & 0xff
        
        buffer = [0]*0x1000 
        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x0002 
        aq_desc.flags = 0x0 
        aq_desc.param0 =  (byte_19 << 24 | byte_18 << 16 | byte_17 << 8| byte_16)  
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.datalen = len(buffer)
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Driver Version Command, status: {} , FW ret value: {}'.format(status, aq_desc.retval))
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            data = dict()
            data["driver_version"] = buffer
            status = (False, data)
        return status

    def QueueShutdown(self, config, debug):
        '''
        
        input:
             config -- type(dict):
             'driver_unloading' : int[1 bit] -- 1 if the driver intends to unload
                     
        '''
        byte_16 = config['driver_unloading'] & 0x1
 
        
        buffer = []
        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x0003
        aq_desc.flags = 0x0 
        aq_desc.param0 =   byte_16 & 0xffffffff
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.datalen = len(buffer)
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Queue Shutdown Command, status: {} , FW ret value: {}'.format(status, aq_desc.retval))
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)
        return status


    def setPfContext(self, config, debug):
        '''
            input:
                config -- type(dict):
                'pf_id' : int[1 byte] -- Physical function ID
                     
        '''
        byte_16 = config['pf_id'] & 0xff
 
        
        buffer = []
        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x0004
        aq_desc.flags = 0x0 
        aq_desc.param0 =   byte_16 & 0xffffffff
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.datalen = len(buffer)
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send set Pf Context Command, status: {} , FW ret value: {}'.format(status, aq_desc.retval))
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)
        return status

    def GetExpandedAqErrorReason(self, config, debug):
        '''
            input:
                config -- type(dict):
                
                     
        '''

        buffer = []
        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x0005
        aq_desc.flags = 0x0 
        aq_desc.param0 = 0
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.datalen = len(buffer)
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Get Expanded Aq Error Reason Command, status: {} , FW ret value: {}'.format(status, aq_desc.retval))
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            data = dict()
            data["error_reason"] = aq_desc.param0
            data["error_identifier"] = aq_desc.param1
            status = (False, None)
        return status

    def RequestResourceOwnership(self, config, debug=False):
        '''
        input:
             config -- type(dict):
             'resource_id' : int[2 bytes] -- see table 9-50
             'access_type' : int[2 bytes] -- see table 9-50
             'timeout' : int[4 bytes] -- Timeout in ms used by SW to override the default timeout for the operation 
             'resource_number' : int[4 bytes] -- For an SDP, this is the pin ID of the SDP
        return :
            'timeout' : int[4 bytes] --indicates the timeout used for the specific resource
        '''
        byte_16 = config['resource_id'] & 0xff
        byte_17 =(config['resource_id'] >> 8) & 0xff
        byte_18 = config['access_type'] & 0xff
        byte_19 = (config['access_type'] >> 8) & 0xff
        byte_20 = config.get('timeout', 0) & 0xff
        byte_21 = (config.get('timeout', 0) >> 8) & 0xff
        byte_22 = (config.get('timeout', 0) >> 16) & 0xff
        byte_23 = (config.get('timeout', 0) >> 24) & 0xff
        byte_24 = config.get('resource_number', 0) & 0xff
        byte_25 = (config.get('resource_number', 0) >> 8) & 0xff
        byte_26 = (config.get('resource_number', 0) >> 16) & 0xff
        byte_27 = (config.get('resource_number', 0) >> 24) & 0xff

        buffer = list()
        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x0008
        aq_desc.flags = 0x2000 
        aq_desc.param0 =  (byte_19 << 24 | byte_18 << 16 | byte_17 << 8| byte_16)  
        aq_desc.param1 = (byte_23 << 24 | byte_22 << 16 | byte_21 << 8| byte_20)  #config['timeout']
        aq_desc.addr_high = (byte_27 << 24 | byte_26 << 16 | byte_25 << 8| byte_24)  #config['resource_number']
        aq_desc.addr_low = 0
        aq_desc.datalen = len(buffer)
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Request Resource Ownership Command, status: {} , FW ret value: {}'.format(status, aq_desc.retval))
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            data = dict()
            data["timeout"] = aq_desc.param1
            data["status"] = aq_desc.addr_low & 0xffff
            status = (False, data)
        return status

    def ReleaseResourceOwnership(self, config, debug=False):
        '''
        input:
             config -- type(dict):
             'resource_id' : int[2 bytes] -- see table 9-50
             'access_type' : int[2 bytes] -- see table 9-50
             'timeout' : int[4 bytes] -- Timeout in ms 
             'resource_number' : int[4 bytes] -- For an SDP, this is the pin ID of the SDP
        '''
        byte_16 = config['resource_id'] & 0xff
        byte_17 =(config['resource_id'] >> 8) & 0xff
        byte_18 = 0
        byte_19 = 0
        
        byte_24 = config.get('resource_number', 0) & 0xff
        byte_25 = (config.get('resource_number', 0) >> 8) & 0xff
        byte_26 = (config.get('resource_number', 0) >> 16) & 0xff
        byte_27 = (config.get('resource_number', 0) >> 24) & 0xff

        
        buffer = list()
        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x0009
        aq_desc.flags = 0x2000 
        aq_desc.param0 =  (byte_19 << 24 | byte_18 << 16 | byte_17 << 8| byte_16)  
        aq_desc.param1 = 0
        aq_desc.addr_high = (byte_27 << 24 | byte_26 << 16 | byte_25 << 8| byte_24)  #config['resource_number']
        aq_desc.addr_low = 0
        aq_desc.datalen = len(buffer)
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Release Resource Ownership Command, status: {} , FW ret value: {}'.format(status, aq_desc.retval))
            status = (True, aq_desc.retval)
        else:
            status = (False, None)
        return status

    def DiscoverFunctionCapabilities(self, config, debug=False):
        '''
            This command is used to request the list capabilities of the function. 
            If the buffer size is not big enough for the whole structure FW will return ENOMEM
            
        '''
        buffer = [0]*0x1000
        aq_desc = AqDescriptor()
        aq_desc.opcode = 0xa 
        aq_desc.flags = 0x1600 
        aq_desc.param0 = 0         
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.datalen = len(buffer)
        status = self.driver.send_aq_command(aq_desc, buffer, debug, True)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Set PHY Config Admin Command, status: {} , FW ret value: {}'.format(status, aq_desc.retval))
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)

        data = dict()
        data['number_of_records'] = aq_desc.param1
        data['resource_recognized'] = buffer

        return (status, data)

    def DiscoverDeviceCapabilities(self, config=None, debug=False):
        '''
            This command is used to request the list capabilities of the device. 
            If the buffer size is not big enough for the whole structure FW will return ENOMEM
        '''
        buffer = [0]*0x1000
        aq_desc = AqDescriptor()
        aq_desc.opcode = 0xb 
        aq_desc.flags = 0x1600 
        aq_desc.param0 = 0         
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.datalen = len(buffer)
        status = self.driver.send_aq_command(aq_desc, buffer, debug, True)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send dicsocer device capabilities Admin Command, status: {} , FW ret value: {}'.format(status, aq_desc.retval))
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            data = dict()
            data['number_of_records'] = aq_desc.param1
            data['resource_recognized'] = buffer
        return (status, data)

    def Vm_VfReset(self, config, debug):
        '''
        input:
             config -- type(dict):
             'reset_operation' : int[2 bits] -- 01= VM Reset operation, 10= VF Reset operation, 11=PF Reset
             'command_type' : int[1 bit] -- 0: This is and initial call / 1: This is a Subsequent call
             'on_time_out' : int[1 bit] -- 0: Return EAGAIN on Time out / 1: Flush Pipe on Time out
             'num_of_queue_grops' : int[1 bytes] -- Number of Disabled Queue Groups(1..127)
             'vmvf_num':int[10 bit] --  VM or VF numbers
             'time_out_time' :int[6 bit] --Command Time out in units of 100 micro seconds (Valid values 0-50)

         return:

             'num_of_fully_processed_grops' : int[1 bytes] -- Number of fully processed groups                                    
             'blocked_cgds' : int[1 bytes] -- A Bitmap of blocked CGDs. Set by EMP FW when returns with EAGAIN     
        '''
        byte_16 = ((config['on_time_out'] & 0x1 ) << 3) |((config['command_type'] & 0x1 ) << 2) |(config['reset_operation'] & 0x3)  
        byte_17 = config['num_of_queue_grops'] & 0xff
        byte_18 = config['vmvf_num'] & 0xff
        byte_19= ((config['time_out_time'] & 0x3f ) << 2) |(config['vmvf_num'] >> 8) & 0x3

        buffer = [0]*0x1000
        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x0C31
        aq_desc.flags = 0x0 
        aq_desc.param0 =  (byte_19 << 24 | byte_18 << 16 | byte_17 << 8| byte_16)  
        aq_desc.param1 = 0
        aq_desc.addr_high =0
        aq_desc.addr_low = 0
        aq_desc.datalen = len(buffer)
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Request Resource Ownership Command, status: {} , FW ret value: {}'.format(status, aq_desc.retval))
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            data = dict()
            #TODO -reset command buffer table:9-57
            data["num_of_fully_processed_grops"] = (aq_desc.param0 >> 8) & 0xff
            data["blocked_cgds"] = aq_desc.param1  & 0xff
            status = (False, data)
        return status

################################################################################
#                      NVM admin commands                                      #
################################################################################
    
    def NvmRead(self, config, debug=False):
        '''
            input:
                 config -- type(dict):
                 'offset' : int[3 bytes] -- Offset in the module
                 'read_from_flash' : int[1 bit] --  1: read is done directly from the flash and not from shadow RAM
                 'last_command_bit' : int[1 bit] --  this is the last admin command of a sequence. (Ignored by EMP)
                 'module_typeID': int[2 bytes] -- Module typeID
                 'length': int[2 bytes] --Length of the section to be read
        '''
        byte_16 = config.get('offset', 0) & 0xff
        byte_17 =(config.get('offset', 0) >> 8) & 0xff
        byte_18 = (config.get('offset', 0) >> 8) & 0xff
        byte_19 = ((config.get("read_from_flash", 0) & 0x1) << 7) | (config.get("last_command_bit", 0) & 0x1)
        byte_20 = config.get('module_typeID', 0) & 0xff
        byte_21 = (config.get('module_typeID', 0)  >> 8) & 0xff
        byte_22 = config['length'] & 0xff
        byte_23 = (config['length'] >> 8) & 0xff
        
        buffer = [0]*0x1000
        
        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x701
        aq_desc.flags = 0x3200
        aq_desc.param0 =  (byte_19 << 24 | byte_18 << 16 | byte_17 << 8| byte_16)
        aq_desc.param1 = (byte_23 << 24 | byte_22 << 16 | byte_21 << 8| byte_20)
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.datalen = len(buffer)
        status = self.driver.send_aq_command(aq_desc, buffer, debug, False)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Nvm Read Admin Command, status: {} , FW ret value: {}'.format(status, aq_desc.retval))
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            data = dict()
            data['datalen'] = aq_desc.datalen
            data['offset'] = aq_desc.param0 & 0xffffff
            data['module_typeID'] = aq_desc.param1 & 0xffff
            data['length'] = (aq_desc.param1 >> 16) & 0xffff
            data['nvm_module'] = buffer[0:data['length']]
            status = (False, data)
        return status

    def NvmErase(self, config, debug=False):
        '''
            Erase consecutive 4 KB sectors of the Flash
            input:
                 config -- type(dict):
                 'offset' : int[3 bytes] -- Offset in the module
                 'read_from_flash' : int[1 bit] --  1: read is done directly from the flash and not from shadow RAM
                 'last_command_bit' : int[1 bit] --  this is the last admin command of a sequence. (Ignored by EMP)
                 'module_typeID': int[2 bytes] -- Module typeID
                 'length': int[2 bytes] --Length of the section to be read
        '''
        byte_16 = 0
        byte_17 = 0
        byte_18 = 0
        byte_22 = 0
        byte_23 = 0
        byte_16 = config.get('offset', 0) & 0xff
        byte_17 = (config.get('offset', 0) >> 8) & 0xff
        byte_18 = (config.get('offset', 0) >> 16) & 0xff
        byte_22 = config.get('length',0) & 0xff
        byte_23 = (config.get('length',0) >> 8) & 0xff
        
        byte_19 = config.get("last_command_bit", 0) & 0x1
        byte_20 = config['module_typeID'] & 0xff
        byte_21 = (config['module_typeID'] >> 8) & 0xff

        buffer = []
        
        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x702 
        aq_desc.flags = 0x0 
        aq_desc.param0 =  (byte_19 << 24 | byte_18 << 16 | byte_17 << 8| byte_16)
        aq_desc.param1 = (byte_23 << 24 | byte_22 << 16 | byte_21 << 8| byte_20)
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.datalen = len(buffer)
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Nvm Erase Admin Command, status: {} , FW ret value: {}'.format(status, aq_desc.retval))
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)
        return status

    def NvmWrite(self, config, debug=False):
        '''
            write the data given by the attached buffer into a specified location in the NVM

            input:
                 config -- type(dict):
                 'offset' : int[3 bytes] -- Offset in the module
                 'flash_only' : int[1 bit] --  
                 'last_command_bit' : int[1 bit] --  this is the last admin command of a sequence. (Ignored by EMP)
                 'module_typeID': int[2 bytes] -- Module typeID
                 'length': int[2 bytes] --Length of the section to be read

            return:
                 'reset_flag' : int[1 bit] -- the type of reset required to get the NVM bank update effective (NVM Bank update only)
                                                0= POR, 1=PERST
        '''
        byte_16 = config.get('offset', 0) & 0xff
        byte_17 = (config.get('offset', 0) >> 8) & 0xff
        byte_18 = (config.get('offset', 0) >> 16) & 0xff
        byte_19 = ((config.get("flash_only", 0) & 0x1) << 7) | config.get("last_command_bit", 0) & 0x1
        byte_20 = config.get('module_typeID', 0) & 0xff
        byte_21 = (config.get('module_typeID', 0) >> 8) & 0xff
        byte_22 = config['length'] & 0xff
        byte_23 = (config['length'] >> 8) & 0xff

        data_to_write = config['data']
        buffer = [0]*0x100
        buffer[0:len(data_to_write)] = data_to_write
        
        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x703
        aq_desc.flags = 0x3000 
        aq_desc.param0 =  (byte_19 << 24 | byte_18 << 16 | byte_17 << 8| byte_16)
        aq_desc.param1 = (byte_23 << 24 | byte_22 << 16 | byte_21 << 8| byte_20)
        aq_desc.addr_high = 0
        aq_desc.addr_low = 2
        aq_desc.datalen = len(buffer)
        status = self.driver.send_aq_command(aq_desc, buffer, debug, True)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Nvm Write Admin Command, status: {} , FW ret value: {}'.format(status, aq_desc.retval))
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            data = dict()
            data["reset_flag"] = (aq_desc.param0 >> 24) & 0xff
            status = (False, data)
        return status

    def debug_NVMConfigRead(self):
        config = dict()

        config['feature_or_field'] = 1
        config['single_or_multiple_elements'] = 1
        config['field_id'] = 0x2

        self.NvmConfigRead(config, True)

    def NvmConfigRead(self, config, debug=False):
        '''
        input:
             config -- type(dict):
             'feature_or_field' : int[1 bit] -- 0: Feature selections 
                                                1: Immediate fields  are written
             'single_or_multiple_elements' : int[1 bit] -- 0: single Feature_ID/ Field_ID is read, 
                                                           1: Feature_ID/Field_ID iteration is used
             'element_count': :int[2 bytes] -- The number of features/fields returned
             'field_id': int[2 bytes] -- field_id
             'feature_id': int[2 bytes] --Feature_ID
             'field_value':int[2 bytes] --field_value
             'requested_feature_selection':int[2 bytes] --Requested feature selection           
        '''
        buffer = [0]*0x1000          

        byte_16 = ((config.get('feature_or_field', 0) & 0x1 )<< 1) | (config['single_or_multiple_elements'] & 0x1)
        if config['feature_or_field']:
            byte_20 = config['field_id'] & 0xff
            byte_21 = (config['field_id'] >> 8) & 0xff
        else:
            byte_20 = config['feature_id'] & 0xff
            byte_21 = (config['feature_id'] >> 8) & 0xff

        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x704 
        aq_desc.flags = 0x1400
        aq_desc.param0 =  byte_16
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.datalen = len(buffer)
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Nvm Config Read Admin Command, status: {} , FW ret value: {}'.format(status, aq_desc.retval))
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            aq_desc.param0
            status = (False, data)
        return status

    def NvmConfigWrite(self, config, debug=False):
        '''
            writes the feature selections and the values of the immediate fields provided in the attached command buffer to the NVM.
            input:
                 config -- type(dict):
                 'feature_or_field' : int[1 bit] -- 0: Feature selections /1: Immediate fields  are written
                 'added_new_config' : int[1 bit] -- 0: Existing config / 1:New config added
                 'field_list': list of ImmediateBufferForNvm (found core.structs)
                 or 
                 'feature_list': list of FeatureBufferForNvm (found core.structs)
                 
                 if feature_or_field == 1 -> immediate buffer
                 else -> feature buffer
        '''

        buffer = list()
        if config['feature_or_field']:
            #expecting immediate field
            immediate_field_list = config['field_list']
            for field in immediate_field_list:
                buffer.append(field.field_id & 0xff)
                buffer.append((field.field_id >> 8) & 0xff)
                buffer.append(field.field_flags & 0xff)
                buffer.append((field.field_flags >> 8) & 0xff)
                buffer.append(field.field_value & 0xff)
                buffer.append((field.field_value >> 8) & 0xff)           
            byte_18 = len(immediate_field_list) & 0xff
            byte_19 = (len(immediate_field_list) >> 8) & 0xff
        else:
            #expecting Feature 
            features_list = config['feature_list']
            for feature in features_list:
                buffer.append(feature.feature_id & 0xff)
                buffer.append((feature.feature_id >> 8) & 0xff)
                buffer.append(feature.feature_flags & 0xff)
                buffer.append((feature.feature_flags >> 8) & 0xff)
                buffer.append(feature.feature_selection & 0xff)
                buffer.append((feature.feature_selection >> 8) & 0xff)           
            byte_18 = len(features_list) & 0xff
            byte_19 = (len(features_list) >> 8) & 0xff

        byte_16 = ((config["added_new_config"] & 0x1) << 2) | ((config['feature_or_field'] & 0x1 )<< 1) | 0
        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x705 
        aq_desc.flags = 0x0 
        aq_desc.param0 =  (byte_19 << 24 | byte_18 << 16 | byte_16)
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.datalen = len(buffer)
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Nvm Config Write Admin Command, status: {} , FW ret value: {}'.format(status, aq_desc.retval))
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)
        return status

    def NvmUpdateChecksum(self, config, debug=False):
        '''
            recalculates/verifies the PFA checksum
            input:
                 config -- type(dict):
                 'verify_checksum' : int[1 bit] -- Verify Checksum
                 'recalculate_checksum' : int[1 bit] -- Recalculate Checksum 
                
            returnd:
                 'checksum': int[2 bytes] --  Returned only if Verify Checksum flag was set in command
        '''
        byte_16 = ((config.get("recalculate_checksum", 0) & 0x1) << 1) | (config.get('verify_checksum', 1) & 0x1 )
        buffer = list()
        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x706
        aq_desc.flags = 0x0 
        aq_desc.param0 =  byte_16
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.datalen = len(buffer)
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Nvm Update Checksum Admin Command, status: {} , FW ret value: {}'.format(status, aq_desc.retval))
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            data = dict() 
            if (byte_16 & 0x1):
                data["checksum"]= (aq_desc.param0 >> 16) & 0xffff

            status = (False, data)
        return status

    def NvmWriteActivate(self, config, debug=False):
        '''
        must be called after NVM Write AQ Command was successfully must be called after NVM Write AQ Command was successfully 
        input:
             config -- type(dict):
             'preserrvation_mode' : int[2 bit] -- 00=No preservation,
                                                  01=Preserve all, 
                                                  10=Return to factory settings,
                                                  11= Preserve Only Selected Fields

             'switch_to_invaled_nvm_bank' : int[1 bit] -- 0=Keep current NVM Bank  
             'switch_to_invaled_orom_bank': int[1 bit] -- 0=Keep current NV OROM Bank
             'switch_to_invaled_ext_tlv_bank': int[1 bit] -- 0= Keep current EXT TLV Bank

        '''
        byte_19 = ((config.get("switch_to_invaled_ext_tlv_bank", 0) & 0x1) << 5) |((config.get("switch_to_invaled_orom_bank", 0) & 0x1) << 4) |((config.get("switch_to_invaled_nvm_bank", 0) & 0x1) << 3) | ((config.get('preserrvation_mode', 0x3) & 0x3 )<< 1) | 0
 
        buffer = list()
        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x707
        aq_desc.flags = 0x0 
        aq_desc.param0 =  (byte_19 << 24) & 0xffffffff
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.datalen = len(buffer)
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Nvm Config Write Admin Command, status: {} , FW ret value: {}'.format(status, aq_desc.retval))
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)
        return status

    def SaveFactorySettings(self, debug=False):
        '''
            saves the PFA, active Topology Netlist, and 32B header to a permanent read only NVM location

        '''
        buffer = list() 
        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x708
        aq_desc.datalen = len(buffer)
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Save Factory Settings Admin Command, status: {} , FW ret value: {}'.format(status, aq_desc.retval))
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)
        return status


    def NvmUpdateEmpr(self, debug=False):
        '''
           request an EMPR after a successful reset to allow activation of the new firmware

        '''
        buffer = list() 
        aq_desc = AqDescriptor()
        aq_desc.opcode = 0x709
        aq_desc.datalen = len(buffer)
        status = self.driver.send_aq_command(aq_desc, buffer, debug)
        if status != 0 or aq_desc.retval != 0:
            print('Failed to send Save Factory Settings Admin Command, status: {} , FW ret value: {}'.format(status, aq_desc.retval))
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag
        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            status = (False, None)
        return status
###############################################################################


#TODO delete this class and move it's functionality somewhere else
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
        #TODO finish this dict based on table 9-55 Resoruce recognized by this verison of the command
        #TODO implement a new calss that holds these values as class member and not as instance members
