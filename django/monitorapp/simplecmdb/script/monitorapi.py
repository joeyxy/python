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
    ld = {'ip':'192.168.2.11','time':'20140716','game':'mhtq','app':'jdk','pid':'1234','useage':'105'}
    #ld = {'ip':'192.168.2.11','time':'2014-07-09 12:30','game':'mhtq','app':'jdk','pid':'1234','useage':'105'}
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
    if len(sys.argv) != 7:
        sys.stderr.write("Usage:./api.py ip time game application pid useage\n")
        raise SystemExit(1)
    ip = sys.argv[1]
    time = sys.argv[2]
    game = sys.argv[3]
    app = sys.argv[4]
    pid = sys.argv[5]
    useage = sys.argv[6]
    postdata = {'ip':ip,'time':time,'game':game,'app':app,'pid':pid,'useage':useage}
    #postdata = getHostTotal()
    #postdata = parserHostTotal(hostdata)
    print postdata
    print urlPost(postdata)
