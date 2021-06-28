
TEST = True

from core.tests.testBase import testBase 

class DumpyTest(testBase):

    def run(self):
        print("testing the testing mechanism")
        self.set_test_status('fail')
        for prot_id, device in self.devices.items():
            device.info()
