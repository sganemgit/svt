
from devices.cnv.cnvBase import cnvBase

class cvn(cnvBase):

    def PrintInfo(self):
        print(self.info())

    def info(self):
        return self.device_name
