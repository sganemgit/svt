
# @author Shady Ganem <shady.ganem@intel.com>

from devices.mev.mevBase import mevBase

class mev(mevBase):

    def info(self):
        print ("mev1")

    def scan_ftdi_devices(self):
        pass

    def get_voltage(self, rail_name="all"):
        if self.fpga is not None:
            if rail_name is "all":
                return self.fpga.read_all_voltages()
            else:
                return self.fpga.read_voltage_by_rail_name(rail_name)
        else: 
            return None

    def get_diode_temperature(self):
        if self.fpga is not None:
            return self.fpga.read_thermal_diode()
        else:
            return None

    def get_rail_names_list(self):
        if self.fpga is not None:
            return self.fpga.get_rail_name_list()
        else:
            return None

    def get_itd_lut(self, mode="SM"):
        '''
            This method return the itd lookup Table
            mode = SM/PM standard mode/performance mode
        '''
        #TODO this method must retreive the LUT from file /etc/hwconf/active/pvt from the imc filesystem
        return self.data.mev_default_itd_lut

    def get_nichot_status(self):
        if self.fpga is not None:
            return self.fpga.get_nichot_status()
        else:
            return None

    def get_thermtrip_status(self):
        if self.fpga is not None:
            return self.fpga.get_thermtrip_status()
        else:
            return None

    def get_thermtrip_threshold(self):
        pvt_ts_cattrip_disable = self.get_pvt_ts_cattrip_disable()
        if pvt_ts_cattrip_disable:
            return self.data.mev_default_thermtrip_b_threshold
        else:
            pvt_ts_cattrip_fuse = self.get_pvt_ts_cattrip()
            return self.data.mev_cattrip_fuse_temperature_setting[pvt_ts_cattrip_fuse]

    def get_nichot_threshold(self, hysteresis_direction="up"):
        if hysteresis_direction == "up":
            return self.data.mev_default_nichot_b_threshold
        elif hysteresis_direction == "down":
            return self.data.mev_default_nichot_b_thershold_hysteresis

    def get_thermtrip_thershold(self, hysteresis_dircetion="up"):
        if hysteresis_dircetion == "up":
            return self.data.mev_default_thermtrip_b_threshold
        elif hysteresis_dircetion == "down":
            return self.data.mev_default_thermtrip_b_threshold_hysteresis

    def get_pvt_vid_vcc_pm(self):
        address, offset, mask = self.data.otp.pvt_vid_vcc_pm
        fuse = self.driver.read_csr(address)
        return (fuse >> (8*offset)) & mask

    def get_pvt_vid_vcc_sm(self):
        address, offset, mask = self.data.otp.pvt_vid_vcc_sm
        fuse = self.driver.read_csr(address)
        return (fuse >> (8*offset)) & mask

    def get_pvt_vid_vnn(self):
        address, offset, mask = self.data.otp.pvt_vid_vnn
        fuse = self.driver.read_csr(address)
        return (fuse >> (8*offset)) & mask

    def get_pvt_vnn_itd_disable(self):
        address, offset, mask = self.data.otp.pvt_vnn_itd_disable
        fuse = self.driver.read_csr(address)
        return (fuse >> (8*offset)) & mask
        
    def get_pvt_vcc_itd_disable(self):
        address, offset, mask = self.data.otp.pvt_vcc_itd_disable
        fuse = self.driver.read_csr(address)
        return (fuse >> (8*offset)>>1) & mask
    
    def get_pvt_ts_cattrip_disable(self):
        address, offset, mask = self.data.otp.pvt_ts_cattrip_disable
        fuse = self.driver.read_csr(address)
        return ((fuse >> (8*offset))>>8) & mask
    
    def get_pvt_use_uncalibrated_ts(self):
        address, offset, mask = self.data.otp.pvt_use_uncalibrated_ts
        fuse = self.driver.read_csr(address)
        return ((fuse >> (8*offset))>> 3) & mask
    
    def get_pvt_ts_cattrip(self):
        address, offset, mask = self.data.otp.pvt_ts_cattrip
        fuse = self.driver.read_csr(address)
        return ((fuse >> (8*offset))>> 4) & mask
    
    def get_all_tm_fuses(self):
        #TODO finish this method by calling the other mehtods
        fuse_dict = dict()
        return fuse_dict
    
    def dump_otp_efuse(self):
        fuse_list = list()
        for word in range(32):
            fuse_list.append(self.driver.read_csr(self.data.otp.base_address + 0x100 + (word*4)) + 2**32)
        return fuse_list
 
    def get_acc_ss_cpu_clk_status(self):
        if self.driver is not None:
            refdiv_to_clk_map = {0x1: "25MHz"}
            fbdiv_to_str_clk_map = {0xf0: "6000MHz", 
                                    0xd8: "5400MHz", 
                                    0xa0: "4000MHz"}
            
            fbdiv_to_int_clk_map = {0xf0: 6000, 
                                    0xd8: 5400, 
                                    0xa0: 4000}

            pll_cfg_dict = dict()
            cfg_0 = self.driver.read_csr(self.data.clk_cpu.cpu_pll_cfg_0_inst)
            cfg_1 = self.driver.read_csr(self.data.clk_cpu.cpu_pll_cfg_1_inst)
            cfg_2 = self.driver.read_csr(self.data.clk_cpu.cpu_pll_cfg_2_inst)
            
            pll_en = cfg_0 & 0x1
            fout_en = (cfg_0 >> 1) & 0xf
            fbdiv = (cfg_0 >> 8) & 0xfff
            bypass_en = (cfg_0 >> 26) & 0xf
            vcodivsel = (cfg_0 >> 30) & 0x1
            refclkdiv = (cfg_2 >> 16) & 0x3f

            #cores 0,1,2,3
            postdiv_2a = (cfg_1 >>  16) & 0x7
            postdiv_2b = (cfg_1 >>  19) & 0x7
            #cores 6,7,8,9
            postdiv_3a = (cfg_1 >>  24) & 0x7
            postdiv_3b = (cfg_1 >>  27) & 0x7
            #core 10,11,12,13
            postdiv_4a = cfg_2 & 0x7
            postdiv_4b = (cfg_2 >> 3) & 0x7
            #cores 3,4,14,15
            postdiv_5a = (cfg_2 >> 8) & 0x7 
            postdiv_5b = (cfg_2 >> 11) & 0x7 
            
            pll_cfg_dict["reference_clock"] = refdiv_to_clk_map.get(refclkdiv, "N/A")
            pll_cfg_dict["pll_enable"] = pll_en 
            pll_cfg_dict["pll_vco"] = vco_clk = fbdiv_to_int_clk_map.get(fbdiv, "N/A") # in MHz
            pll_cfg_dict["fanout_enable"] = fout_en

            pll_cfg_dict["cores_0_1_2_3"] = int(vco_clk/((postdiv_2a+1)*(postdiv_2b+1)))
            pll_cfg_dict["cores_6_7_8_9"] =  int(vco_clk/((postdiv_3a+1)*(postdiv_3b+1)))
            pll_cfg_dict["cores_10_11_12_13"] = int(vco_clk/((postdiv_4a+1)*(postdiv_4b+1)))
            pll_cfg_dict["cores_3_4_14_15"] = int(vco_clk/((postdiv_4a+1)*(postdiv_4b+1)))
            
            return pll_cfg_dict

