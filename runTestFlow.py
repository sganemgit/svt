#!/usr/bin/python

# @author Shady Ganem <shady.ganem@intel.com>

import sys
import os
import time
import argparse
import modulefinder
from core.tests.XmlParser import XmlParser
from core.tests.TestFactory import TestFactory

def check_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg 
    
def configure_parser_args(parser):
    parser.add_argument('-f', '--flow', help='Path to the test flow file', type=lambda x: check_file(parser, x))
    return parser

def main():
    parser = configure_parser_args(argparse.ArgumentParser())
    args = parser.parse_args()
    test_factory = TestFactory() # this object performs a lot of imports 
    XmlParser.TestFlow(args.flow)
    for test, args, setup in XmlParser.TestFlow(args.flow):
        if test in test_factory.tests_dict: 
            current_test = test_factory.create_test(test)
            current_test.start_test()
            del current_test
        else:
            print('Test {} does not exist'.format(test))

if __name__=="__main__":
    main()





