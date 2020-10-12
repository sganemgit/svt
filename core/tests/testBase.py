
# @author Shady Ganem <shady.ganem@intel.com>

import os, sys
from datetime import datetime
from core.log.log import log
import argparse
from core.devices.DeviceFactory import DeviceFactory
from core.exceptions.Exceptions import *
from core.tests.XmlParser import XmlParser

class testBase():

    def __init__(self):
        self.test_start_time = datetime.now()
        self.testname = str(self.__class__).split('.')[-1]
        self.logname = "{}_{}".format(datetime.now().strftime('%Y-%m-%d_%H_%M_%S'), self.testname)
        self.log = log(self.logname, "DEBUG")
        self.log.info(self.testname)
        self._test_status = "Pass"
        self._fail_reason_list = list()
        self.test_iteration = 0
        self.args = dict()
        self.setup = dict()
        self.devices = dict()
        self.dut_lp_pairs = list()

    @classmethod
    def CreateTest(cls, args, setup):
        test_obj = cls()
        test_obj.args = args
        test_obj.setup = setup
        test_obj.devices = DeviceFactory.create_devices_from_setup(setup['Devices'])
        test_obj.dut_lp_pairs = DeviceFactory.create_dut_lp_pairs(setup['Links'], test_obj.devices)
        return test_obj

    def __del__(self):
        self.summarise_test()

    def __call__(self):
        self.start_test()

    def start_test(self):
        try:
            self.run()
        except Exception as e:
            import traceback
            traceback.print_exc(file=sys.stdout)
            self.set_test_status('fail')
            self.append_fail_reason(str(e))
            raise e

    def append_fail_reason(self, reason):
        self._fail_reason_list.append('Test Iteration #{} - {}'.format(self.test_iteration, reason))
        self.set_test_status('fail')

    def set_test_status(self, status):
        if status.lower() == 'pass':
            self._test_status = "Pass"
        elif status.lower() == 'fail':
            self._test_status = "Fail"
        elif status.lower == 'error':
            self._test_status = "Error"
        else:
            self.log.warning("Trying to set an invalid test status - {}".format(status))

    def summarise_test(self):
        if self._fail_reason_list:
            self.log.info("")
            for reason in self._fail_reason_list:
                self.log.info('Fail Reason ' + str(reason))
        self.log.info("")
        self.log.info("-----------------------")
        if self._test_status == "Pass":
            self.log.info("Test Status: {}".format(self._test_status),'g')
        else:
            self.log.info("Test Status: {}".format(self._test_status),'r')
        self.log.info("-----------------------")
        self.log.info("")
        self.log.info("{} ran for {}".format(str(self.__class__).split('.')[-1], str(datetime.now() - self.test_start_time)), 'g')
        self.log.info('')
