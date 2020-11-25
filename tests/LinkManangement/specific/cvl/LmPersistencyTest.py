
TEST = True

from core.tests.testBase import testBase
import time

class LmPersistencyTest(testBase):

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

    def reset_both_sides(self, dut,lp,reset):
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

    def run(self):
        self.init_params()

        for dut, lp in self.dut_lp_pairs:
            self.log.info(dut.info())
            self.log.info(lp.info())
            self.reset_both_sides(dut, lp, 'globr')

        for dut, lp in self.dut_lp_pairs:
            #check lenient mode and log it
            try:
                self.log.info("Testing pfa persistency after an empr", 'o')
                self.log.info("DUT port number: {}".format(dut.port_number))
                self.log.info("LP  port number: {}".format(lp.port_number))

                #read current PFA 
                self.log.info('reading module type id {}'.format(self.module_type_id))
                current_pfa_value = dut.ReadNvmModuleByTypeId(self.module_type_id)
                pfa_data = current_pfa_value['nvm_module']

                dut.ResetDefaultOverrideMask(int(dut.port_number))
                lp.ResetDefaultOverrideMask(int(lp.port_number))

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
                
                #perform empr reset . could be that we will need POR
                self.reset_both_sides(dut, lp, 'empr')
                
                self.log.info('reading module type id {} after changes'.format(hex(self.module_type_id)))
                current_pfa_value = dut.ReadNvmModuleByTypeId(self.module_type_id)

                new_pfa_data = current_pfa_value['nvm_module']

                if new_pfa_data == pfa_data:
                    self.append_fail_reason("pfa did not remain persistent after emp")

            except Exception as e:
                print(str(e))
                self.append_fail_reason("Exception was raised during the test setting test to fail")
            finally:
                self.log.info("resetting default override mask values to default")
                dut.ResetDefaultOverrideMask(int(dut.port_number))
                lp.ResetDefaultOverrideMask(int(lp.port_number))


