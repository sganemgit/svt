

from core.drivers.ftdidriver.FtdiDriver import FtdiDriver

class cvlFpga:
    def __init__(self, index):
        self.index = index

    def connect(self):
        try:
            self._driver_proxy = FtdiDriver(self.index) 
        except Exception as e:
            raise e
