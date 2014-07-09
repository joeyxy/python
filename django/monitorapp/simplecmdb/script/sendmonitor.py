#!/usr/bin/env python
import urllib,urllib2
#from host import *
#import platform
from cpuinfo import *
from diskinfo import *
from meminfo import *
from product import *
from hostinfo import *
from ipaddress import *

def getHostInfo():
        pd = {}
        version = platform.dist()
        os_name = platform.node()
        os_release = platform.release()
        os_version = '%s %s' % (version[0],version[1])
        pd['os_name'] = os_name
        pd['os_release'] = os_release
        pd['os_version'] = os_version
        return pd


def getHostTotal():
    ld = []
    ip = "192.168.2.11"
    time = "20140709"
    game = "mhtq"
    app = "jdk"
    pid = "12345"
    useage = "105"
    ld.append(ip)
    ld.append(time)
    ld.append(game)
    ld.append(app)
    ld.append(pid)
    ld.append(useage)
    return ld

def parserHostTotal(hostdata):
	pg = {}
	for i in hostdata:
		pg[i[0]] = i[1]
	return pg

def urlPost(postdata):
    try:
        data = urllib.urlencode(postdata)
        headers = {'User-Agent':'Mozilla/5.0(Windows;U;Windows NT 6.1;en-US;rv:1.9.1.6)Gecko/20091201 Firefox/3.5.6'}
        req = urllib2.Request('http://192.168.2.38:8090/api/monitor_collect',headers=headers,data=data)
        url = 'http://192.168.2.38:8090/api/monitor_collect'
        response = urllib2.urlopen(req)
        return response.read()
    except urllib2.HTTPError,e:
        print e
if __name__=='__main__':
    hostdata = getHostTotal()
    postdata = parserHostTotal(hostdata)
    print postdata
    print urlPost(postdata)
