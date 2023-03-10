
# @author Shady Ganem <shady.ganem@intel.com>

import os, sys
from datetime import datetime
from core.log.log import log
from core.log.dataframe import dataframe
import argparse
from core.devices.DeviceFactory import DeviceFactory
from core.exceptions.Exceptions import *
from core.tests.XmlParser import XmlParser
from core.instruments.InstrumentFactory import InstrumentFactory

class testBase():

    @classmethod
    def CreateTest(cls, args, setup):
        try:
            test_obj = cls(args.get("log_level", "INFO"))
            test_obj.args = args
            test_obj.setup = setup
            test_obj.instruments = InstrumentFactory.create_instruments_from_setup(setup["Instruments"])
            test_obj.devices = DeviceFactory.create_devices_from_setup(setup['Devices'])
            test_obj.dut_lp_pairs = DeviceFactory.create_dut_lp_pairs(setup['Links'], test_obj.devices)
            return test_obj
        except Exception as e:
            import traceback
            traceback.print_exc(file=sys.stdout)
            test_obj.set_test_status('fail')
            test_obj.append_fail_reason(str(e))
            raise e

    def __init__(self, log_level="INFO"):
        self.test_start_time = datetime.now()
        self.testname = (str(self.__class__).split("'")[1]).split(".")[-1]
        self.logname = "{}_{}".format(datetime.now().strftime('%Y-%m-%d_%H_%M_%S'), self.testname)
        self.log = log(self.logname, log_level)
        self.table = dataframe(self.logname)
        self.log.info(self.testname)
        self._test_status = "Pass"
        self._fail_reason_list = list()
        self._error_list = list()
        self.test_iteration = 0
        self.args = dict()
        self.setup = dict()
        self.devices = dict()
        self.dut_lp_pairs = list()

    def __del__(self):
        self.table.flush()
        self.summarise_test()

    def __call__(self):
        self.start_test()

    def start_test(self):
        try:
            self.test_start_time = datetime.now()
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
        self.log.info("{} ran for {}".format(self.testname, str(datetime.now() - self.test_start_time)), 'o')
        self.log.info('')
