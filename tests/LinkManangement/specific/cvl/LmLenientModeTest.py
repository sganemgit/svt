
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

    def does_default_override_maks_exist(self, dut): 
        pfa_status = dut.GetCurrentPfaOverrideMaskStatus()
        return pfa_status['override_enable']

    def run(self):
        self.init_params()

        for dut, lp in self.dut_lp_pairs:
            self.log.info(dut.info())
            self.log.info(lp.info())
            self.reset_both_sides(dut, lp, 'globr')

        for dut, lp in self.dut_lp_pairs:
            #this test will check all the cases according to spreedsheet of DCR102
            dut_default_override_mask_enabled = self.does_default_override_maks_exist(dut)
            lenient_mode = dut.GetCurrentModuleComplianceEnforcement()
            phy_abilities = dut.GetPhyTypeAbilities(1)
            
            if dut_default_override_mask_enabled:
                if phy_abilities:
                    #phy abilities with media has modes
                    if lenient_mode == 'strict':
                        self.log.info("link attempted based on default override mask config but only if support declarded by media")
                    elif lenient_mode == 'lenient':
                        self.log.info("link attempted based on default override maks config")
                else:
                    if lenient_mode == 'strict':
                        self.log.info("Error message is logged with information about media and link")
                    elif lenient_mode == 'lenient':
                        self.log.info("link attemted based on AN and 4 hihest AUI modes in netlist and warning message is logged with information about Media")
            else:
                self.log.info("Dut default override maks is disabled")
                if phy_abilities:
                    self.log.info("GetPhyAbilities with media has modes")
                    self.log.info("lenient mode {}".format(lenient_mode))
                    self.log.info("link attempted based on support declared by media")
                else:
                    self.log.info("GetPhyAbilities with media is empty")
                    self.log.info("lenient mode {}".format(lenient_mode))
                    if lenient_mode == 'strict':
                        self.log.info("Error message is logged with information about media and link")
                    if lenient_mode == 'lenient':
                        self.log.info("link attemted based on AN and 4 highest AUI modes in netlist and warning message is logged with information about Media")

