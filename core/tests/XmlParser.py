
# @author Shady Ganem <shady.ganem@intel.com>

import xml.etree.ElementTree as ET

class XmlParser():

    @classmethod
    def IterTestCases(cls, path_to_test_flow):
        '''
        setup_dict = {'Devices': device_dict ={'device_0':{'name':value,
                                                           'hostname': value,
                                                           'number': value,
                                                           'Ports': {'someid': number,
                                                                     'someotherid': number}},
                                                'device_n': {...}}

                       'Links':   links_dict = {'link_0':{role: id,
                                                          role: id},
                                                 'link_n':{...}}}
        '''
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
                device_dict = dict()
                link_dict = dict()

                device_dom_list = testcase_dom.findall('Setup/Devices/Device')
                if device_dom_list:
                    for index, device_dom in enumerate(device_dom_list):
                        device_dict['device_{}'.format(index)] = device_dom.attrib
                        pf_dict = dict()
                        pf_dom_list = device_dom.findall('Port')
                        if pf_dom_list:
                            for pf in pf_dom_list:
                                pf_dict[pf.attrib['ID']] = pf.attrib['number']

                        device_dict['device_{}'.format(index)]['Ports'] = pf_dict
                
                link_dom_list = testcase_dom.findall('Setup/Links/Link')
                if link_dom_list:
                    for index, link_dom in enumerate(link_dom_list):
                        pf_dict = dict()
                        pf_dom_list = link_dom.findall('Port')
                        if pf_dom_list:
                            for pf in pf_dom_list:
                                pf_dict[pf.attrib['role']] = pf.attrib['ID']
                        
                        link_dict['link_{}'.format(index)] = pf_dict

                setup_dict['Devices'] = device_dict
                setup_dict['Links'] = link_dict
                yield (test_name, user_args_dict, setup_dict)
        except Exception as e:
            raise e

    @classmethod
    def TestFlow(cls, path_to_test_flow):
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
    def IterRegressionAndSetup(self, path_to_reg_file, path_to_setup_file):
        try:
            reg_xml_tree = ET.parse(path_to_test_flow)
            setup_xml_tree = ET.parse(path_to_setup_file)
        except Exception as e:
            raise e

