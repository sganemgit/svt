import os
from datetime import datetime
from core.log.log import log
import argparse
import  xml.etree.ElementTree as ET

class testBase():
    def  __init__(self):
        self.testname = str(self.__class__).split('.')[-1]
        self.logname = "{}_{}".format(datetime.now().strftime('%Y-%m-%d_%H_%M_%S'), self.testname)
        self.log = log(self.logname, "DEBUG")
        self.log.info(self.testname)
        self._parser = self._configure_parser()
        self._args = self._parser.parse_args()
        print(self._args.setup)
        print(self._args.regression)
        self.setup = self._parse_setup_file()
        self._test_status = "Pass"
        self.user_args = self._parse_regression_file()
        self.run()

    def _configure_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-r','--regression', help="Path to the regression file")
        parser.add_argument('-s', '--setup'    , help="Path to the setup file")
        return parser

    def run(self):
        self.log.warning("must override the run function in every test")


    def _parse_regression_file(self):
        try:
            tree = ET.parse(self._args.regression)
        except Exception as e:
            self.log.critical(str(e))
            raise e

    def _parse_setup_file(self):
        try:
            tree = ET.parse(self._args.setup)
            root = tree.getroot()
            print(root)
        except Exception as e:
            self.log.critical(str(e))
            raise e

    def set_test_status(self, status):
        if status.lower() == 'pass':
            self._test_status = "Pass"
        elif status.lower() == 'fail':
            self._test_status = "Fail"
        else:
            self.log.warning("Invalid Test Status - {}".format(status))
