#!/usr/bin/python3

# @author Shady Ganem <shady.ganem@intel.com>

import os
import argparse
from core.tests.XmlParser import XmlParser
from core.tests.TestFactory import TestFactory

def check_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg 

def configure_argparser_args(parser):
    parser.add_argument('-f', '--flow', help='Path to the test flow file', type=lambda x: check_file(parser, x))
    return parser

def main():
    args = configure_argparser_args(argparse.ArgumentParser()).parse_args()
    test_factory = TestFactory() # this object performs a lot of imports 
    for test, args, setup in XmlParser.IterTestCases(args.flow):
        if test in test_factory.tests_dict: 
            current_test = test_factory.create_test(test, args, setup)
            current_test.start_test()
            del current_test
        else:
            print('Test {} does not exist'.format(test))

if __name__=="__main__":
    main()

