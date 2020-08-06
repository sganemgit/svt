# @author Shady Ganem <shady.ganem@intel.com>
import libSvPython
import libPyApi
import libPyAdminqApi

import sys
import struct
from ctypes import *
import threading
from core.structs.DeviceInfo import DeviceInfo
from core.structs.AqDescriptor import AqDescriptor
from core.drivers.svdriver.SvDriverCommands import *

############################################################################################
# driver api values

IP_TYPE = {'DEFAULT': libPyApi.IP_DEFAULT, 
           'LAN' : libPyApi.IP_LAN,
           'ICE' : libPyApi.IP_ICE,
           'RDMA' : libPyApi.IP_RDMA,
           'FXP' : libPyApi.IP_FXP,
           'HIF' : libPyApi.IP_HIF,
           'EPL' : libPyApi.IP_EPL,
           'HLP' : libPyApi.IP_HLP,
           'ALL' : libPyApi.IP_ALL,
           'MAX' : libPyApi.IP_MAX}


TX_LIMIT_TYPE = {'FULL_RING': libPyApi.TX_MODE_FULL_RING,
                 'PACKET_COUNT': libPyApi.TX_MODE_PACKET_COUNT_LIMIT,
                 'TIME': libPyApi.TX_MODE_TIME_LIMIT,
                 'INFINTE': libPyApi.TX_MODE_INFINITE}

TX_PACKET_TYPES = {'L2_DRIVER_PACKET': libPyApi.PT_L2_DRIVER_PACKET,
                   'ETH_IPV4' : libPyApi.PT_ETH_IPV4,
                   'ETH_IPV6' : libPyApi.PT_ETH_IPV6,
                   'TCP_IPV4' : libPyApi.PT_TCP_IPV4,
                   'TCP_IPV6' : libPyApi.PT_TCP_IPV4,
                   'UDP_IPV4' : libPyApi.PT_UDP_IPV4,
                   'UDP_IPV6' : libPyApi.PT_UDP_IPV6,
                   'ICMP_IPV4': libPyApi.PT_ICMP_IPV4,
                   'ICMP_IPV6': libPyApi.PT_ICMP_IPV6,
                   'ARP_IPV4' : libPyApi.PT_ARP_IPV4,
                   'ARP_IPV6' : libPyApi.PT_ARP_IPV6,
                   'UNKNOWN' : libPyApi.PT_UNKNOWN}

TX_DESCRIPTOR_TYPES = {'ADV_CONTEXT': libPyApi.TXDT_ADV_CONTEXT,
                       'ADV_DATA': libPyApi.TXDT_ADV_DATA,
                       'ANY' : libPyApi.TXDT_ANY,
                       'FCOE_CTXT' : libPyApi.TXDT_FCOE_CTXT,
                       'FCOE_DDP_CTXT': libPyApi.TXDT_FCOE_DDP_CTXT,
                       'FILTER_PROG': libPyApi.TXDT_FILTER_PROG,
                       'FLEX_CTXT1': libPyApi.TXDT_FLEX_CTXT1,
                       'FLEX_CTXT2': libPyApi.TXDT_FLEX_CTXT2,
                       'FLEX_DATA': libPyApi.TXDT_FLEX_DATA,
                       'LEGACY': libPyApi.TXDT_LEGACY}

TX_WB_MODE = {'SV_DD_BIT_WB_MODE': libPyApi.SV_DD_BIT_WB_MODE,
              'SV_HEAD_WB_MODE' : libPyApi.SV_HEAD_WB_MODE,
              'SV_PUSH_MODE' : libPyApi.SV_PUSH_MODE,
              'SV_COMPLETION_QUEUE_MODE' : libPyApi.SV_COMPLETION_QUEUE_MODE}

