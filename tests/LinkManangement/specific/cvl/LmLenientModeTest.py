
TEST = True 

from core.tests.testBase import testBase

class LmLenientModeTest(testBase):

    def poll_for_link(self, dut, lp, timeout):
        log = self.log
        start_time = time.time()
        end_time = time.time() + timeout
        while time.time() < end_time:
            dut_link = dut.GetMacLinkStatus()
            lp_link = lp.GetMacLinkStatus()
            if dut_link == 1  and lp_link == 1:
                log.info("link is up on dut port {}".format(dut.port_number))
                log.info("link is up on lp port {}".format(lp.port_number))
                log.info("TTL = {}".format(time.time() - start_time))
                return True
        log.info("link is down on dut port {} and lp port {}".format(dut.port_number,lp.port_number),'r')
        self.append_fail_reason("link is down on dut port {} and lp port {}".format(dut.port_number,lp.port_number))
        return False

    def reset_both_sides(self, dut, lp, reset):
        log = self.log
        log.info("performing {} reset on lp".format(reset))
        lp.Reset(reset)
        log.info("performing {} reset on dut".format(reset))
        dut.Reset(reset)

    def init_params(self):
        self.log.info("-"*80)
        self.log.info("Received Parameters:")
        for key, value in self.args.items():
            self.log.info("{}: {}".format(key, value))
        self.log.info("-"*80)
        self.phy_type = self.args['phy_type']
        self.module_type_id = 0x134
    
    def configure_link(self, dut, lp, PhyType, FecType):
        log = self.log
        try:
            if PhyType in dut.data.ieee_802_3_force_phy_type_list:
                log.info("{} does not support AN".format(PhyType), 'o')
                log.info("setting dut to {} with fec {}".format(PhyType, FecType), 'o')
                dut.SetPhyConfiguration(PhyType,FecType)
                log.info("setting lp to {} with fec {}".format(PhyType, FecType), 'o')
                lp.SetPhyConfiguration(PhyType,FecType)
            else:
                lp.DisableFECRequests(0)
                log.info("setting dut to {} with fec {}".format(PhyType, FecType), 'o')
                dut.SetPhyConfiguration(PhyType,FecType)
        except Exception as e:
            log.info("Exception {} raised in {}".format(str(e), self.configure_link.__name__))
            self.append_fail_reason("Fail to configure link of {} ".format(PhyType))

    def is_default_override_mask_set(self, device): 
        pfa_status = device.GetCurrentPfaOverrideMaskStatus()
        return pfa_status['override_enable'] and pfa_status['override_phy_types']

    def check_link_correctness(self, dut, lp):
        dut_phy_abil = dut.GetPhyTypeAbilities(4)
        lp_phy_abil = lp.GetPhyTypeAbilities(4)
        if dut.GetCurrentLinkStatus() == 'UP':
            self.log.info("dut link is up")
            dut_phy_type = dut.GetCurrentPhyType() 
            if dut_phy_type:
                self.log.info("current dut phy type is {}".format(dut_phy_type))
            if dut_phy_type in dut_phy_abil:
                self.log.info("dut phy type exists in default phy capabilites")
                return True
            else:
                self.log.info("dut phy type does not exist in default phy capabilities")
                return False
        else: 
            self.log.info("dut link is down")
            if dut_phy_abil:
                self.log.info("dut default phy capablities:")
                for phy_type in dut_phy_abil:
                    self.log.info(phy_type)
                return False
            else: 
                self.log.info("dut default phy types list is empty")
                return True

    def run(self):
        self.init_params()

        for dut, lp in self.dut_lp_pairs:
            self.log.info(dut.info())
            self.log.info(lp.info())
            self.reset_both_sides(dut, lp, 'globr')

        for dut, lp in self.dut_lp_pairs:
            #this test will check all the cases according to spreedsheet of DCR102
            lenient_mode = dut.GetCurrentModuleComplianceEnforcement()
            phy_abilities = dut.GetPhyTypeAbilities(1)
            
            #testing with override from pfa disabled this behavior 
            try:
                self.log.info("Testing automatic link behavior when override from pfa is unset", 'o')
                self.log.info("DUT port number: {}".format(dut.port_number))
                self.log.info("LP  port number: {}".format(lp.port_number))

                dut.ResetDefaultOverrideMask(int(dut.port_number))
                lp.ResetDefaultOverrideMask(int(dut.port_number))

                dut_override_from_pfa = self.is_default_override_mask_set(dut)
                lp_override_from_pfa = self.is_default_override_mask_set(lp)
                if dut_override_from_pfa:
                    raise Exception("unable to disable Default override mask on dut")
                if lp_override_from_pfa:
                    raise Exception("unable to disable Default override mask on lp")
                
                link_correctness_status = self.check_link_correctness(dut, lp)
                if  link_correctness_status:
                    self.log.info("dut link complies with DCR 181 and 102", 'g')
                else: 
                    self.append_fail_reason("dut link does not compllie with DCR 181 and 102")
                
            
            except Exception as e:
                self.log.info(str(e))
                self.append_fail_reason("Exception raised while testing link behavior with default overrid mask disabled")


            try:
                self.log.info("Testing automatic link behavior when lenient mode enabled and override from pfa is set", 'o')
                self.log.info("DUT port number: {}".format(dut.port_number))
                self.log.info("LP  port number: {}".format(lp.port_number))
                
                data = dut.GetPhyAbilitiesFields()
                #create new config dict for DUT port
                new_config= dict()
                new_config['port'] = dut.port_number
                new_config['lenient'] = 0x0
                new_config['epct_ability_enable'] = 0x0
                new_config['port_disable'] = 0x0
                new_config['override_enable'] = 0x1
                new_config['disable_automatic_link'] = 0x0
                new_config['eee_enable'] =  1  
                new_config['pause_ability'] = 0x3
                new_config['lesm_enable'] = 0x1
                new_config['auto_fec_enable'] = data['auto_fec_en']
                new_config['fec_options'] = data['fec_opt']
                new_config['override_phy_types'] = 0x1
                new_config['override_disable_automatic_link'] = 0x1
                new_config['override_eee'] = 0x1
                new_config['override_pause'] = 0x1
                new_config['override_lesm_enable'] = 0x1
                new_config['override_fec'] = 0x1
                new_config['phy_types'] = 0xffffffffffffffffffffffffffffffff #this is a mask for bitwise with 128 bit phy_type 

                self.log.info("Setting the fields in the DefaultOverrideMask PFA to the following values")
                for key, val in new_config.items():
                    self.log.info("{} : {}".format(key, hex(val)))  
                #setdefaultmask by calling the method for the dut 
                dut.SetDefaultOverrideMask(new_config)


                data = lp.GetPhyAbilitiesFields()
                #create new config dict for lp port
                new_config= dict()
                new_config['port'] = lp.port_number
                new_config['lenient'] = 0x0
                new_config['epct_ability_enable'] = 0x0
                new_config['port_disable'] = 0x0
                new_config['override_enable'] = 0x1
                new_config['disable_automatic_link'] = 0x0
                new_config['eee_enable'] =  1  
                new_config['pause_ability'] = 0x3 
                new_config['lesm_enable'] = 0x1
                new_config['auto_fec_enable'] = data['auto_fec_en']
                new_config['fec_options'] = data['fec_opt']
                new_config['override_phy_types'] = 0x1
                new_config['override_disable_automatic_link'] = 0x0
                new_config['override_eee'] = 0x1
                new_config['override_pause'] = 0x1
                new_config['override_lesm_enable'] = 0x1
                new_config['override_fec'] = 0x1
                new_config['phy_types'] = 0xffffffffffffffffffffffffffffffff #this is a mask for bitwise with 128 bit phy_type 

                self.log.info("Setting the fields in the DefaultOverrideMask PFA to the following values")
                for key, val in new_config.items():
                    self.log.info("{} : {}".format(key, hex(val)))  
                #setdefaultmask by calling the method for the lp 
                lp.SetDefaultOverrideMask(new_config)

                dut_override_from_pfa = self.is_default_override_mask_set(dut)
                lp_override_from_pfa = self.is_default_override_mask_set(lp)

                if not dut_override_from_pfa:
                    raise Exception("unable to enable Default override mask on dut")
                if not lp_override_from_pfa:
                    raise Exception("unable to enable Default override mask on lp")
              
                if dut.GetCurrentModuleComplianceEnforcement() == 'strict':
                    self.log.warning("dut leneint mode is strict")
                    self.log.info("enabling lenient mode") 
                    dut.EnableLenientMode()
                if dut.GetCurrentModuleComplianceEnforcement() == 'strict':
                    self.append_fail_reason("unable to alter leneint mode dut")
                    raise RuntimeError

                if lp.GetCurrentModuleComplianceEnforcement() == 'strict':
                    self.log.warning("lp leneint mode is strict")
                    self.log.info("enabling lenient mode") 
                    lp.EnableLenientMode()
                if lp.GetCurrentModuleComplianceEnforcement() == 'strict':
                    self.append_fail_reason("unable to alter leneint mode on lp")
                    raise RuntimeError

                link_correctness_status = self.check_link_correctness(dut, lp)
                if  link_correctness_status:
                    self.log.info("dut link complies with DCR 181 and 102", 'g')
                else: 
                    self.append_fail_reason("dut link does not compllie with DCR 181 and 102")
            
            except Exception as e:
                self.log.info(str(e))
                self.append_fail_reason("Exception raised while testing lenient mode with default overrid mask disable")
            finally:
                dut.ResetDefaultOverrideMask(int(dut.port_number))
                lp.ResetDefaultOverrideMask(int(dut.port_number))

            try:
                self.log.info("Testing automatic link behavior when lenient mode disabled and override from pfa is set", 'o')
                self.log.info("DUT port number: {}".format(dut.port_number))
                self.log.info("LP  port number: {}".format(lp.port_number))
                
                data = dut.GetPhyAbilitiesFields()
                #create new config dict for DUT port
                new_config= dict()
                new_config['port'] = dut.port_number
                new_config['lenient'] = 0x1
                new_config['epct_ability_enable'] = 0x0
                new_config['port_disable'] = 0x0
                new_config['override_enable'] = 0x1
                new_config['disable_automatic_link'] = 0x0
                new_config['eee_enable'] =  1 #data['eee_cap'] 
                new_config['pause_ability'] = 0x3 #data['pause_abil']
                new_config['lesm_enable'] = 0x1
                new_config['auto_fec_enable'] = data['auto_fec_en']
                new_config['fec_options'] = data['fec_opt']
                new_config['override_phy_types'] = 0x1
                new_config['override_disable_automatic_link'] = 0x1
                new_config['override_eee'] = 0x1
                new_config['override_pause'] = 0x1
                new_config['override_lesm_enable'] = 0x1
                new_config['override_fec'] = 0x1
                new_config['phy_types'] = 0xffffffffffffffffffffffffffffffff #this is a mask for bitwise with 128 bit phy_type 

                self.log.info("Setting the fields in the DefaultOverrideMask PFA to the following values")
                for key, val in new_config.items():
                    self.log.info("{} : {}".format(key, hex(val)))  
                #setdefaultmask by calling the method for the dut 
                dut.SetDefaultOverrideMask(new_config)

                data = lp.GetPhyAbilitiesFields()
                #create new config dict for lp port
                new_config= dict()
                new_config['port'] = lp.port_number
                new_config['lenient'] = 0x1
                new_config['epct_ability_enable'] = 0x0
                new_config['port_disable'] = 0x0
                new_config['override_enable'] = 0x1
                new_config['disable_automatic_link'] = 0x0
                new_config['eee_enable'] =  1  
                new_config['pause_ability'] = 0x3 
                new_config['lesm_enable'] = 0x1
                new_config['auto_fec_enable'] = data['auto_fec_en']
                new_config['fec_options'] = data['fec_opt']
                new_config['override_phy_types'] = 0x1
                new_config['override_disable_automatic_link'] = 0x0
                new_config['override_eee'] = 0x1
                new_config['override_pause'] = 0x1
                new_config['override_lesm_enable'] = 0x1
                new_config['override_fec'] = 0x1
                new_config['phy_types'] = 0xffffffffffffffffffffffffffffffff #this is a mask for bitwise with 128 bit phy_type 

                self.log.info("Setting the fields in the DefaultOverrideMask PFA to the following values")
                for key, val in new_config.items():
                    self.log.info("{} : {}".format(key, hex(val)))  
                #setdefaultmask by calling the method for the lp 
                lp.SetDefaultOverrideMask(new_config)

                dut_override_from_pfa = self.is_default_override_mask_set(dut)
                lp_override_from_pfa = self.is_default_override_mask_set(lp)

                if not dut_override_from_pfa:
                    self.append_fail_reason("unblae to enable default override mask on dut")
                    raise RuntimeError

                if not lp_override_from_pfa:
                    self.append_fail_reason("unblae to enable default override mask on lp")
                    raise RuntimeError
              
                if dut.GetCurrentModuleComplianceEnforcement() == 'lenient':
                    self.log.warning("dut lenient mode is lenient")
                    self.log.info("dut Disabling lenient mode")
                    dut.DisableLenientMode()
                if dut.GetCurrentModuleComplianceEnforcement() == 'lenient':
                    self.append_fail_reason("unable to alter leneint mode dut")

                if lp.GetCurrentModuleComplianceEnforcement() == 'lenient':
                    self.log.warning("lp lenient mode is lenient")
                    self.log.info("lp Disabling lenient mode")
                    self.log.warning("leneint mode is enabled")
                    lp.DisableLenientMode()
                if lp.GetCurrentModuleComplianceEnforcement() == 'lenient':
                    self.append_fail_reason("unable to alter leneint mode on lp")
                    raise RuntimeError

                link_correctness_status = self.check_link_correctness(dut, lp)
                if  link_correctness_status:
                    self.log.info("dut link complies with DCR 181 and 102", 'g')
                else: 
                    self.append_fail_reason("dut link does not compllie with DCR 181 and 102")
            
            except Exception as e:
                self.log.info(str(e))
                self.append_fail_reason("Exception raised while testing lenient mode with default overrid mask disable")
            finally:
                dut.ResetDefaultOverrideMask(int(dut.port_number))
                lp.ResetDefaultOverrideMask(int(dut.port_number))
