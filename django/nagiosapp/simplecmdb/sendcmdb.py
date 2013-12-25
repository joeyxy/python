#!/usr/bin/env python
import urllib,urllib2
#from host import *
import platform

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
	hostinfo = getHostInfo()
	for x in hostinfo.iteritems():
		ld.append(x)

def parserHostTotal(hostdata):
	pg = {}
	for i in hostdata:
		pg[i[0]] = i[0]
	return pg

def urlPost(postdata):
	data = urllib.urlencode(postdata)
	req = urllib2.Request('http://192.168.57.228:8088/api/collect',data)
	response = urllib2.urlopen(req)
	return response.read()

if __name__=='__main__':
	hostdata = getHostTotal()
	postdata = parserHostTotal(hostdata)
	print urlPost(postdata)
