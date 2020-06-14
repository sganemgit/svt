import libSvPython
import struct
from ctypes import *
import threading
#from ipacore.drivers.aq_descriptor import AqDescriptor
#from ipacore.drivers.projectsspecificdata import ProjectsSpecificData

class SvDriver(object):
    """This class wrapps 'libSvPython' module (python wrapper for SV driver)"""

    def __init__(self, device_info):                
        self._port_number = int(device_info.port_number)
        self._project_name = device_info.project_name      
        self._device_number = device_info.device_number
        self._device_string = device_info.driver_specific_id
        self._dev_id = device_info.dev_id
        self._bdf_location = device_info.location 

        self._mdio_lock = None

        self._mdio_cntrl, self._mdio_data = ProjectsSpecificData.get_mdios_regs(self._project_name)
        if self._mdio_cntrl is None:
            raise ValueError('Missing data for MDIO registers for project ' + self._project_name)

        #create adapter handle
        self._create()    

    def __del__(self):
        self._release()

    def set_additional_fields(self, **kwargs):
        self._mdio_lock = kwargs['mdio_locker']

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
               
    def get_device_info(self):
        return {'dev_id':self._dev_id, 'device_number':self._device_number, 'port_number':self._port_number,'bdf_location':self._bdf_location.get_location_string(),'b':self._bdf_location.a,'d':self._bdf_location.b,'f':self._bdf_location.c}

    def start_tx(self, **kwargs):                
        '''
        This method starts TX on ring 0. Parameters can be passed in **kwargs dictionary
        as key-value pairs. List of parameters and their default values
        if not passed in **kwargs:
            'packet_size' - default value 512            
            'packets_to_send' - passed value -1 means infinite. Default value infinite            
        '''

        packet_size = 512        
        packets_to_send = -1        

        if 'packet_size' in kwargs:
            packet_size = int(kwargs['packet_size'])                    
        if 'packets_to_send' in kwargs:
            packets_to_send = int(kwargs['packets_to_send'])              

        ringId = 0
        txringSize = 8160                
        txdescType = 1        
        wbmode = 0
        txqueueOpMode = 0        
        descsPerPacket = 1
        RsBitFrequency = 16
        descSize = 0 #0 - 16 byte descriptor, 1 - 32 byte descirptor

        if self._project_name == 'rrc':
            descSize = 1 # 32 byte

        status = libSvPython.set_tx_ring_c(self._device_string, ringId, txringSize, packet_size, txdescType, wbmode, txqueueOpMode, descsPerPacket, RsBitFrequency)
        if (status != libSvPython.ERROR_STATUS_OK):
            raise RuntimeError("Error configuring Tx ring on {}, driver returned {}".format(self._device_string, status))

        if packets_to_send == -1: 
            status = libSvPython.start_tx_time_c(self._device_string, ringId, 604800000) # 1 week of traffic
        else:
            status = libSvPython.start_tx_c(self._device_string, ringId, packets_to_send)

        if (status != libSvPython.ERROR_STATUS_OK):
            raise RuntimeError("Error starting Tx on {}, driver returned {}".format(self._device_string, status))


        pass

    def stop_tx(self):
        '''
        This method stops TX on ring 0.
        '''
        ringId = 0
        status = libSvPython.stop_tx_c(self._device_string, ringId)
        if (status != libSvPython.ERROR_STATUS_OK):
            raise RuntimeError("Error stopping Tx on {}, driver returned {}".format(self._device_string, status))

        pass

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
           
    def read_pci(self, register_offset):
        ''' 
        This method reads 32-bits pci register at offset specified 
        in 'register_offset' and returns register value.            
        '''
        value = libSvPython.read_pci_c(self._device_string, register_offset)
        return value      

    def write_pci(self, register_offset, write_value):
        '''
        This method writes value specified in 'write_value' 
        to 32-bits pci register at offset specified in 'register_offset'.
        '''  
        libSvPython.write_pci_c(self._device_string, register_offset, write_value)
        pass

    def read_csr(self, register_offset):
        ''' 
        This method reads 32-bits csr register at offset specified 
        in 'register_offset' and returns register value.            
        '''
        return self._read_csr(register_offset)     

    def write_csr(self, register_offset, write_value):
        '''
        This method writes value specified in 'write_value' 
        to 32-bits csr register at offset specified in 'register_offset'.
        '''  
        libSvPython.write_csr_c(self._device_string, register_offset, write_value)
        pass

    def read_phy_register(self, page, register_offset, phy_add):
        ''' 
        This method reads phy register according to
        'page', 'register_offset' and 'phy_add' and returns register value.            
        '''
        with self._mdio_lock:
            #key = threading.current_thread().getName()
            #print 'read mdio thread ' + key
            value = 0        
            value = value | ((phy_add & 0x1f) << 21) # set phy address
            value = value | ((page & 0x1F) << 16) # set phy page
            value = value | (register_offset & 0xFFFF) # set phy page
            value = value | 0x40000000 # set mdio cmd        
    
            libSvPython.write_csr_c(self._device_string, self._mdio_cntrl, value)
            while (self._read_csr(self._mdio_cntrl) & 0x40000000):
                pass
    
            # read cycle        
            value = value | (0x3 << 26)     # set opcode to read operation
            value = value | 0x40000000         # set mdio cmd
    
            libSvPython.write_csr_c(self._device_string, self._mdio_cntrl, value)
    
            while (self._read_csr(self._mdio_cntrl) & 0x40000000):
                pass    
    
            value = self._read_csr(self._mdio_data)
            value = (value & 0xffff0000) >> 16
            #print 'finished reading medio thread ' + key
            return value        

    def write_phy_register(self, page, register_offset, phy_add, write_value):
        '''
        This method writes value specified in 'write_value' 
        to phy register according to 'page', 'register_offset' and 'phy_add'.
        '''           
        with self._mdio_lock:
            #key = threading.current_thread().getName()
            #print 'writing mdio thread ' + key
   
            # address cycle        
        
            value = 0        
            value = value | ((phy_add & 0x1f) << 21) # set phy address
            value = value | ((page & 0x1F) << 16) # set phy page
            value = value | (register_offset & 0xFFFF) # set phy page
            value = value | 0x40000000 # set mdio cmd    
    
    
            libSvPython.write_csr_c(self._device_string, self._mdio_cntrl, value)
            while (self._read_csr(self._mdio_cntrl) & 0x40000000):
                pass
            # write data register
            libSvPython.write_csr_c(self._device_string, self._mdio_data, (write_value & 0xFFFF))
    
            # write cycle        
            value = value | (0x1 << 26)     # set opcode to read operation
            value = value | 0x40000000         # set mdio cmd
    
            libSvPython.write_csr_c(self._device_string, self._mdio_cntrl, value)
    
            while (self._read_csr(self._mdio_cntrl) & 0x40000000):
                pass    
    
            #print 'finished writing mdio thread ' + key
            pass
    
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
        desc_size = libSvPython.get_aq_descriptor_size()
        descriptor = libSvPython.ByteArray(desc_size)
                
        aq_buffer_size = 0
        sent_aq_buffer = None
        if aq_buffer is not None:                       
            aq_buffer_size = len(aq_buffer)
            sent_aq_buffer = libSvPython.ByteArray(aq_buffer_size)
            j = 0          
            while j < aq_buffer_size:
                sent_aq_buffer[j] = aq_buffer[j]                
                j += 1
       
        descriptor[0] = aq_descriptor.flags & 0xff
        descriptor[1] = (aq_descriptor.flags >> 8) & 0xff
        descriptor[2] = aq_descriptor.opcode & 0xff
        descriptor[3] = (aq_descriptor.opcode >> 8) & 0xff
        descriptor[4] = aq_descriptor.datalen & 0xff
        descriptor[5] = (aq_descriptor.datalen >> 8) & 0xff
        descriptor[6] = aq_descriptor.retval & 0xff
        descriptor[7] = (aq_descriptor.retval >> 8) & 0xff
        descriptor[8] = aq_descriptor.cookie_high & 0xff
        descriptor[9] = (aq_descriptor.cookie_high >> 8) & 0xff
        descriptor[10] = (aq_descriptor.cookie_high >> 16) & 0xff
        descriptor[11] = (aq_descriptor.cookie_high >> 24) & 0xff
        descriptor[12] = aq_descriptor.cookie_low & 0xff
        descriptor[13] = (aq_descriptor.cookie_low >> 8) & 0xff
        descriptor[14] = (aq_descriptor.cookie_low >> 16) & 0xff
        descriptor[15] = (aq_descriptor.cookie_low >> 24) & 0xff
        descriptor[16] = aq_descriptor.param0 & 0xff
        descriptor[17] = (aq_descriptor.param0 >> 8) & 0xff
        descriptor[18] = (aq_descriptor.param0 >> 16) & 0xff
        descriptor[19] = (aq_descriptor.param0 >> 24) & 0xff
        descriptor[20] = aq_descriptor.param1 & 0xff
        descriptor[21] = (aq_descriptor.param1 >> 8) & 0xff
        descriptor[22] = (aq_descriptor.param1 >> 16) & 0xff
        descriptor[23] = (aq_descriptor.param1 >> 24) & 0xff
        descriptor[24] = aq_descriptor.addr_high & 0xff
        descriptor[25] = (aq_descriptor.addr_high >> 8) & 0xff
        descriptor[26] = (aq_descriptor.addr_high >> 16) & 0xff
        descriptor[27] = (aq_descriptor.addr_high >> 24) & 0xff
        descriptor[28] = aq_descriptor.addr_low & 0xff
        descriptor[29] = (aq_descriptor.addr_low >> 8) & 0xff
        descriptor[30] = (aq_descriptor.addr_low >> 16) & 0xff
        descriptor[31] = (aq_descriptor.addr_low >> 24) & 0xff

        if debug_print:
            print 'AQ descriptor sent:'
            for i in range(0, desc_size):
                print descriptor[i],
            print

        ret_val = libSvPython.AllocWORD()
        status = libSvPython.send_adminqueue_command(self._device_string, descriptor, sent_aq_buffer, aq_buffer_size, ret_val)        

        if debug_print:
            print 'AQ descriptor received:'
            for i in range(0, desc_size):
                print descriptor[i],
            print
                  
        aq_descriptor.flags = libSvPython.get_aq_descriptor_flags(descriptor)
        aq_descriptor.opcode = libSvPython.get_aq_descriptor_opcode(descriptor)
        aq_descriptor.param0 = libSvPython.get_aq_descriptor_param0(descriptor)
        aq_descriptor.param1 = libSvPython.get_aq_descriptor_param1(descriptor)
        aq_descriptor.retval = libSvPython.get_aq_descriptor_retval(descriptor)
        aq_descriptor.datalen = libSvPython.get_aq_descriptor_datalen(descriptor)
        aq_descriptor.cookie_low = libSvPython.get_aq_descriptor_coockie_low(descriptor)
        aq_descriptor.cookie_high = libSvPython.get_aq_descriptor_cookie_high(descriptor)
        aq_descriptor.addr_low = libSvPython.get_aq_descriptor_addr(descriptor,True)
        aq_descriptor.addr_high = libSvPython.get_aq_descriptor_addr(descriptor,False)                         
    
        if aq_buffer is not None:                                                
            j = 0
            while j < aq_buffer_size:
                aq_buffer[j] = sent_aq_buffer[j]                
                j += 1            
        return status    

    def send_aq_command2(self, aq_descriptor, aq_buffer = None):
        '''This function sends AQ command.
            Arguments:
                aq_descriptor - aq command data descriptor with following fields
                    opcode, flags, param0, param1, cookie_high, cookie_low, address_high, address_low, retval, datalen.
                    If one of these fields not set default value is 0.
                 aq_buffer - optional buffer for AQ. Refer to EAS for specific command, each value represents byte.
                           If no buffer required pass None, default value is None.
                 Responsse from FW will be returned in these arguments.
        '''
        desc_size = libSvPython.get_aq_descriptor_size()
        completion = libSvPython.ByteArray(desc_size)
                
        aq_buffer_size = 0
        sent_aq_buffer = None
        if aq_buffer is not None:            
            aq_buffer_size = len(aq_buffer)
            sent_aq_buffer = libSvPython.ByteArray(aq_buffer_size)
            j = 0
            while j < aq_buffer_size:
                sent_aq_buffer[j] = aq_buffer[j]
                j += 1


        ret_val = libSvPython.send_adminqueue_command_with_parameters(self._device_string,  aq_descriptor.opcode, aq_descriptor.param0, aq_descriptor.param1, aq_descriptor.addr_high, aq_descriptor.addr_low, sent_aq_buffer, aq_buffer_size, completion)
                  
        aq_descriptor.flags = libSvPython.get_aq_descriptor_flags(completion)
        aq_descriptor.opcode = libSvPython.get_aq_descriptor_opcode(completion)
        aq_descriptor.param0 = libSvPython.get_aq_descriptor_param0(completion)
        aq_descriptor.param1 = libSvPython.get_aq_descriptor_param1(completion)
        aq_descriptor.retval = libSvPython.get_aq_descriptor_retval(completion)
        aq_descriptor.datalen = libSvPython.get_aq_descriptor_datalen(completion)
        aq_descriptor.cookie_low = libSvPython.get_aq_descriptor_coockie_low(completion)
        aq_descriptor.cookie_high = libSvPython.get_aq_descriptor_cookie_high(completion)
        aq_descriptor.addr_low = libSvPython.get_aq_descriptor_addr(completion,True)
        aq_descriptor.addr_high = libSvPython.get_aq_descriptor_addr(completion,False)                         
    
        if aq_buffer is not None:                                    
            j = 0
            while j < aq_buffer_size:
                aq_buffer[j] = sent_aq_buffer[j]
                j += 1  

    def receive_aq_command(self, aq_descriptor, aq_buffer = None, debug_print = False):
        '''This function receives AQ command.
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
        desc_size = libSvPython.get_aq_descriptor_size()
        descriptor = libSvPython.ByteArray(desc_size)
    
        aq_buffer_size = 0
        sent_aq_buffer = None
        if aq_buffer is not None:
            aq_buffer_size = len(aq_buffer)
            s = struct.Struct('b'*aq_buffer_size)
            packed_s = s.pack(*aq_buffer)
            sent_aq_buffer = str(packed_s)
    
        descriptor[0] = aq_descriptor.flags & 0xff
        descriptor[1] = (aq_descriptor.flags >> 8) & 0xff
        descriptor[2] = aq_descriptor.opcode & 0xff
        descriptor[3] = (aq_descriptor.opcode >> 8) & 0xff
        descriptor[4] = aq_descriptor.datalen & 0xff
        descriptor[5] = (aq_descriptor.datalen >> 8) & 0xff
        descriptor[6] = aq_descriptor.retval & 0xff
        descriptor[7] = (aq_descriptor.retval >> 8) & 0xff
        descriptor[8] = aq_descriptor.cookie_high & 0xff
        descriptor[9] = (aq_descriptor.cookie_high >> 8) & 0xff
        descriptor[10] = (aq_descriptor.cookie_high >> 16) & 0xff
        descriptor[11] = (aq_descriptor.cookie_high >> 24) & 0xff
        descriptor[12] = aq_descriptor.cookie_low & 0xff
        descriptor[13] = (aq_descriptor.cookie_low >> 8) & 0xff
        descriptor[14] = (aq_descriptor.cookie_low >> 16) & 0xff
        descriptor[15] = (aq_descriptor.cookie_low >> 24) & 0xff
        descriptor[16] = aq_descriptor.param0 & 0xff
        descriptor[17] = (aq_descriptor.param0 >> 8) & 0xff
        descriptor[18] = (aq_descriptor.param0 >> 16) & 0xff
        descriptor[19] = (aq_descriptor.param0 >> 24) & 0xff
        descriptor[20] = aq_descriptor.param1 & 0xff
        descriptor[21] = (aq_descriptor.param1 >> 8) & 0xff
        descriptor[22] = (aq_descriptor.param1 >> 16) & 0xff
        descriptor[23] = (aq_descriptor.param1 >> 24) & 0xff
        descriptor[24] = aq_descriptor.addr_high & 0xff
        descriptor[25] = (aq_descriptor.addr_high >> 8) & 0xff
        descriptor[26] = (aq_descriptor.addr_high >> 16) & 0xff
        descriptor[27] = (aq_descriptor.addr_high >> 24) & 0xff
        descriptor[28] = aq_descriptor.addr_low & 0xff
        descriptor[29] = (aq_descriptor.addr_low >> 8) & 0xff
        descriptor[30] = (aq_descriptor.addr_low >> 16) & 0xff
        descriptor[31] = (aq_descriptor.addr_low >> 24) & 0xff

        if debug_print:			
            print 'AQ descriptor sent:'
            for i in range(0, desc_size):
                print descriptor[i],
            print
            print 'Sent buffer:', sent_aq_buffer.__repr__()
   
        status = libSvPython.receive_adminqueue_command(self._device_string, descriptor, sent_aq_buffer, aq_buffer_size)
  
        if debug_print:
            print 'AQ descriptor received:'
            for i in range(0, desc_size):
                print descriptor[i],
            print
            print 'Received buffer:', sent_aq_buffer.__repr__()
    
        aq_descriptor.flags = libSvPython.get_aq_descriptor_flags(descriptor)
        aq_descriptor.opcode = libSvPython.get_aq_descriptor_opcode(descriptor)
        aq_descriptor.param0 = libSvPython.get_aq_descriptor_param0(descriptor)
        aq_descriptor.param1 = libSvPython.get_aq_descriptor_param1(descriptor)
        aq_descriptor.retval = libSvPython.get_aq_descriptor_retval(descriptor)
        aq_descriptor.datalen = libSvPython.get_aq_descriptor_datalen(descriptor)
        aq_descriptor.cookie_low = libSvPython.get_aq_descriptor_coockie_low(descriptor)
        aq_descriptor.cookie_high = libSvPython.get_aq_descriptor_cookie_high(descriptor)
        aq_descriptor.addr_low = libSvPython.get_aq_descriptor_addr(descriptor,True)
        aq_descriptor.addr_high = libSvPython.get_aq_descriptor_addr(descriptor,False) 
    
        if aq_buffer is not None:
            response_buffer = s.unpack(sent_aq_buffer)
            for i in range(0, len(response_buffer)):
                aq_buffer[i] = int(response_buffer[i])

        return status

    def device_reset(self, reset_type):
        ''' This function resets device.
            Arguments:
                reset_type - type of reset to perform. Options:
                'PF', 'CORE', 'GLOBAL', 'EMP', 'VF_SW', 'VFLR', 'FL'
                'PCI', 'PCE_RESTORE', 'BME', 'ACPI'

        '''
        reset_type_value = 0
        if reset_type == 'PF':
            reset_type_value = 0
        elif reset_type == 'CORE':
            reset_type_value = 1
        elif reset_type == 'GLOBAL':
            reset_type_value = 2
        elif reset_type == 'EMP':
            reset_type_value = 3
        elif reset_type == 'VF_SW':
            reset_type_value = 4
        elif reset_type == 'VFLR':
            reset_type_value = 5
        elif reset_type == 'FL':
            reset_type_value = 6
        elif reset_type == 'PCI':
            reset_type_value = 7
        elif reset_type == 'PCI_RESTORE':
            reset_type_value = 8
        elif reset_type == 'BME':
            reset_type_value = 9
        elif reset_type == 'ACPI':
            reset_type_value = 10
        else:
            raise RuntimeError("Unsupported reset type " + reset_type)

        libSvPython.reset_device_c(self._device_string, reset_type_value)

    def _read_csr(self, register_offset):       
        value = libSvPython.read_csr_c(self._device_string, register_offset)        
        return value[1] 

    def _create(self):                    
        status = libSvPython.svInit(self._device_string)        
        if status != libSvPython.ERROR_STATUS_OK:
            raise RuntimeError("Failed to init device {} device number {} port number {}, device not found".format(self._project_name, self._device_number, self._port_number))

    def _release(self):
        p
