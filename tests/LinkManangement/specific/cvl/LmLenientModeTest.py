
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
            #TODO print error message and set fail reason
            log.info("Exception {} raised in {}".format(str(e), self.configure_link.__name__))
            self.append_fail_reason("Fail to configure link of {} ".format(self.phy_type))
            raise e

    def run(self):
        self.init_params()

        for dut, lp in self.dut_lp_pairs:
            self.log.info(dut.info())
            self.log.info(lp.info())
            self.reset_both_sides(dut, lp, 'globr')

        for dut, lp in self.dut_lp_pairs:
            #check lenient mode and log it
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








                    
