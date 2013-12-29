#!/usr/bin/env python

#usage:health_check.py ip port

import socket
import os
import sys
from threading import Thread
from Queue import Queue

timeout = 5
def scan(line,timeout=timeout):
    try:
        ip=line.split(':')[0].strip('\n')
        port=line.split(':')[1].strip('\n')
        cs=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        cs.settimeout(float(timeout))
        address=(str(ip),int(port))
        status=cs.connect_ex(address)
        if status == 0:
            #return {'ip':'%s','port':'%s','status':'up'} % (ip,port)
            return "%s,%s,up" % (ip,port)
        else:
            return "[%s, %s,down]" % (ip,port)
            #return {'ip':'%s','port':'%s','status':'down'} % (ip,port)
    except Exception,e:
        print "error:%s" % e

def scan_port(ip,port,timeout=timeout):
    try:
        cs=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        cs.settimeout(float(timeout))
        address=(str(ip),int(port))
        status=cs.connect_ex(address)
        if status == 0:
            result = 'ok'
            print result
            return result
        else:
            result = 'down'
            print result
            return result
    except Exception,e:
            return "error:%s" % e


if __name__ == "__main__":
    if not len(sys.argv)>2:
        print __doc__
        sys.exit(1)
    result = scan_port(sys.argv[1],sys.argv[2])
    print result
