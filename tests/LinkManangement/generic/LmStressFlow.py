
import time
from GenericLinkManagement import GenericLinkManagement
from core.utilities.Timer import Timer


class LmStressFlow(GenericLinkManagement):


    def do_traffic_before_stress(self, dut = None, lp = None):
        print("starting traffic before stress")

    def do_traffic_after_stress(self, dut = None, lp = None):
        print("starting traffic after stress")

    def run(self):
        run_time = 6
        timer = Timer(self.args.get('run_time', 60))
        timer.start()
        while not timer.expired():
            print("*"*10)
            self.log.info("="*10 + " Iteration Number {} ".format(self.test_iteration) + "="*10, 'g')
            for dut, lp in self.dut_lp_pairs:
                self.do_traffic_before_stress(dut ,lp)
                self.perform_stress(dut, lp)
                self.do_traffic_after_stress(dut, lp)
            self.test_iteration += 1