TX_PACKET_LOAD_METHOD = {'AUTO_GENERATE_DESCRIPTORS': libPyApi.TPLM_AUTO_GENERATE_DESCRIPTORS,
                         'AUTO_GENERATE_DESCRIPTORS_REMOTELY': libPyApi.TPLM_AUTO_GENERATE_DESCRIPTORS_REMOTELY,
                         'AUTO_GENERATE_DESCRIPTORS_REMOTELY_FULL_RING' : libPyApi.TPLM_AUTO_GENERATE_DESCRIPTORS_REMOTELY_FULL_RING,
                         'AUTO_GENERATE_PACKETS_AND_DESCRIPTORS' : libPyApi.TPLM_AUTO_GENERATE_PACKETS_AND_DESCRIPTORS,
                         'AUTO_GENERATE_PACKETS_AND_DESCRIPTORS_WITH_PARAMS' : libPyApi.TPLM_AUTO_GENERATE_PACKETS_AND_DESCRIPTORS_WITH_PARAMS, 
                         'DESCRIPTORS_GENERATED_EXTERNALLY' : libPyApi.TPLM_DESCRIPTORS_GENERATED_EXTERNALLY,
                         'DESCRIPTORS_GENERATED_EXTERNALLY_REMOTELY' : libPyApi.TPLM_DESCRIPTORS_GENERATED_EXTERNALLY_REMOTELY }

QUEUE_OPERATION_MODE = {'SV': libPyApi.QOM_SV ,
                        'QAV': libPyApi.QOM_QAV,
                        'NET': libPyApi.QOM_NET,
                        'CC': libPyApi.QOM_CC,
                        'COMMS': libPyApi.QOM_COMMS,
                        'SPLITQ': libPyApi.QOM_SPLITQ,
                        'DEFAULT': libPyApi.QOM_DEFAULT} 

LINK_MODE = {'LM_10G_FULL' : libPyApi.LM_10G_FULL,
             'LML_5G_FULL' : libPyApi.LM_2_5G_FULL}

#TODO finish this enum

DEV_IDS = {'fvl' : ['1583','1581','1572','1586','1580'],
           'sgvl': ['1563'],
           'fortpond' : ['1589'],
           'crsvl' : ['1586','1572','15ff'],
           'elv' : ['1586','1572','15ff'],
           'tvl' : ['1528'],
           'cpk' : ['f0a5','1888','1889','1890','1891','1892','1893','1894','1895','1896','1897','1898','1899','189a','189b','189c','189d','189e','189f'],
           'cvl' : ['1590','1591','1592','1593','1594','1595','1598','1599','159a','159b'],
           'cvl_sd' : ['159a','159b','1599'],
           'fvl25' : ['158a','158b'],
           'lbg' : ['37d0'],
           'nnt' : ['10fb'],
           'mev' : ['f002']}

class DriverProxy(libPyApi.driver_proxy):

    def __init__(self, device, pf_num, nic_num=None, remote="", vf_num=libPyApi.INVALID_VF):
        """
        """
        if nic_num:
            super(DriverProxy, self).__init__(device, pf_num, nic_num, remote, vf_num)

        else:
            super(DriverProxy, self).__init__(device, pf_num, remote, vf_num)

