#!/usr/bin/env python

import time
import socket,re,urllib,urllib2,os,sys
from threading import Thread
import subprocess
from Queue import Queue
#from color import inRed, inGreen


timeout = 5
ip_queue = Queue()
num_threads = 10 

def scan_port(iq,timeout=timeout):
	line=iq.get()
	ip=line.split(':')[0].strip('\n')
	port=line.split(':')[1].strip('\n')
	try:
		#print "ip:%s,port:%s"% (ip,port)
		cs=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		cs.settimeout(float(timeout))
		address=(str(ip),int(port))
		status=cs.connect_ex(address)
		if status == 0:
			print "host:%s port:%s ok" % (ip,port)
			iq.task_done()
			#print inGreen("host:%s port:%s ok" % ip,port)
		else:
			print "host:%s port:%s down" % (ip,port)
			iq.task_done()
			return 0
			
	except Exception,e:
		#print inRed("error:%s" % ip)
		print "error:%s" % e
		return 1
		iq.task_done()
	except KeyboardInterrupt:
		print "You pressed Ctrl+c"
		sys.exit()

file = raw_input("Enter the file to check the services:")
f = open(file,'r')

#place ip into ip_queue
for eachline in f:
	ip_queue.put(eachline)

f.close()
#spawn pool of scan_port threads
num_threads = ip_queue.qsize()
for i in range(num_threads):
	worker = Thread(target=scan_port,args=(ip_queue,5))
	worker.setDaemon(True)
	worker.start()

print "Main Thread waiting"
ip_queue.join()
print "Done"
