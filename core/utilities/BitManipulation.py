def compose_num_from_array_slice(buffer, start_index, length):
    ''' This function builds number from bytes in array and returns it
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

def _calculate_port_offset(offset_base, mul, port_number):
    '''This function return port offset according to port number and offset.
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
    '''This function return the value from specific bit
        argument:
            value (hex) - value from register
            bit_number (int) 
    '''
    return (value >> bit_number) & 0x1

