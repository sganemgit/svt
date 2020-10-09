
# @author Shady Ganem <shady.ganem@intel.com>

import  xml.etree.ElementTree as ET

class XmlParser():
    def __init__(self):
        pass


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
