
#--------------------------------------------
# @author Shady Ganem <shady.ganem@intel.com>
#--------------------------------------------

import math 

def compose_num_from_array_slice(buffer, start_index, length):
    ''' 
        This function builds number from bytes in array and returns it
        Arguments:
            buffer - array of bytes
            start_index - index of byte to start from, will be MSB in final number
            length - number of bytes starting from 'start_index' that will be included in final number
        Returns:
            number composed from bytes
    '''    
    temp = buffer[start_index:start_index+length]
    length = len(temp)
    result = temp[length-1]
    for i in range(length-2,-1,-1):
        result = result << 8 | temp[i]
    return result

def calculate_port_offset(offset_base, mul, port_number):
    '''
        This function return port offset according to port number and offset.
    '''
    return offset_base + mul * port_number

def get_bits_slice_value(value, bit_start_number, bit_end_number):
        '''This function return value from slice of bits
            arguments: value, bit_start_number, bit_end_number
            return: slice value
        '''
        mask_length = bit_end_number - bit_start_number + 1
        mask_string = '1' * mask_length
        mask = int(mask_string, 2)
        slice_value = (value >> bit_start_number) & mask    
        return slice_value

def get_bit_value(value, bit_number):
    '''
        This function return the value from specific bit
        argument:
            value (hex) - value from register
            bit_number (int) 
    '''
    return (value >> bit_number) & 0x1

def intgerTo4ByteList(I):
        '''
            this is a Level 0 function that convert a 4-byte integer to an array of length 4 that contans the 4 bytes
            argument: I = integer
            return: list of length 4
        '''
        data = [0]*4
        data[0] = I&0xFF
        data[1] = (I&0xff00)>>8
        data[2] = (I&0xff0000)>>16
        data[3] = (I&0xff000000)>>24
        return data

def turn_arg_to_bytes(number):
    '''
        param arg: int[4 bytes]
        return: list of all  bytes
    '''
    byte_list = list()
    if number:
        temp_inp = number
        for i in range(int(math.log(number,256))+1):
            byte_list.append(temp_inp & 0xFF)
            temp_inp = temp_inp >> 8
    return byte_list