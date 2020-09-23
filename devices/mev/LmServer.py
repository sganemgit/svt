
# @author Shady Ganem <shady.ganem@intel.com>



from socket import *
import time



class LmServer:
    '''
        This class handles connections to the LM Server that runs on the MEV IMC
    '''


    def __init__(self, ip = '127.0.0.1', port = '5077'):
        self._socket = socket()
        self._socket.settimeout(10)
        self._IP = ip 
        self._PORT = port
    
    def set_imc_tcp_ip_address(self, ip, port):
        self._IP = ip
        self._PORT = port
    
    def get_imc_tcp_ip_address(self):
        return self._IP, self._PORT

    def connect(self):
        try:
            self._socket(self.get_imc_tcp_ip_address())
            time.sleep(0.2)
        except Exception as e:
            print('could not connect to imc')
            raise e

    def lm_server_recv(self):
        pass

