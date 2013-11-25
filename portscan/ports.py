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
num_threads = 100 


def scan_port(iq,timeout=timeout):
	while True:
		line=iq.get()
		ip=line.split(':')[0].strip('\n')
		for port in range(1,1025):
			#line=iq.get()
  			#ip=line.split(':')[0].strip('\n')
			#port=line.split(':')[1].strip('\n')
			try:
				#print "ip:%s,port:%s"% (ip,port)
				cs=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				cs.settimeout(float(timeout))
				address=(str(ip),int(port))
				status=cs.connect_ex(address)
				if status == 0:
					print colored("host:%s port:%s ok" % (ip,port),'green')
				else:
					print colored("host:%s port:%s down" % (ip,port),'red')
			
			except Exception,e:
				print "error:%s" % e
			except KeyboardInterrupt:
				print "You pressed Ctrl+c"
				sys.exit()

		iq.task_done()
file = raw_input("Enter the file to check the services:")
f = open(file,'r')

#place ip into ip_queue
for eachline in f:
	ip_queue.put(eachline)

f.close()
#spawn pool of scan_port threads
if ip_queue.qsize() < num_threads:
	num_threads = ip_queue.qsize()

	
for i in range(num_threads):
	worker = Thread(target=scan_port,args=(ip_queue,5))
	worker.setDaemon(True)
	worker.start()

print "Main Thread waiting"
ip_queue.join()
print "Done"
