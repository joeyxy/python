#!/usr/bin/python

import sys, urllib, urllib2, json

url = 'http://apis.baidu.com/apistore/iplookupservice/iplookup?ip=117.89.35.58'


req = urllib2.Request(url)

req.add_header("apikey", "82daebb3d355823f09432a5213f41bf1")

resp = urllib2.urlopen(req)
content = resp.read()
if(content):
    print u'content:%s' % content