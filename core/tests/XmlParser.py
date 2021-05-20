
# @author Shady Ganem <shady.ganem@intel.com>

import xml.etree.ElementTree as ET
from core.utilities.colors import colors

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
                #parsing the test name
                test_name = testcase_dom.find('Test').attrib['name']
                #parsing the input arguments
                user_args_dict = dict()
                parametes_list = testcase_dom.findall('Input/Parameter')
                if parametes_list:
                    for parameter in parametes_list:
                        param = parameter.attrib['name']
                        value = parameter.attrib['value']
                        user_args_dict[param] = value
                
                #parsing setup arguments
                setup_dict = dict()
                device_dict = dict()
                link_dict = dict()
                instrument_dict = dict()
                #parsing devices 
                device_dom_list = testcase_dom.findall('Setup/Devices/Device')
                if device_dom_list:
                    for index, device_dom in enumerate(device_dom_list):
                        device_key = "device{}".format(index)
                        device_dict[device_key] = device_dom.attrib
                        pf_dict = dict()
                        pf_dom_list = device_dom.findall('PF')
                        if pf_dom_list:
                            for pf in pf_dom_list:
                                pf_dict[pf.attrib['ID']] = pf.attrib
                        device_dict[device_key]['PFs'] = pf_dict
                
                #parsing links
                link_dom_list = testcase_dom.findall('Setup/Links/Link')
                if link_dom_list:
                    for index, link_dom in enumerate(link_dom_list):
                        pf_dict = dict()
                        pf_dom_list = link_dom.findall('PF')
                        if pf_dom_list:
                            for pf in pf_dom_list:
                                pf_dict[pf.attrib['role']] = pf.attrib['ID']
                        
                        link_dict['link_{}'.format(index)] = pf_dict
                
                #parsing instruments
                inst_id_list = list()
                instrumet_dom_list = testcase_dom.findall('Setup/Instruments/Instrument')
                if instrumet_dom_list:
                    for index, instrument_dom in enumerate(instrumet_dom_list):
                        current_inst_id =  instrument_dom.attrib.get("ID", f"instrument_{index}")
                        if current_inst_id not in inst_id_list:
                            inst_id_list.append(current_inst_id)
                            instrument_dict[current_inst_id] = instrument_dom.attrib
                        else:
                            print(colors.Orange("WARNING: Instrument with ID '{}' already exists".format(current_inst_id)))

                setup_dict['Devices'] = device_dict
                setup_dict['Links'] = link_dict
                setup_dict['Instruments'] = instrument_dict
                yield (test_name, user_args_dict, setup_dict)
        except Exception as e:
            #TODO gracefully handle exceptions
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
            reg_xml_tree = ET.parse(path_to_reg_file)
            setup_xml_tree = ET.parse(path_to_setup_file)
        except Exception as e:
            raise e

