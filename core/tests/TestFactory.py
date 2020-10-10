
# @author Shady Ganem <shady.ganem@intel.com>

import os
import imp
import sys

class TestFactory:
    
    def __init__(self):
        self.tests_dict = self._get_all_test_modules_paths()

    def _iter_submodules(self, package):
        file, pathname, description = imp.find_module(package)
        for dirpath, _, filenames in os.walk(pathname):
            for  filename in filenames:
                if os.path.splitext(filename)[1] == ".py":
                    if not '__init__' in filename:
                        yield (dirpath, filename)

    def _get_all_test_modules_paths(self):
        test_dict = dict()
        for module_path, module_name in self._iter_submodules('tests'):
            try:
                module_name_wo_extension = module_name.split('.')[0]
                if module_path not in sys.path:
                    sys.path.append(module_path)
                temp_module = __import__(module_name_wo_extension)
                if 'TEST' in dir(temp_module):
                    if temp_module.TEST:
                        test_dict[module_name_wo_extension] = module_path
            except Exception as e:
                print('Exception "{}" was raised while trying to import module {}'.format(str(e), module_name))
        return test_dict 

    def iter_available_tests(self):
        for test_name in self.test_dict.keys():
            yield test_name

    def get_all_available_tests(self):
        return self.test_dict.keys()

    def get_all_available_tests_full_path(self):
        test_full_path_list = list()
        for test_name, test_path in self.tests_dict.items():
            test_full_path_list.append(sys.path.join(test_path, test_name))
        return test_full_path_list
    
    def create_test(self, test_name):
        try:
            if test_name in self.tests_dict.keys():
                if not self.tests_dict[test_name] in sys.path:
                    sys.path.append(self.tests_dict[test_name])
                module = __import__(test_name)
                return module.__dict__[test_name]()
        except Exception as e:
            raise e

if __name__=="__main__":
    TestFactory()
