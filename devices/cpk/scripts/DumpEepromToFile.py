

from devices.cpk.cpk import cpk
import binascii

def main():
    cpk0 = cpk(0,0,'')
    eeprom_data = cpk0.ReadSffEeprom()
    for port, data in eeprom_data.items():
        with open('sff_eeprom_dump_port_{}.hex'.format(port), 'w+') as f:
            bin_arr = bytearray(data)
            line = 0
            for index, byte in enumerate(data):
                if index % 16 == 0:
                    if index == 0:
                        f.write("{:07x}".format(line)+"0    ")
                        f.write('{:02x}'.format(byte, 'x')+' ')
                    else:
                        f.write('    ')
                        for item in data[line*16:line*16+16]:
                            f.write(chr(item))
                            print("{} : {}".format(item, chr(item)))

                        f.write('\n')
                        line += 1
                        f.write("{:07x}".format(line)+"0    ")
                        f.write('{:02x}'.format(byte, 'x')+' ')
                else:
                    f.write('{:02x}'.format(byte, 'x')+' ')

            f.write('\n')

if __name__=='__main__':
    main()
