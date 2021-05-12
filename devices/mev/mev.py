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
        return self.data.mev_default_thermtrip_b_threshold

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
        #TODO return fuse value via sv driver
        pass

    def get_pvt_vid_vcc_sm(self):
        #TODO return fuse value via sv driver
        pass

    def get_pvt_vid_vnn(self):
        #TODO return fuse value via sv driver
        pass

    def get_pvt_vnn_itd_disable(self):
        #TODO return fuse value via sv driver
        pass
        
    def get_pvt_vcc_itd_disable(self):
        #TODO return fuse value via sv driver
        pass
    
    def get_pvt_ts_cattrip_disable(self):
        #TODO return fuse value via sv driver
        pass
    
    def get_pvt_use_uncalibrated_ts(self):
        #TODO return fuse value via sv driver
        pass
    
    def get_PVT_TS_CATTRIP_6_0(self):
        #TODO return fuse value via sv driver
        pass
    
    def get_all_tm_fuses(self):
        #TODO finish this method by calling the other mehtods
        fuse_dict = dict()
        return fuse_dict
 
    def get_acc_ss_cpu_clk_status(self):
        if self.driver is not None:
            core_pll_cfg_dict = dict()
            cfg_1 = self.driver.read_csr(self.data.mev_cpu_cfg_pll_1_inst)
            cfg_2 = self.driver.read_csr(self.data.mev_cpu_cfg_pll_2_inst)

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
            
            #TODO finish this method. should return a dict with the each pll clk


