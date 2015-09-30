#!/usr/bin/env python
#create at:20150225 joey joeyxy83@gmail.com
#for check the port status,and create the check list :ip.list
#input format ip : 192.168.10.0/32 
#port : 27017


import socket
from threading import Thread
from Queue import Queue
from termcolor import colored
from IPy import IP
import time 

timeout = 5
ip_queue = Queue()
out_queue = Queue()
num_threads = 100 


def scan_port(iq,port,timeout=timeout):
	while True:
		ip=iq.get()
		try:
			#print ip 
			#print "ip:%s,port:%s"% (ip,port)
			cs=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			cs.settimeout(float(timeout))
			address=(str(ip),int(port))
			status=cs.connect_ex(address)
			if status == 0:
				#print colored("host:%s port:%s ok" % (ip,port),'green')
				out_queue.put(ip)
				iq.task_done()
			else:
				#print colored("host:%s port:%s down" % (ip,port),'red')
				iq.task_done()
			
		except Exception,e:
			print "error:%s" % e
			iq.task_done()
		except KeyboardInterrupt:
			print "You pressed Ctrl+c"
			sys.exit()

def print_result(q,file):

	while True:
		out = q.get()
		print out
		file.write(out+'\n')
		if q.empty():
			break
		


ips =IP(raw_input('input ip list: '))
port = raw_input('input the check port: ')


#place ip into ip_queue
for ip in ips:
	ip_queue.put(str(ip))

#spawn pool of scan_port threads
if ip_queue.qsize() < num_threads:
	num_threads = ip_queue.qsize()

	
for i in range(num_threads):
	worker = Thread(target=scan_port,args=(ip_queue,port,5))
	worker.setDaemon(True)
	worker.start()

print "Main Thread waiting"
ip_queue.join()

print "Done"
file = time.strftime("%y-%m-%d-%H-%M.") + 'ip.list'
f = open(file,'w')
print_result(out_queue,f)
f.close()