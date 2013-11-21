#!/usr/bin/env python

import time
import socket,re,urllib,urllib2,os,sys
from threading import Thread
import subprocess
from Queue import Queue
#from color import inRed, inGreen


timeout = 5
ip_queue = Queue()

def scan_port(ip,port,timeout=timeout):
	try:
		#print "ip:%s,port:%s"% (ip,port)
		cs=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		cs.settimeout(float(timeout))
		address=(str(ip),int(port))
		status=cs.connect_ex(address)
		if status == 0:
			print "host:%s port:%s ok" % (ip,port)
			#print inGreen("host:%s port:%s ok" % ip,port)
		else:
			print "host:%s port:%s down" % (ip,port)
			return 0
	except Exception,e:
		#print inRed("error:%s" % ip)
		print "error:%s" % e
		return 1
	return 0

file = raw_input("enter the file to check the services:")
f = open(file,'r')
for eachline in f:
	ip=eachline.split(':')[0].strip('\n')
        port=eachline.split(':')[1].strip('\n')
	#print "ip:%s,port:%s"% (ip,port)
	scan_port(ip,port,5)
f.close()


