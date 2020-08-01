from datetime import datetime
from core.log.log import log


class testBase():
    def  __init__(self):
        self.testname = str(self.__class__).split('.')[-1]
        print self.testname
        self.logname = "{}_{}".format(datetime.now().strftime('%Y-%m-%d_%H:%M:%S'), self.testname)
        self.log = log(self.logname, "DEBUG")

    def run(self):
        print "must override the run function in every test"


