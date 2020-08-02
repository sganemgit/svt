from datetime import datetime
from core.log.log import log


class testBase():
    def  __init__(self):
        self.testname = str(self.__class__).split('.')[-1]
        print self.testname
        self.logname = "{}_{}".format(datetime.now().strftime('%Y-%m-%d_%H_%M_%S'), self.testname)
        self.log = log(self.logname, "DEBUG")
        self._test_status = "pass"

    def run(self):
        print "must override the run function in every test"


    def set_test_status(self, status):
        if status.lower() == 'pass':
            self._test_status = "Pass"
        elif status.lower() == 'fail':
            self._test_status = "Fail"
        else:
            self.log.warning("Invalid Test Status - {}".format(status))
