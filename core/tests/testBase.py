
# @author Shady Ganem <shady.ganem@intel.com>

import os
from datetime import datetime
from core.log.log import log
import argparse
from core.devices.DeviceFactory import DeviceFactory
from core.exceptions.Exceptions import *
from core.tests.XmlParser import XmlParser

class testBase():

    def __init__(self):
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

#    def __init__(self):
#        self._parser = self._configure_parser(argparse.ArgumentParser())
#        self._args = self._parser.parse_args()
#
#        if self._args.output:
#            print(self._args.output)
#            self.output_path = self._args.output
#
#        self.testname = str(self.__class__).split('.')[-1]
#        self.logname = "{}_{}".format(datetime.now().strftime('%Y-%m-%d_%H_%M_%S'), self.testname)
#        self.log = log(self.logname, "DEBUG")
#        self.log.info(self.testname)
#        if self._args.auto:
#            self.log.info("Test Auto Mode Enabled")
#        else:
#            self._setup_dom = self._parse_setup_file()
#            self._reg_dom = self._parse_regression_file()
#            self.devices = self._create_devices()
#            self.pairs = self._create_dut_lp_pairs()
#            self.user_args = self._get_user_args()
#            self._core_args = self._get_core_args()
#        self._test_status = "Pass"
#        self._fail_reason_list = list()
#        self.test_iteration = 0
#        try:
#            self.run()
#        except Exception as e:
#            self.summarise_test()
#            raise e

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
            self.set_test_status('fail')
            self.append_fail_reason(str(e))
            raise e

    def _configure_parser(self, parser):
        parser.add_argument('-r', '--regression', help="Path to regression file")
        parser.add_argument('-s', '--setup' , help="Path to setup file")
        parser.add_argument('-a', '--auto', help="Automatically detect device. No setup or regressioin files required", action='store_true')
        parser.add_argument('-o', '--output', help="Set path to the output log file")
        return parser

    def run(self):
        self.log.warning("must override the run function in every test")

    def _parse_regression_file(self):
        try:
            if self._args.regression:
                regression_file_path = os.path.abspath(os.path.join(self._args.regression))
                regression_dom = ET.parse(regression_file_path)
                return regression_dom
            else:
                raise RegressionFileError("regression argument was not passed")
        except Exception as e:
            self.log.critical(str(e))
            raise e

    def _parse_setup_file(self):
        try:
            if self._args.setup:
                setup_file_path = os.path.abspath(os.path.join(self._args.setup))
                setup_dom = ET.parse(setup_file_path)
                return setup_dom
            else:
                raise SetupFileError("setup argument was not passed")
        except Exception as e:
            self.log.critical(str(e))
            raise e

    def _create_devices(self):
        devices_info_dict = dict()
        try:
            devices_list = self._setup_dom.getroot().findall('devices/device')
            for device_ET in devices_list:
                port_list = device_ET.findall('port')
                for port_ET in port_list:
                    info_dict = dict()
                    info_dict['device_name'] = device_ET.get('name')
                    info_dict['device_number'] = device_ET.get('driverDeviceNumber')
                    info_dict['hostname'] = device_ET.get('host')
                    info_dict['port_number'] = port_ET.get('driverPortNumber')
                    devices_info_dict[port_ET.get('uniqueId')] = info_dict
            devices_dict = dict()
            for device, info in devices_info_dict.iteritems():
                devices_dict[device] = DeviceFactory.create_device(info['device_name'], info['device_number'], info['port_number'], info['hostname'])
            return devices_dict
        except Exception as e:
            raise e

    def _get_core_args(self):
        args_dict = dict()
        try:
            parameter_list = self._reg_dom.getroot().findall('Parameter_List/parameter')
            for parameter_ET in parameter_list:
                if parameter_ET.get('type') == 'core':
                        args_dict[parameter_ET.get('name')] = parameter_ET.get('value')
            return args_dict
        except Exception as e:
            self.log.error("Error while parsing core args")
            raise e

    def _get_user_args(self):
        args_dict = dict()
        try:
            parameter_list = self._reg_dom.getroot().findall('Parameter_List/parameter')
            for parameter_ET in parameter_list:
                if parameter_ET.get('type') == 'user':
                        args_dict[parameter_ET.get('name')] = parameter_ET.get('value')
            return args_dict
        except Exception as e:
            self.log.error("Error while creating user args")
            raise e

    def _create_dut_lp_pairs(self):
        pairs = list()
        try:
            physicalLink_list = self._setup_dom.findall('physicalConnection/physicalLink')
            for physicalLink_ET in physicalLink_list:
                pair_dict = dict()
                item_list = physicalLink_ET.findall('item')
                for item_ET in item_list:
                    if item_ET.get('uniqueId') in self.devices:
                        if item_ET.get('role') == "DUT":
                            pair_dict['dut'] = self.devices[item_ET.get('uniqueId')]
                        elif item_ET.get('role') == "PARTNER":
                            pair_dict['lp'] = self.devices[item_ET.get('uniqueId')]
                        else:
                            raise DeviceRoleError("item {} has no role".format(item_ET.get('uniqueId')))
                    else:
                        raise PhysicalLinkError('item {} cannot be found in the devices'.format(item_ET.get('uniqueId')))
                pairs.append(pair_dict)
            return pairs
        except Exception as e:
            self.log.error("Error while creating DUT-LP pairs")
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
