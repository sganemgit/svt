
from data.common.commonData import commonData

class mevData(commonData):

    mev_default_itd_lut = { "_comment": "ITD lookup table (max_temp values are in Celsius, resolution of *_delta in mv)",
                            "max_temp":[43,47,51,55,59,63,67,71,75,79,125],
                            "vnn_delta":[10,9,8,7,6,5,4,3,2,1,0],
                            "vcc_delta":[10,9,8,7,6,5,4,3,2,1,0]}