class SvDriver(object):
    """This class performs all the interface with SV driver)"""

    def __init__(self, device_info):
        self._project_name = device_info.device_name
        self._device_number = device_info.device_number
        self._port_number = int(device_info.port_number)
        self._hostname = device_info.hostname
        self._driver_proxy = DriverProxy(self._project_name,int(self._port_number), int(self._device_number), self._hostname)
        

    @classmethod
    def create_driver_by_name(cls, device_name, device_number, port_number, hostname = ""):
        '''This method constructs an SvDriver object
            input params @device_name
                         @device_number
                         @port_number
                         @hostname
         '''
        device_info = DeviceInfo()
        device_info.device_name = device_name
        device_info.device_number = str(device_number)
        device_info.port_number = str(port_number)
        device_info.dev_id = get_device_id_by_name(device_name, device_number, port_number)
        device_info.dev_location = get_device_bdf_by_name(device_name,device_number, port_number)
        device_info.driver_specific_id = get_device_specific_id(device_name,device_number, port_number)
	device_info.hostname = hostname
        return cls(device_info)

    def port_number(self):
        '''
            This method return port number of current port.
        '''
        return self._port_number
    
    def device_number(self):
        '''
            This method return device number to which current port belongs.
        '''
        return self._device_number              

    def start_tx(self, **kwargs):                
        '''
            This method starts TX on ring 0. Parameters can be passed in **kwargs dictionary
            as key-value pairs. List of parameters and their default values
            if not passed in **kwargs:
                'packet_size' - default value 512            
                'packets_to_send' - passed value -1 means infinite. Default value infinite 


                @input as key = word arguments
                @number_of_packets
                @ring_id
                @ring_size
                @tx_packet_type
                @packet_size
                @desc_type
                @wb_mode
                @tx_packet_load_method
                @op_mode
                @num_of_desc_per_packet
                @rs_bit_frequency         
        '''
        #TODO use the dict.get method to filling in the values
        skip_ring_cfg = kwargs.get('skip_ring_cfg', False)
    
        ring_cfg = libPyApi.TxRingConfiguration()
        ring_cfg.packet_size = kwargs.get('packet_size', 512)
        ring_cfg.packet_type = kwargs.get('tx_packet_type', TX_PACKET_TYPES['L2_DRIVER_PACKET'])
        ring_cfg.descs_per_packet = kwargs.get('num_of_desc_per_packet',1)
        ring_cfg.ring_size = kwargs.get('ring_size', 1024)
        ring_cfg.wb_mode = kwargs.get('wb_mode', 0)
        ring_cfg.operation_mode = kwargs.get('operation_mode', 0)
        # ring_cfg.cq_id = kwargs('cq_id', 1)

        
        ring_id = kwargs.get('ring_id', 0)
        desc_type = kwargs.get('desc_type', TX_DESCRIPTOR_TYPES['ADV_DATA'])
        tx_packet_load_method = kwargs.get('tx_packet_load_method', TX_PACKET_LOAD_METHOD['AUTO_GENERATE_PACKETS_AND_DESCRIPTORS'])

        tx_limit_type = kwargs.get('tx_limit_type', 'INFINTE')

        time_limit = kwargs.get('time_limit', 5)
        number_of_packets = kwargs.get('number_of_packets', 1000000)


        rs_bit_frequency = 16
        descSize = 0
        step = 0

        tx_ring = self._driver_proxy.get_tx_ring(ring_id)

        if not tx_ring:
            raise RuntimeError(self._driver_proxy.driver_error_to_string(libPyApi.ERROR_RING_NOT_ALLOCATED))

        if not skip_ring_cfg:
            status = tx_ring.configure_tx_ring_with_properties(ring_cfg)

        if status != libPyApi.ERROR_STATUS_OK:
            raise RuntimeError(self._driver_proxy.driver_error_to_string(status))

        tx_options = libPyApi.TxOptions()

        
        if tx_limit_type == 'INFINTE':
            tx_options.tx_limit_type = libPyApi.TX_MODE_INFINITE
        elif tx_limit_type == 'TIME':
            tx_options.tx_limit_type = libPyApi.TX_MODE_TIME_LIMIT
        elif tx_limit_type == 'PACKET_COUNT':
            tx_options.tx_limit_type = libPyApi.TX_MODE_PACKET_COUNT_LIMIT
        else:
            tx_options.tx_limit_type = libPyApi.TX_MODE_FULL_RING


        status = tx_ring.start_tx(tx_options)

        if status != libPyApi.ERROR_STATUS_OK:
            raise RuntimeError(self._driver_proxy.driver_error_to_string(status))

        self._driver_proxy.dispose_tx_ring(tx_ring)

    def stop_tx(self, **kwargs):
        '''
            This method stops TX on ring 0.
        '''
        ring_id = kwargs.get('ring_id', 0)

        tx_ring = self._driver_proxy.get_tx_ring(ring_id)
        if not tx_ring:
            raise RuntimeError(self._driver_proxy.driver_error_to_string(libPyApi.ERROR_RING_NOT_ALLOCATED))

        status = tx_ring.stop_tx(5)

        if (status != libPyApi.ERROR_STATUS_OK):
            raise RuntimeError(self._driver_proxy.driver_error_to_string(status))
        self._driver_proxy.dispose_tx_ring(tx_ring)

    def start_rx(self, **kwargs):
        '''
        This method starts RX on ring 0.       
        '''    
        ringId = 0        
        rxringSize = 8160
        rxbuffSize = 2048
        rxhdrSize = 256        
        rxdescType = "ADV_ONE_BUFFER"                
        rxqueueOpMode = 0
        descsPerPacket = 1        
        descSize = 0 #0 - 16 byte descriptor, 1 - 32 byte descirptor

        if self._project_name == 'rrc':
            descSize = 1 # 32 byte

        status = libSvPython.set_rx_ring_c(self._device_string, ringId, rxringSize, rxbuffSize, rxdescType, descSize, rxhdrSize, rxqueueOpMode)
        if (status != libSvPython.ERROR_STATUS_OK):
            raise RuntimeError("Error configuring Rx ring on {}, driver returned {}".format(self._device_string, status))
       
        status = libSvPython.start_rx_infinite_c(self._device_string, ringId)
        if (status != libSvPython.ERROR_STATUS_OK):
            raise RuntimeError("Error starting Rx on {}, driver returned {}".format(self._device_string, status))

        status = libSvPython.enable_rx_promiscuous_filter(self._device_string)
        if (status != libSvPython.ERROR_STATUS_OK):
            raise RuntimeError("Error setting promiscuous filter on {}, driver returned {}".format(self._device_string, status))
                    
        pass

    def stop_rx(self):
        '''
        This method stops RX on ring 0.
        '''        
        ringId = 0
        status = libSvPython.stop_rx_c(self._device_string, ringId)
        if (status != libSvPython.ERROR_STATUS_OK):
            raise RuntimeError("Error stopping Rx on {}, driver returned {}".format(self._device_string, status))
        pass
           
    def configure_tx_ring(self, ring, **kwargs):
        pass

    def configure_rx_ring(self, ring, **kwargs):
        pass

    def read_pci(self, register_offset):
        ''' 
        This method reads 32-bits pci register at offset specified 
        in 'register_offset' and returns register value.            
        '''
        pci_block = self._driver_proxy.create_pci_block()
        value = pci_block.read_word(register_offset)
        self._driver_proxy.dispose_pci_block(pci_block)
        return  value

    def write_pci(self, register_offset, write_value):
        '''
        This method writes value specified in 'write_value' 
        to 32-bits pci register at offset specified in 'register_offset'.
        ''' 
        pci_block = self._driver_proxy.create_pci_block()
        status = pci_block.write_word(register_offset, write_value)
        self._driver_proxy.dispose_pci_block(pci_block)
        if status[0]:
            raise RuntimeError("writing to {} failed".format(register_offset))

    def read_csr(self, register_offset):
        ''' 
            This method reads 32-bits csr register at offset specified 
            in 'register_offset' and returns register value.            
        '''
        csr_block = self._driver_proxy.csr(IP_TYPE['DEFAULT'])
        value = csr_block.read_64(register_offset)[1]
        self._driver_proxy.dispose_csr_block(csr_block)
        return value

    def write_csr(self, register_offset, write_value):
        '''
            This method writes value specified in 'write_value' 
            to 32-bits csr register at offset specified in 'register_offset'.
        '''  
        csr_block = self._driver_proxy.csr(IP_TYPE['DEFAULT'])
        csr_block.write(register_offset, write_value)
        self._driver_proxy.dispose_csr_block(csr_block)

 
    def send_aq_command(self, aq_descriptor, aq_buffer = None, debug_print = False):
        '''This function sends AQ command.
            Arguments:
                aq_descriptor - aq command data descriptor with following fields
                    opcode, flags, param0, param1, cookie_high, cookie_low, address_high, address_low, retval, datalen.
                    If one of these fields not set default value is 0.
                aq_buffer - optional buffer for AQ. Refer to EAS for specific command, each value represents byte.
                             If no buffer required pass None, default value is None.
				debug_print - print AQ descriptor or not
                Responsse from FW will be returned in these arguments.
            Returns:
                0 if aq command sent successfully, else error code   
        '''
        aq = self._driver_proxy.create_admin_queue()
        desc = libPyAdminqApi.ControlQueueDescriptor()
        desc.opcode = aq_descriptor.opcode
        desc.flags  = aq_descriptor.flags
        desc.param0 = aq_descriptor.param0
        desc.param1 = aq_descriptor.param1
        desc.cookie_low = aq_descriptor.cookie_low
        desc.cookie_high = aq_descriptor.cookie_high
        desc.addr_high = aq_descriptor.addr_high
        desc.addr_low = aq_descriptor.addr_low
        desc.retval = aq_descriptor.retval
        desc.datalen = aq_descriptor.datalen

        aq_buffer_out = libSvPython.ByteArray(aq_descriptor.datalen)
        if aq_buffer is not None:
            for i in range(aq_descriptor.datalen):
                aq_buffer_out[i] = aq_buffer[i]
        buffer_size = aq_descriptor.datalen

        # send command, response will update the desc fields and aq_buffer
        status = aq.admin_queue_send_command(desc, aq_buffer_out, buffer_size, True)
        print(status)

        if debug_print:
            print "admin queue desciptor:\n"
            # print admin queue desciptor
            print("flags: %s" % (hex(desc.flags)))
            print("opcode: %s" % (hex(desc.opcode)))
            print("param0: %s" % (hex(desc.param0)))
            print("param1: %s" % (hex(desc.param1)))
            print("retval: %s" % (desc.retval))
            print("datalen: %s" % (desc.datalen))
            print("cookie_low: %s" % (hex(desc.cookie_low)))
            print("cookie_high: %s" % (hex(desc.cookie_high)))
            print("addr_low: %s" % (hex(desc.addr_low)))
            print("addr_high: %s" % (hex(desc.addr_high)))

            print

            if desc.datalen:
                print "admin queue buffer: \n"
                # print admin queue buffer
                for i in range(desc.datalen):
                    if i > 0 and i % 16 == 0:
                        sys.stdout.write("\n")
                    sys.stdout.write(hex(aq_buffer_out[i]) + " ")

                print
        aq_descriptor.flags = desc.flags
        aq_descriptor.opcode = desc.opcode
        aq_descriptor.param0 = desc.param0
        aq_descriptor.param1 = desc.param1
        aq_descriptor.retval = desc.retval
        aq_descriptor.datalen = desc.datalen
        aq_descriptor.cookie_low = desc.cookie_low
        aq_descriptor.addr_low = desc.addr_low
        aq_descriptor.addr_high = desc.addr_high
        if aq_buffer is not None:
            for i in range(aq_descriptor.datalen):
                aq_buffer[i] = aq_buffer_out[i]
        self._driver_proxy.dispose_admin_queue(aq)
        return status[0]

    def device_reset(self, reset_type):
        ''' This function resets device.
            Arguments:
                reset_type - type of reset to perform. Options:
                'PF', 'CORE', 'GLOBAL', 'EMP', 'VF_SW', 'VFLR', 'FL'
                'PCI', 'PCE_RESTORE', 'BME', 'ACPI'

        '''
        if reset_type == 'PF':
            reset_type_value = libPyApi.DRT_PF_RESET
        elif reset_type == 'CORE':
            reset_type_value = libPyApi.DRT_CORE_RESET
        elif reset_type == 'GLOBAL':
            reset_type_value = libPyApi.DRT_GLOBAL_RESET
        elif reset_type == 'EMP':
            reset_type_value = libPyApi.DRT_EMP_RESET
        elif reset_type == 'VF_SW':
            reset_type_value = libPyApi.DRT_VF_SW_RESET
        elif reset_type == 'VFLR':
            reset_type_value = libPyApi.DRT_VFLR_RESET
        elif reset_type == 'FL':
            reset_type_value = libPyApi.DRT_FL_RESET
        elif reset_type == 'PCI':
            reset_type_value = libPyApi.DRT_PCI_RESET
        elif reset_type == 'PCI_RESTORE':
            reset_type_value = libPyApi.DRT_PCI_RESET_RESTORE
        elif reset_type == 'BME':
            reset_type_value = libPyApi.DRT_BME_RESET
        elif reset_type == 'ACPI':
            reset_type_value = libPyApi.DRT_ACPI_RESET
        elif reset_type == 'None':
            reset_type_value = libPyApi.DRT_NONE
        elif reset_type == 'MEV_IMC':
            reset_type_value = libPyApi.DRT_MEV_IMC_RESET
        elif reset_type == 'MEV_LINK':
            reset_type_value = libPyApi.DRT_MEV_IMC_RESET
        else:
            raise RuntimeError("Unsupported reset type " + reset_type)
        dcfg = self._driver_proxy.cfg()
        result = dcfg.reset_device()
        self._driver_proxy.dispose_driver_config(dcfg)
        if result != libPyApi.ERROR_STATUS_OK:
            raise RuntimeError(self._driver_proxy.driver_error_to_string(result))

    def __del__(self):
        pass

if __name__=="__main__":
    try:
        import readline
    except ImportError:
        print("Module readline not available.")
    else:
        import rlcompleter
        readline.parse_and_bind("tab: complete")
    cvl = SvDriver.create_driver_by_name('cvl', str(0), str(0), 'ladh444')

