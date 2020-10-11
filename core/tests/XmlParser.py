
# @author Shady Ganem <shady.ganem@intel.com>

import xml.etree.ElementTree as ET

class XmlParser():

    @classmethod
    def TestFlow(self, path_to_test_flow):
        try:
            testflow = list()
            xml_tree = ET.parse(path_to_test_flow)
            testflow_dom = xml_tree.getroot()
            testcase_dom_list = testflow_dom.findall('TestCase')
            for testcase_dom in testcase_dom_list:
                test_name = testcase_dom.find('Test').attrib['name']
                user_args_dict = dict()
                parametes_list = testcase_dom.findall('Input/Parameter')
                if parametes_list:
                    for parameter in parametes_list:
                        param = parameter.attrib['name']
                        value = parameter.attrib['value']
                        user_args_dict[param] = value
                setup_dict = dict()
                testflow.append((test_name, user_args_dict, setup_dict))
            return testflow
        except Exception as e:
            raise e

    @classmethod    
    def RegressionFile(self, path_to_reg_file):
        try:
            xml_tree = ET.parse(path_to_test_flow)
        except Exception as e:
            raise e

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
