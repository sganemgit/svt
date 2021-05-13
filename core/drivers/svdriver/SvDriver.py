
# @author Shady Ganem <shady.ganem@intel.com>

import libSvPython
import libPyApi
import libPyAdminqApi

import sys
import time
from core.drivers.svdriver.SvDriverBase import SvDriverBase
#from core.structs.AqDescriptor import AqDescriptor
#from core.drivers.svdriver.SvDriverCommands import *

MDIO_REGS = {'fvl'    : (0x8818C,0x8819C), 
             'fpk'    : (0x8818C,0x8819C), 
             'sgvl'   : (0x425C,0x4260),
             'fortpond' : (0x8818C,0x8819C), 
             'crsvl' : (0x8818C,0x8819C), 
             'elv' : (0x8818C,0x8819C), 
             'tvl' : (0x425C,0x4260),
             'cpk' : (0x0000,0x0000),
             'cvl' : (0x0000,0x0000),
             'cvl_sd' : (0x0000,0x0000),
             'fvl25' : (0x8818C,0x8819C),
             'nnt' : (0x425C,0x4260),
             'lbg' : (0x8818C,0x8819C),                 
	     'mev' : (0x0000,0x0000)}

############################################################################################
# driver api values

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

RX_DESCRIPTOR_TYPES ={"LEGACY": libPyApi.RXDT_LEGACY,
                      "ONE_BUFFER": libPyApi.RXDT_ADV_ONE_BUFFER,
                      "HDR_SPLIT": libPyApi.RXDT_ADV_HDR_SPLIT,
                      "HDR_REPLIC": libPyApi.RXDT_ADV_HDR_REPLIC,
                      "HDR_REPLIC_LONG": libPyApi.RXDT_ADV_HDR_REPLIC_LONG,
                      "HDR_SPLIT_ALWAYS_USE_HEADER_BUFF": libPyApi.RXDT_ADV_HDR_SPLIT_ALWAYS_USE_HEADER_BUFF,
                      "HDR_SPLIT_SMALL_LARGE": libPyApi.RXDT_ADV_HDR_SPLIT_SMALL_LARGE,
                      "FLEX": libPyApi.RXDT_FLEX}

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

MALICIOUS_MODE = {"NONE": libPyApi.MALICIOUS_NONE,
                  "NO_EOP": libPyApi.MALICIOUS_NO_EOP,
                  "TXADDR": libPyApi.MALICIOUS_TXADDR,
                  "TXLEN": libPyApi.MALICIOUS_TXLEN}

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

DESC_SIZE = {16: libPyApi.RXDS_16_BYTES,
             32: libPyApi.RXDS_32_BYTES}

