#!/usr/bin/env python
import unittest
from ConfigParser import ConfigParser
from argparse import ArgumentParser
from glob import glob
import os, sys, shutil
sys.path.append(os.path.abspath('..'))
from core.sessions import cfgfilepath

def run_all(confpatterns):
    
    files = []
    for pattern in confpatterns:
        files.extend(glob(pattern))
        
    module_strings = [str[0:len(str)-3] for str in files]
    suites = [unittest.defaultTestLoader.loadTestsFromName(str) for str in module_strings]
    testSuite = unittest.TestSuite(suites)
    text_runner = unittest.TextTestRunner(verbosity=2).run(testSuite)
    
confpath = ''
confpattern = []

argparser = ArgumentParser()
argparser.add_argument('ini_file')
argparser.add_argument('test_patterns', nargs='*', default =  [ 'test_*.py' ])
argparser.add_argument('-showcmd', action='store_true')
argparser.add_argument('-showtest', action='store_true')

parsed = argparser.parse_args()

configparser = ConfigParser()
configparser.read(parsed.ini_file)
conf = configparser._sections['global']
conf['showcmd'] = parsed.showcmd
conf['showtest'] = parsed.showtest
conf['shell_sh'] = True if conf['shell_sh'].lower() == 'true' else False


if __name__ == "__main__":
    run_all(parsed.test_patterns)
    shutil.rmtree(cfgfilepath)
