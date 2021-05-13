
# @author Shady Ganem <shady.ganem@intel.com>

from core.drivers.svdriver.SvDriver import SvDriver

import libPyMevCp

class SnicDriver(SvDriver):

    def send_mbx_to_peer_pf(self, fucn_id, msg, opcode):
        dp = self._driver_proxy
        mbox_queue = dp.create_mail_box_queue()
        rc, retval = mbox_queue.send_to_peer_pf(fucn_id, msg, opcode)
        if rc != 0:
            raise Exception("Send to peer Driver: status {}".format(dp.driver_error_to_string(rc)))
        return retval

    def send_mbx_to_peer_driver(self, host_id, queue, msg, opcode):
        dp = self._driver_proxy
        mbox_queue = dp.create_mail_box_queue()
        rc, retval = mbox_queue.send_to_peer_driver(host_id, queue, msg, opcode)
        if rc != 0:
            raise Exception("Send to peer Driver: status {}".format(dp.driver_error_to_string(rc)))
        return retval
    
    def read_csr(self, register_offset):
        ''' 
            This method reads 32-bits csr register at offset specified 
            in 'register_offset' and returns register value.            
        '''
        csr_block = self._driver_proxy.csr(self.IP_TYPE['HIF'])
        value = csr_block.read(register_offset)[1]
        self._driver_proxy.dispose_csr_block(csr_block)
        return value

    def write_csr(self, register_offset, write_value):
        '''
            This method writes value specified in 'write_value' 
            to 32-bits csr register at offset specified in 'register_offset'.
        '''  
        csr_block = self._driver_proxy.csr(self.IP_TYPE['HIF'])
        csr_block.write(register_offset, write_value)
        self._driver_proxy.dispose_csr_block(csr_block)