class SvDriver(SvDriverBase):
    """
        This class performs all the interfacing with SV driver
    """

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

    def __init__(self, device_info):
        self._project_name = device_info.device_name
        self._device_number = int(device_info.device_number)
        self._port_number = int(device_info.port_number)
        self._hostname = device_info.hostname
        self._ip_type = self.IP_TYPE["DEFAULT"]
        self._driver_proxy = libPyApi.driver_proxy(self._project_name,int(self._port_number), int(self._device_number), self._hostname)
    
    def set_ip_type(self, ip_type="DEFAULT"):
        self._ip_type = ip_type
        
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
            This method starts TX on ring a given ring. Parameters can be passed in **kwargs dictionary
            as key-value pairs. List of parameters and their default values
                @skip_ring_cfg
                @number_of_packets
                @ring_id
                @ring_size
                @tx_packet_type
                @packet_size
                @desc_type
                @wb_mode
                @tx_packet_load_method
                @num_of_desc_per_packet
                @rs_bit_frequency   
                @operation_mode  
                @cq_id
                @time_limit
                @tx_limit_type - options: FULL_RING, PACKET_COUNT, TIME, INFINTE
                @dest_mac_enable - curntly not supported
                @src_mac_enable - curently not supported
                @vlan_tag_enable - not supported
        '''
        skip_ring_cfg = kwargs.get('skip_ring_cfg', False)
        ring_id = kwargs.get('ring_id', 0)
        desc_type = kwargs.get('desc_type', TX_DESCRIPTOR_TYPES['ADV_DATA'])
        tx_packet_load_method = kwargs.get('tx_packet_load_method', TX_PACKET_LOAD_METHOD['AUTO_GENERATE_PACKETS_AND_DESCRIPTORS'])
        tx_limit_type = kwargs.get('tx_limit_type', 'INFINTE')
        time_limit = kwargs.get('time_limit', 5)
        number_of_packets = kwargs.get('number_of_packets', 1000000)
        rs_bit_frequency = kwargs.get('rs_bit_frequency', 16)

        ring_cfg = libPyApi.TxRingConfiguration()
        ring_cfg.packet_size = kwargs.get('packet_size', 512)
        ring_cfg.packet_type = kwargs.get('tx_packet_type', TX_PACKET_TYPES['L2_DRIVER_PACKET'])
        ring_cfg.descs_per_packet = kwargs.get('num_of_desc_per_packet',1)
        ring_cfg.ring_size = kwargs.get('ring_size', 1024)
        ring_cfg.wb_mode = kwargs.get('wb_mode', 0)
        ring_cfg.operation_mode = kwargs.get('operation_mode', 0)
        ring_cfg.cq_id = kwargs.get('cq_id', 1)

        ring_cfg.dest_mac_enable = kwargs.get('dest_mac_enable', 0)
        if ring_cfg.dest_mac_enable:
            ring_cfg.dest_mac = kwargs.get('dest_mac', ring_cfg.dest_mac)

        ring_cfg.src_mac_enable = kwargs.get('src_mac_enable', 0)
        if ring_cfg.src_mac_enable:
            ring_cfg.src_mac = kwargs.get('src_mac', ring_cfg.src_mac)

        ring_cfg.vlan_tag_enable = kwargs.get('vlan_tag_enable', 0)
        if ring_cfg.vlan_tag_enable:
            ring_cfg.vlan_tag = kwargs.get('vlan_tag',ring_cfg.vlan_tag)

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
            tx_options.limit_value = number_of_packets
        elif tx_limit_type == 'FULL_RING':
            tx_options.tx_limit_type = libPyApi.TX_MODE_FULL_RING
        else:
            print("Warning: invalid limit using FULL_RING")
            tx_options.tx_limit_type = libPyApi.TX_MODE_FULL_RING

        try:
            status = tx_ring.start_tx(tx_options)
        except Exception as e:
            raise e

        if status != libPyApi.ERROR_STATUS_OK:
            raise RuntimeError(self._driver_proxy.driver_error_to_string(status))

        self._driver_proxy.dispose_tx_ring(tx_ring)

    def get_ring_status(self, ring_id):
        try:
            ring_status = libPyApi.TxRingStatus()
            tx_ring = self._driver_proxy.get_tx_ring(ring_id)
            status = tx_ring.get_status(ring_status)
            self._driver_proxy.dispose_tx_ring(tx_ring)
            if status:
                raise RuntimeError(self._driver_proxy.driver_error_to_string(status))
            return ring_status.State
        except Exception as e:
            raise e

    def is_ring_done(self, ring_id):
        try:
            if self.get_ring_status(ring_id) == libPyApi.RING_STATE_WORKING:
                return False
            else:
                return True
        except Exception as e:
            raise e

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
            This method starts TX on ring a given ring. Parameters can be passed in **kwargs dictionary
            as key-value pairs. List of parameters and their default values
                @buffer_size
                @ring_id
                @ring_size
                @packet_size
                @desc_type
                @op_mode
                @num_of_desc_per_packet   
                @operation_mode  
        '''
        ring_id = kwargs.get('ring_id', 0)

        ring_cfg = libPyApi.RxRingProperties()
        ring_cfg.desc_count = kwargs.get('desc_count', 128)
        ring_cfg.desc_type = kwargs.get('desc_type', RX_DESCRIPTOR_TYPES['ONE_BUFFER'])
        ring_cfg.desc_size = kwargs.get('desc_size', DESC_SIZE[32])
        ring_cfg.buffer_size = kwargs.get('buffer_size', 2048)
        ring_cfg.hdr_size = kwargs.get('hdr_size', 128)
        ring_cfg.operation_mode = kwargs.get('operation_mode', QUEUE_OPERATION_MODE['DEFAULT'])
        ring_cfg.srrctl_index = int("0xFFFF", 16)
        ring_cfg.malicious_mode = kwargs.get('malicious_mode',MALICIOUS_MODE['NONE'])
        ring_cfg.mirroring_replication = False

        rx_ring = self._driver_proxy.get_rx_ring(ring_id)

        if not rx_ring:
            raise RuntimeError(self._driver_proxy.driver_error_to_string(libPyApi.ERROR_RING_NOT_ALLOCATED))

        status = rx_ring.configure_rx_ring(ring_cfg)

        if status != libPyApi.ERROR_STATUS_OK:
            raise RuntimeError(self._driver_proxy.driver_error_to_string(status))

        status = rx_ring.start_rx()

        if status != libPyApi.ERROR_STATUS_OK:
            raise RuntimeError(self._driver_proxy.driver_error_to_string(status))

        self._driver_proxy.dispose_rx_ring(rx_ring)

    def stop_rx(self, **kwargs):
        '''
        This method stops RX on ring 0.
        '''        
        ring_id = kwargs.get('ring_id', 0)
        rx_ring = self._driver_proxy.get_rx_ring(ring_id)
        if not rx_ring:
            raise RuntimeError(self._driver_proxy.driver_error_to_string(libPyApi.ERROR_RING_NOT_ALLOCATED))

        status = rx_ring.stop_rx()

        if (status != libPyApi.ERROR_STATUS_OK):
            raise RuntimeError(self._driver_proxy.driver_error_to_string(status))
        self._driver_proxy.dispose_rx_ring(rx_ring)
           
    def get_rx_descriptors(self, ring_number):
        '''
            create a list of all the ring descriptors

                :param device: device identity
                :param ring_number: ring number
                :return: list of descriptors
        ''' 
        dp = self._driver_proxy

        rx_ring = dp.get_rx_ring(ring_number)

        if rx_ring is None:
            raise RuntimeError("Getting Rx ring failed, ring number = %s" % ring_number)

        ring_props = libPyApi.RxRingProperties()

        rx_ring.get_ring_properties(ring_props)

        if ring_props is None:
            raise RuntimeError("Getting ring properties failed, ring number = %s" % ring_number)

        ring_size = ring_props.desc_count

        data = list() 
        buff = libPyApi.vector_descriptor()
        rx_ring.get_ring_descriptors(buff)

        for idx in range(0, ring_size):
            offset = rx_ring.get_descriptor_offset(idx)
            # offset = [0,0]
            # desc_type = DESC_TYPE[rx_ring.get_ring_descriptor_type(idx)[1]]
            address = buff[idx].address
            fields = buff[idx].fields
            row = ["{0:0>12}".format(idx),
                    hex(offset[1]),
                    hex(address),
                    "{0:0>12}".format(hex(fields))]

            data.append(row)
        return data

    def configure_tx_ring(self, **kwargs):
        pass

    def configure_rx_ring(self, **kwargs):
        pass

    def tx_start_traffic(self, **kwargs):
        pass

    def rx_start_traffic(self, **kwargs):
        pass

    def get_fw_info(self):
        '''
            This method retuns a dictionary conatining FW info
        '''
        fw_info_dict = dict()
        fw_info = libPyApi.SvFirmwareVersion()
        self._driver_proxy.cfg().get_firmware_version(fw_info)
        fw_info_dict['FW build'] = hex(fw_info.fw_build)
        fw_info_dict['FW Api version'] = "{}.{}".format(fw_info.api_major_version, fw_info.api_minor_version)
        fw_info_dict['FW version'] = "{}.{}".format(fw_info.fw_major_version, fw_info.fw_minor_version)
        fw_info_dict['FW rom version'] = hex(fw_info.rom_version)
        fw_info_dict['FW patch version'] = str(fw_info.fw_patch_version)
        return fw_info_dict

    def get_kernel_module_name(self):
        '''
            This method returns the kernel device driver's module name in the kernel
        '''
        return self._driver_proxy.get_module_name()

    def read_shadow_ram(self, word_offset):
        '''
            This methods reads from the Internal shadow RAM
        '''
        nvm_block = self._driver_proxy.nvm()
        value = nvm_block.shadow_ram_read(word_offset)
        if value[0]:
            raise RuntimeError("shadow ram read failed status {}".format(value[0]))
        return value[1]

    def dump_show_ram_to_file(self, filename):
        '''
            This method dumps shadow ram values to a file
        '''
        nvm_block = self._driver_proxy.nvm()
        value = nvm_block.dump_shadow_ram_to_file(filename)
        if value:
            raise RuntimeError("shadow ram read failed status {}".format(value[0]))

    def read_nvm(self, word_offset):
        '''
            this method reads from the device's nvm
        '''
        nvm_block = self._driver_proxy.nvm()
        value = nvm_block.read(word_offset)
        if value[0]:
            raise RuntimeError("nvm read failed status {}".format(value[0]))
        return value[1]

    def read_nvm_memory_mapped(self, word_offset):
        '''
            this method reads from the device's nvm
        '''
        nvm_block = self._driver_proxy.nvm()
        value = nvm_block.memory_mapped_read(word_offset)
        if value[0]:
            raise RuntimeError("nvm read failed status {}".format(value[0]))
        return value[1]        

    def write_nvm(slef, word_offset, value_16bit):
        '''
            this method reads from the device's nvm
        '''
        nvm_block = self._driver_proxy.nvm()
        nvm_block.write(word_offset, value_16bit)

    def get_nvm_version(self):
        '''
            This method returns the currnet device nvm version as a string 
        '''
        version = libPyApi.SvNvmVersion()
        self._driver_proxy.nvm().get_nvm_version(version)    
        return "{}.{}".format(version.major,version.minor)

    def get_nvm_id(self):
        '''
            This method returns the currnet device nvm id
        '''
        version = libPyApi.SvNvmVersion()
        self._driver_proxy.nvm().get_nvm_version(version)    
        return hex(version.id)

    def get_flash_size(self):
        '''
            This method returns the flash size as an int
        '''
        return self._driver_proxy.nvm().get_flash_size()[1]

    def get_shadow_ram_size(self):
        '''
            This method returns the shadow ram size as an int
        '''
        return self._driver_proxy.nvm().get_shadow_ram_size()[1]

    def get_eeprom_size(self):
        '''
            This method returns the shadow ram size as an int
        '''
        return self._driver_proxy.nvm().get_eepromsize()[1]

    def read_pci(self, register_offset):
        ''' 
        This method reads 32-bits pci register at offset specified 
        in 'register_offset' and returns register value.            
        '''
        pci_block = self._driver_proxy.create_pci_block()
        value = pci_block.read_word(register_offset)
        self._driver_proxy.dispose_pci_block(pci_block)
        return  value[1]

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
        csr_block = self._driver_proxy.csr(self.IP_TYPE['DEFAULT'])
        value = csr_block.read(register_offset)[1]
        self._driver_proxy.dispose_csr_block(csr_block)
        return value

    def read_csr_64(self, register_offset):
        ''' 
            This method reads 64-bits csr register at offset specified 
            in 'register_offset' and returns register value.          
        '''
        csr_block = self._driver_proxy.csr(self.IP_TYPE['DEFAULT'])
        value = csr_block.read_64(register_offset)[1]
        self._driver_proxy.dispose_csr_block(csr_block)
        return value

    def write_csr(self, register_offset, write_value):
        '''
            This method writes value specified in 'write_value' 
            to 32-bits csr register at offset specified in 'register_offset'.
        '''  
        csr_block = self._driver_proxy.csr(self.IP_TYPE['DEFAULT'])
        csr_block.write(register_offset, write_value)
        self._driver_proxy.dispose_csr_block(csr_block)

    def write_csr_64(self, register_offset, write_value):
        '''
            This method writes value specified in 'write_value' 
            to 64-bits csr register at offset specified in 'register_offset'.
        '''  
        csr_block = self._driver_proxy.csr(self.IP_TYPE['DEFAULT'])
        csr_block.write_64(register_offset, write_value)
        self._driver_proxy.dispose_csr_block(csr_block)
 
    def send_aq_command(self, aq_descriptor, aq_buffer = None, debug_print = False, auto_fill=False):
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
        if debug_print:
          print("admin queue desciptor command:\n")
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

          print()

          if desc.datalen:
            print("admin queue buffer: \n")
            # print admin queue buffer
            for i in range(desc.datalen):
                if i > 0 and i % 16 == 0:
                    sys.stdout.write("\n")
                sys.stdout.write(hex(aq_buffer_out[i]) + " ")
            print()

        # send command, response will update the desc fields and aq_buffer
        status = aq.admin_queue_send_command(desc, aq_buffer_out, buffer_size, auto_fill)

        if debug_print:
            print("admin queue desciptor response:\n")
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

            print()

            if desc.datalen:
                print("admin queue buffer: \n")
                # print admin queue buffer
                for i in range(desc.datalen):
                    if i > 0 and i % 16 == 0:
                        sys.stdout.write("\n")
                    sys.stdout.write(hex(aq_buffer_out[i]) + " ")
                print()

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
        reset_values = {'PF': libPyApi.DRT_PF_RESET,
                        'CORE': libPyApi.DRT_CORE_RESET,
                        'GLOBAL': libPyApi.DRT_GLOBAL_RESET,
                        'EMP': libPyApi.DRT_EMP_RESET,
                        'VF_LR': libPyApi.DRT_VFLR_RESET,
                        'VF_SW': libPyApi.DRT_VF_SW_RESET,
                        'FL': libPyApi.DRT_FL_RESET,
                        'PCI': libPyApi.DRT_PF_RESET,
                        'PCI_RESTORE': libPyApi.DRT_PCI_RESET_RESTORE,
                        'BME': libPyApi.DRT_BME_RESET,
                        'ACPI': libPyApi.DRT_ACPI_RESET,
                        'MEV_IMC': libPyApi.DRT_MEV_IMC_RESET,
                        'MEV_LINK': libPyApi.DRT_MEV_IMC_RESET,
                         None: libPyApi.DRT_NONE}
        driver_cfg = self._driver_proxy.cfg()
        result = driver_cfg.reset_device(reset_values[reset_type])
        self._driver_proxy.dispose_driver_config(driver_cfg)
        if result != libPyApi.ERROR_STATUS_OK:
            raise RuntimeError(self._driver_proxy.driver_error_to_string(result))

    def read_phy_register(self, devadd, mdiadd, phyadd):
        ''' 
        	This method reads phy register according to
        	'devadd', 'mdiadd' and 'phyadd' and returns register value.            
        '''
        mdio_cntrl, mdio_data = MDIO_REGS[self._project_name]
        value = 0        
        value = value | ((phyadd & 0x1f) << 21) # set phy address
        value = value | ((devadd & 0x1F) << 16) # set phy devadd
        value = value | (mdiadd & 0xFFFF) # set phy devadd
        #the opcode for reading is 0b10 [26:27]  or 0b11 [26:27]
        value = value | 0x40000000 # set mdio cmd        

        self.write_csr(mdio_cntrl, value)
        while self.read_csr(mdio_cntrl) & 0x40000000:
            time.sleep(0.01)
               
        # read cycle        
        value = value | (0x3 << 26)     # set opcode to read operation
        value = value | 0x40000000         # set mdio cmd

        self.write_csr(mdio_cntrl, value)

        while (self.read_csr(mdio_cntrl) & 0x40000000):
            pass    

        value = self.read_csr(mdio_data)
        value = (value & 0xffff0000) >> 16
        return value  							      

    def write_phy_register(self, page, register_offset, phy_add, write_value):
        '''
        	This method writes value specified in 'write_value' 
        	to phy register according to 'page', 'register_offset' and 'phy_add'.
        '''           
        mdio_cntrl, mdio_data = MDIO_REGS[self._project_name]
        value = 0        
        value = value | ((phy_add & 0x1f) << 21) # set phy address
        value = value | ((page & 0x1F) << 16) # set phy page
        value = value | (register_offset & 0xFFFF) # set phy page
        value = value | 0x40000000 # set mdio cmd    


        self.write_csr(mdio_cntrl, value)
        while (self.read_csr(mdio_cntrl) & 0x40000000):
            pass
        # write data register
        self.write_csr(mdio_cntrl, (write_value & 0xFFFF))

        # write cycle        
        value = value | (0x1 << 26)     # set opcode to read operation
        value = value | 0x40000000         # set mdio cmd

        self.write_csr(mdio_cntrl, value)

        while (self.read_csr(mdio_cntrl) & 0x40000000):
            pass    

        #print 'finished writing mdio thread ' + key
        pass

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

