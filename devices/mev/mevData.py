
from data.common.commonData import commonData


class mevData(commonData):

    mev_default_itd_lut = { "_comment": "ITD lookup table (max_temp values are in Celsius, resolution of *_delta in mv)",
                            "max_temp":[43,47,51,55,59,63,67,71,75,79,125],
                            "vnn_delta":[10,9,8,7,6,5,4,3,2,1,0],
                            "vcc_delta":[10,9,8,7,6,5,4,3,2,1,0]}
    
    mev_vnn_rail_name = "VNN_0V74"
    
    mev_vcc_rail_name = "VCC_1V04"

    mev_default_vnn = 0.74
    
    mev_default_vcc = 1.08
    
    mev_default_thermtrip_b_threshold = 122

    mev_default_nichot_b_threshold = 100

    mev_default_nichot_b_thershold_hysteresis = 95

    mev_fuse_default_pvt_vid_vcc_pm = 0b10001100
    
    mev_fuse_default_pvt_vid_vcc_sm = 0b10001100

    mev_fuse_default_pvt_vid_vnn = 0b01011010

    mev_offset_g = 57.4

    mev_slope_h = 249.4

    mev_pvt_config_file_path = "/etc/hwconf/active/pvt"

    mev_pvt_log_file_path = "/var/dts_log.txt"
    
    mev_cattrip_fuse_temperature_setting  = {0b0000: 125,
                                             0b0001: 124.5,
                                             0b0010: 124.0,
                                             0b0011: 123.5,
                                             0b0100: 123.0,
                                             0b0101: 122.5,
                                             0b0110: 122.0,
                                             0b0111: 121.5,
                                             0b1000: 121.0,
                                             0b1001: 120.5,
                                             0b1010: 120.0,
                                             0b1011: 119.5,
                                             0b1100: 119.0,
                                             0b1101: 118.5,
                                             0b1110: 118.0,
                                             0b1111: 117.5}
   
    class clk_cpu:
        base_address = 0x3e00000
        cpu_pll_cfg_0_inst = base_address + 0
        cpu_pll_cfg_1_inst = base_address + 0x4
        cpu_pll_cfg_2_inst = base_address + 0x8
        cpu_pll_cfg_3_inst = base_address + 0xc
        cpu_pll_cfg_4_inst = base_address + 0x10
        cpu_pll_cfg_5_inst = base_address + 0x14
        cpu_pll_cfg_6_inst = base_address + 0x18
        mem_remap_cfg_8_inst = base_address + 0x1c
        cpu_pll_ro_0_inst = base_address + 0x20
 
    class pvt_0:
        base_address = 0xfc00000
        pvt_comp_id = base_address + 0
        irq_ts_status = base_address + 0x64
    
    class pvt_1:
        base_address = 0xfe00000
        pvt_comp_id = base_address + 0
        irq_ts_status = base_address + 0x64
        
    class syscon:
        base_address = 0x2800000
        int_en = base_address + 0x2224
        int_stat = base_address + 0x2220
        int_stat_test = base_address + 0x2228
        
    class otp:
        base_address = 0x4c00000
        otp_efuse_data00 = base_address + 0x100 # 0-3
        otp_efuse_data01 = base_address + 0x104 # 4-7
        otp_efuse_data02 = base_address + 0x108 # 8-11
        otp_efuse_data03 = base_address + 0x10c # 12-15
        otp_efuse_data04 = base_address + 0x110
        otp_efuse_data05 = base_address + 0x114
        otp_efuse_data06 = base_address + 0x118
        otp_efuse_data07 = base_address + 0x11c
        otp_efuse_data08 = base_address + 0x120
        otp_efuse_data09 = base_address + 0x124
        otp_efuse_data0a = base_address + 0x128
        otp_efuse_data0b = base_address + 0x12c
        otp_efuse_data0c = base_address + 0x130
        otp_efuse_data0d = base_address + 0x134
        otp_efuse_data0e = base_address + 0x138
        otp_efuse_data0f = base_address + 0x13c
        otp_efuse_data10 = base_address + 0x140
        otp_efuse_data11 = base_address + 0x144
        otp_efuse_data12 = base_address + 0x148
        otp_efuse_data13 = base_address + 0x14c
        otp_efuse_data14 = base_address + 0x150
        otp_efuse_data15 = base_address + 0x154
        otp_efuse_data16 = base_address + 0x158
        otp_efuse_data17 = base_address + 0x15c
        otp_efuse_data18 = base_address + 0x160
        otp_efuse_data19 = base_address + 0x164
        otp_efuse_data1a = base_address + 0x168
        otp_efuse_data1b = base_address + 0x16c
        otp_efuse_data1c = base_address + 0x170
        otp_efuse_data1d = base_address + 0x174
        otp_efuse_data1e = base_address + 0x178
        otp_efuse_data1f = base_address + 0x17c 
        
        get_address_by_byte = lambda byte: (0x4c00000 + 0x100 + (int(byte/4)*4), byte%4)
        # tuples (address, byte_offset, mask, bit_offset)
        pvt_use_uncalibrated_ts = get_address_by_byte(63) + (0x1, 3)
        pvt_ts_cattrip = get_address_by_byte(63) + (0xf, 4) 
        pvt_ts_cattrip_disable = get_address_by_byte(63) + (0x1, 8)
        pvt_vid_vcc_sm = get_address_by_byte(66) + (0xff,)
        pvt_vid_vcc_pm = get_address_by_byte(99) + (0xff,)
        pvt_vid_vnn = get_address_by_byte(100) + (0xff,)
        pvt_vnn_itd_disable = get_address_by_byte(101) + (0x1,)
        pvt_vcc_itd_disable = get_address_by_byte(101) + (0x1, 1)
        pvt_ares_max_frequency = get_address_by_byte(101) + (0x1f,)
        
