#!/usr/bin/env python
import urllib,urllib2
import sys

def urlPost(postdata):
    try:
        data = urllib.urlencode(postdata)
        headers = {'User-Agent':'Mozilla/5.0(Windows;U;Windows NT 6.1;en-US;rv:1.9.1.6)Gecko/20091201 Firefox/3.5.6'}
        req = urllib2.Request('http://192.168.2.38:8090/api/tq_collect',headers=headers,data=data)
        response = urllib2.urlopen(req)
        return response.read()
    except urllib2.HTTPError,e:
        print e
if __name__=='__main__':
    if len(sys.argv) != 8:
        sys.stderr.write("Usage:./api.py ip time zone application ops status runtime\n")
        raise SystemExit(1)
    ip = sys.argv[1]
    time = sys.argv[2]
    zone = sys.argv[3]
    app = sys.argv[4]
    ops = sys.argv[5]
    status = sys.argv[6]
    runtime = sys.argv[7]
    postdata = {'ip':ip,'time':time,'zone':zone,'app':app,'ops':ops,'status':status,'runtime':runtime}
    print postdata
    print urlPost(postdata)
