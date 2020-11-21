
from core.drivers.ftdidriver.FtdiDriver import FtdiDriver


class FpgaHandler:

    def __init__(self):
        try:
            if self.is_ftdi_connected():
                print("TODO: Init FTDI driver instance")
            else: 
                print("no FTDI devcie dectected")

        except Exception as e:
            print('Failed to deceted FTDI')

    def is_ftdi_connected(self):
        return True if FtdiDriver.GetFtdiDevices() else False

if __name__=='__main__':
    FpgaHandler()
