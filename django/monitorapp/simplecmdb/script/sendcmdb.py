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
    cpuinfo = parserCpuInfo(getCpuInfo())
    diskinfo = parserDiskInfo(getDiskInfo())
    for i in parserMemInfo(getMemInfo()):
        meminfo = i
    productinfo = parserDMI(getDMI())
    hostinfo = getHostInfo()
    ipaddr = parserIpaddr(getIpaddr())
    for i in ipaddr:
        ip = i
    for k in cpuinfo.iteritems():
        ld.append(k)
    for i in diskinfo.iteritems():
        ld.append(i)
    for j in meminfo.iteritems():
        ld.append(j)
    for v in productinfo.iteritems():
        ld.append(v)
    for x in hostinfo.iteritems():
        ld.append(x)
    for y in ip.iteritems():
        ld.append(y)
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
        req = urllib2.Request('http://192.168.1.4:8080/api/collect',headers=headers,data=data)
        url = 'http://192.168.1.4:8080/api/collect'
        response = urllib2.urlopen(req)
        return response.read()
    except urllib2.HTTPError,e:
        print e
if __name__=='__main__':
    hostdata = getHostTotal()
    postdata = parserHostTotal(hostdata)
    #print postdata
    print urlPost(postdata)
