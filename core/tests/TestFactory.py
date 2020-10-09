
# @author Shady Ganem <shady.ganem@intel.com>

import os
import imp

class TestFactory:
    
    def __init__(self):
        self.tests_paths = self._get_all_test_modules_paths()
        for item in self.tests_paths:
            print item

    def _iter_submodules(self, package):
        file, pathname, description = imp.find_module(package)
        for dirpath, _, filenames in os.walk(pathname):
            for  filename in filenames:
                if os.path.splitext(filename)[1] == ".py":
                    if not '__init__' in filename:
                        yield (os.path.join(dirpath, filename), filename)

    def _get_all_test_modules_paths(self):
        path_list = list()
        for module_path , module_name in self._iter_submodules('tests'):
            try:
                print module_name.split('.')[0]
                print module_path
                temp_module = imp.load_source(module_name.split('.')[0] , module_path)
                if 'TEST' in dir(temp_module):
                    if temp_module.TEST:
                        path_list.append(module_path)
            except Exception as e:
                print('Exception "{}" was raised while trying to import module {}'.format(str(e), module_name))
        return path_list

    def get_all_availble_tests(self):
        return self.tests_paths

if __name__=="__main__":
    TestFactory()
