#!/usr/bin/env python 
#check url pic using baidu stu api
#joey 20150611

import os
import re
import time
import sys
import requests
import urllib2
import urllib
import json

def baidu_stu_html_extract(html):
    pattern = re.compile(r"keywords:'(.*?)'")
    matches = pattern.findall(html)
    if not matches:
        return '[UNKOWN]'
    json_str = matches[0]
    json_str = json_str.replace('\\x22', '"').replace('\\\\', '\\')
    result = [item['keyword'] for item in json.loads(json_str)]
    return '|'.join(result) if result else '[UNKOWN]'

def baidu_stu_lookup(path):
    url = ("http://stu.baidu.com/n/image?fr=html5&needRawImageUrl=true&id="
          "WU_FILE_0&name=233.png&type=image%2Fpng&lastModifiedDate=Mon+Mar"
          "+16+2015+20%3A49%3A11+GMT%2B0800+(CST)&size=")
    raw = open(path, 'rb').read()
    url = url + str(len(raw))
    req = urllib2.Request(url, raw, {'Content-Type':'image/png', 'User-Agent':UA})
    resp = urllib2.urlopen(req)
    resp_url = resp.read()      # return a pure url
    url = "http://stu.baidu.com/n/searchpc?queryImageUrl=" + urllib.quote(resp_url)
    req = urllib2.Request(url, headers={'User-Agent':UA})
    resp = urllib2.urlopen(req)
    html = resp.read()
    return baidu_stu_html_extract(html)

def downloadImg(url):
    pic_file = int(time.time())
    print '[+] Download Picture: {}'.format(url)
    try:
        resp = requests.get(url, verify=False, timeout=5)
    except:
        resp = requests.get(url, verify=False, timeout=3)
    with open("./pic/%s.png"%pic_file, 'wb') as fp:
        fp.write(resp.content)
    return pic_file


if __name__ == '__main__':
    try:
    	UA = "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36"
        url = sys.argv[1]
        pic_file = downloadImg(url)
        file = str(pic_file)+'.png'
    	path = './pic/'+file
        result = baidu_stu_lookup(path)
        print result
    except Exception, e:
        print 'Usage: %s http://pic_url.com/test.jpg' % sys.argv[0]
        print 'Error: %s' % str(e)
        pass