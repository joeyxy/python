#!/usr/bin/env python
# coding=utf8
# author=f1#ff0000team

import re
import sys
import json
import requests

reload(sys)
sys.setdefaultencoding('utf-8')


f_obj = open('./ip.list','r')
f_content = f_obj.readlines()
for i in f_content:
    url = 'http://ip.taobao.com/service/getIpInfo.php?ip=%s' % i
    try:
        page_content = requests.get(url).text.encode('utf8')
    except:
        continue
    json_data = json.loads(page_content)
    ip = json_data['data']['ip'][:-1]
    country = json_data['data']['country']
    return_str = ip + ' --- ' + country + '\n'
    print return_str
    output = open('./port27017_aliip.txt', 'a+')
    output.write(return_str)
    output.close()