
import time
from GenericLinkManagement import GenericLinkManagement
from core.utilities.Timer import Timer


class LmStressFlow(GenericLinkManagement):

    def run(self):
        timer = Timer(int(self.args.get('run_time', 60)))
        timer.start()
        while not timer.expired():
            self.log.info("="*10 + " Iteration Number {} ".format(self.test_iteration) + "="*10, 'g')
            for dut, lp in self.dut_lp_pairs:
                self.do_traffic_before_stress(dut ,lp)
                for i in range(int(self.args.get('stress_quantity',1))):
                	self.do_stress(dut, lp)
                self.do_traffic_after_stress(dut, lp)
            self.test_iteration += 1
