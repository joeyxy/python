#!/usr/bin/env python
#create at:20131125 joey joeyxy83@gmail.com
#for check the server services ports
#file format in each line: ip

#import time
#import socket,re,urllib,urllib2,os,sys
#import subprocess
import socket
from threading import Thread
from Queue import Queue
from termcolor import colored

timeout = 5
ip_queue = Queue()
port_queue = Queue()
num_threads = 100 


def scan_port(ip1,port,timeout=timeout):
	while True:
		line=port.get()
		ip=ip1
		try:
			cs=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			cs.settimeout(float(timeout))
			address=(str(ip),int(port))
			status=cs.connect_ex(address)
			if status == 0:
				print colored("host:%s port:%s open" % (ip,port),'green')
			#else:
				#print colored("host:%s port:%s close" % (ip,port),'red')
			
		except Exception,e:
			print "error:%s" % e
		except KeyboardInterrupt:
			print "You pressed Ctrl+c"
			sys.exit()

		port.task_done()
file = raw_input("Enter the file to check the services:")
f = open(file,'r')

#place ip into ip_queue
for eachline in f:
	ip = eachline.strip('\n')
	for port in range(1,1025):
		port_queue.put(eachline)
	if port_queue.qsize() < num_threads:
		num_threads = port_queue.qsize()
	for i in range(num_threads):
		worker = Thread(target=scan_port,args=(ip,port_queue,5))
		worker.setDaemon(True)
		worker.start()

f.close()


print "Main Thread waiting"
port_queue.join()
print "Done"
