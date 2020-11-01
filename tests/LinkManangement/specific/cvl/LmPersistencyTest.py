
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
        self.poll_for_link(dut, lp, 15)

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
                lenient_mode = dut.GetCurrentModuleComplianceEnforcement()
                self.log.info("Current lenient mode : {}".format(lenient_mode))
                if lenient_mode != 'strict':
                    self.log.info("Disabling lenient mode")
                    dut.DisableLenientMode()
                    lenient_mode = dut.GetCurrentModuleComplianceEnforcement()
                    self.log.info("Current lenient mode after diabling attempt : {}".format(lenient_mode))
                    if lenient_mode != 'strict':
                        self.append_fail_reason("lenient mode is not changing. current mode is {}".format(lenient_mode))
                        raise RuntimeError("can not alter lenient mode")

                #read current PFA 
                current_NVM_PFA = dut.ReadNvmModuleByTypeId(self.module_type_id)

                data = dut.GetPhyAbiliesFields()
                #create new config dict for DUT port
                new_config= dict()
                new_config['port'] = dut.port_number
                new_config['lenient'] = 0x0
                new_config['epct_ability_enable'] = 0x0
                new_config['port_disable'] = 0x0
                new_config['override_enable'] = 0x1
                new_config['disable_automatic_link'] = 0x0
                new_config['eee_enable'] = data['eee_cap'] 
                new_config['pause_ability'] = data['pause_abil']
                new_config['lesm_enable'] = data['lesm_en']
                new_config['auto_fec_enable'] = data['auto_fec_en'] 
                new_config['fec_options'] = data['fec_opt']
                new_config['override_phy_types'] = 0x1
                new_config['override_disable_automatic_link'] = 0x1
                new_config['override_eee'] = 0x1
                new_config['override_pause'] = 0x1
                new_config['override_lesm_enable'] = 0x1
                new_config['override_fec'] = 0x1
                new_config['phy_types'] = 0xffffffffffffffffffffffffffffffff

                #setdefaultmask by calling the method for the dut 

                print(new_config)
                dut.SetDefaultOverrideMask(new_config)
                

                #perform empr reset . could be that we will need POR
                for dut, lp in self.dut_lp_pairs:
                    self.reset_both_sides(dut, lp, 'empr')
                
                #read new configurations
                new_lenient_mode = dut.GetCurrentModuleComplianceEnforcement()

                # if changes are persistent after reset then test will pass. else fail.
                if new_lenient_mode == 'strict':
                    self.append_fail_reason("lenient mode did not stay persistent after an empr")

                self.log.info("current lenient mode is {}".format(new_lenient_mode))

            except Exception as e:
                print(str(e))
                self.append_fail_reason("Exception was raised during the test setting test to fail")

