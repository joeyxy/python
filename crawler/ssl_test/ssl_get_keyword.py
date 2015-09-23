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
            keywords = ['system', 'password', 'passwd', 'admin']
            for word in keywords:
                if result.find(word) > 0:
                    print 'new data', time.asctime()
                    with open('data_' + time.strftime("%y-%m-%d-%H-%M") + '.txt', 'w') as f:
                        f.write(result)
                        break
        time.sleep(1.0)