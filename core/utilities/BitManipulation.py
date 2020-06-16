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


