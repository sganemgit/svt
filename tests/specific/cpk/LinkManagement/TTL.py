
TEST = True

from core.tests.testBase import testBase

class TTL(testBase):

    def init_params(self):
        self.protocol = self.args.phy_type
    def run(self):
        self.log.info("TTL test")

        for dut, lp in self.dut_lp_pair:
            pass
