
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
    
    mev_default_thermtrip_b_threshold = 125
    
    mev_default_nichot_b_threshold = 100

    mev_fuse_default_pvt_vid_vcc_pm = 0b10001100
    
    mev_fuse_default_pvt_vid_vcc_sm = 0b10001100

    mev_fuse_default_pvt_vid_vnn = 0b01011010

    mev_offset_g = 57.4

    mev_slope_h = 249.4

    
    
