
# @author Shady Ganem <shady.ganem@intel.com>

from core.drivers.svdriver.SvDriver import SvDriver

import libPyMevCp

class SnicDriver(SvDriver):

    #TODO move this mbx methods to a base class to reuse the same code with other driver types
    def send_mbx_to_peer_pf(self, fucn_id, msg, opcode):
        dp = self._driver_proxy
        mbox_queue = dp.create_mail_box_queue()
        rc, retval = mbox_queue.send_to_peer_pf(fucn_id, msg, opcode)
        if rc != 0:
            raise Exception("Send to peer Driver: status {}".format(dp.driver_error_to_string(rc)))
        return retval

    #TODO move this mbx methods to a base class to reuse the same code with other driver types
    def send_mbx_to_peer_driver(self, host_id, queue, msg, opcode):
        dp = self._driver_proxy
        mbox_queue = dp.create_mail_box_queue()
        rc, retval = mbox_queue.send_to_peer_driver(host_id, queue, msg, opcode)
        if rc != 0:
            raise Exception("Send to peer Driver: status {}".format(dp.driver_error_to_string(rc)))
        return retval

