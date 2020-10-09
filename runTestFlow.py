#!/usr/bin/python

# @author Shady Ganem <shady.ganem@intel.com>


import sys
import os
import time
import argparse
import modulefinder
from core.tests.XmlParser import XmlParser
import tests

print dir(tests.TnT)

def find_test_class(testname):
    pass

def check_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg 
    
def configure_parser_args(parser):
    parser.add_argument('-f', '--flow', help='Path to the test flow file', required=True, type=lambda x: check_file(parser, x))
    return parser

def main():
    parser = configure_parser_args(argparse.ArgumentParser())
    args = parser.parse_args()
    XmlParser.TestFlow(args.flow)
    for test, args, setup in XmlParser.TestFlow(args.flow):
        print test
        print args
        print setup

if __name__=="__main__":
    main()





