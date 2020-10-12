
import time
from GenericLinkManagement import GenericLinkManagement
from core.utilities.Timer import Timer

class LmStressFlow(GenericLinkManagement):

    def init_test_params(self):
        self.log.info("-"*60)
        self.log.info("Received Parameters:")
        for key, value in self.args.items():
            self.log.info("{}: {}".format(key, value))
        self.log.info("-"*60)
        self.number_of_packets = int(self.args.get('number_of_packets', self.get_random_number_of_packets()))
        self.packet_size = int(self.args.get('packet_size', self.get_random_packet_size()))
        self.run_time = int(self.args.get('run_time', 60))
        self.stress_quantity = int(self.args.get('stress_quantity',1))
        self.ring_id = int(self.args.get('ring_id', 0))

    def run(self):
        self.init_test_params()

        self.log.info("performing globr reset on all pfs")
        for dut, lp in self.dut_lp_pairs:
            dut.Reset('globr')
            lp.Reset('globr')

        timer = Timer(self.run_time)
        timer.start()
        while not timer.expired():

            self.log.info("="*10 + " Iteration Number {} ".format(self.test_iteration) + "="*10, 'g')
            for dut, lp in self.dut_lp_pairs:
                self.do_traffic_before_stress(dut ,lp)
                for i in range(self.stress_quantity):
                    self.log.info("stress iteration {}".format(i))
                    self.do_stress(dut, lp)
                self.do_traffic_after_stress(dut, lp)
            self.test_iteration += 1
