#!/usr/bin/env python
# coding=utf8
# author=evi1m0@2015<ff0000team>
#http://linux.im/2015/03/01/cloudSight-api.html

import sys
import time
import requests

def _api(url):
    count = 0
    api_url = 'http://api.cloudsightapi.com/image_requests'
    res_url = 'http://api.cloudsightapi.com/image_responses/'
    headers = {
                'Origin': 'http://cloudsightapi.com',
                'HOST': 'api.cloudsightapi.com',
                'Authorization': 'CloudSight amZd_zG32VK-AoSz05JLIA',
              }
    post_data = {
                'image_request[remote_image_url]': url,
                'image_request[locale]': 'zh-CN',
                'image_request[language]': 'zh-CN',
                }

    token_req = requests.post(api_url, data=post_data, headers=headers)
    token = token_req.json()['token']
    while count<10:
        try:
            count += 1
            print '[+] Loading...'
            result = requests.get('%s%s'%(res_url, token), headers=headers)
            status = result.json()['status']
            if status == 'completed':
                print '[+] Pic: %s' % url
                print '[*] Name: %s' % result.json()[u'name']
                break
        except Exception, e:
            print '[-] False: %s' % str(e)
            pass


if __name__ == '__main__':
    try:
        url = sys.argv[1]
        _api(url)
    except Exception, e:
        print 'Usage: cloudsightapi.py http://pic_url.com/test.jpg'
        print 'Error: %s' % str(e)
        pass