
# @author Shady Ganem <shady.ganem@intel.com>

from socket import *
import time

class LmServer:
    '''
        This class handles connections to the LM Server that runs on the MEV IMC
    '''
    def __init__(self, ip = '127.0.0.1', port = 5077):
        self._socket = socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(10)
        self._IP = ip 
        self._PORT = port
    
    def set_imc_tcp_ip_address(self, ip, port):
        self._IP = ip
        self._PORT = port
    
    def get_imc_tcp_ip_address(self):
        return (self._IP, self._PORT)

    def connect(self):
        try:
            self._socket.connect(self.get_imc_tcp_ip_address())
            time.sleep(0.2)
        except Exception as e:
            print('could not connect to imc')
            raise e

    def disconnect(self):
        self._socket.close()

    def receive(self):
        total_data = list()
        while True:
            data = self._socket.recv(1024)
            if not data: break
            total_data.append(data)
        return ''.join(total_data)

    def send(self):
        pass
        

