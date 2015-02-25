#!/usr/bin/env python
#coding:utf-8
#joey -20150225
#refer:https://github.com/yangbh/Hammer/blob/master/plugins/System/mongodb_unauth_access.py
#http://linux.im/2014/12/11/mongodb_unauthorized_access_vulnerability_global_probing_report.html

import pymongo
import sys
from threading import Thread
from Queue import Queue
#from IPy import IP
#from dummy import * 

ip_queue = Queue()
out_queue = Queue()
nmu_threads = 100


def Audit(q,port):
	while True:
		ip = q.get()
		try:
			connection = pymongo.MongoClient(ip,port,socketTimeoutMS=3000)
			# connection.api.authenticate("root","1234")
			# db = connection.admin
			# db.system.users.find_one()
			dbs = connection.database_names()
			#security_hole(ip+':'+str(port)+'/'+str(dbs))
			#logger(ip + ':' + str(port)+'/'+str(dbs))
			if dbs:
				print ip,port
				print dbs
				out_queue.put(ip)
				q.task_done()

		except pymongo.errors.OperationFailure,e:
			#logger('Exception:\t'+str(e))
			print "mongo error is:%s" % e
			q.task_done()
		except Exception,e:
			print "error is:%s" % e
			q.task_done()
			
		except KeyboardInterrupt:
			print "You pressed Ctrl+c"
			sys.exit()
			# pass


if __name__=='__main__':
	file = raw_input("Enter the file to check: ")
	port = int(raw_input("Enter the port to check: "))
	f = open(file,'r')
	ips = []
	for eachline in f:
		ip_queue.put(eachline.strip())

	#spawn pool of scan_port threads
	if ip_queue.qsize() < num_threads:
		num_threads = ip_queue.qsize()

	
	for i in range(num_threads):
		worker = Thread(target=Audit,args=(ip_queue,port))
		worker.setDaemon(True)
		worker.start()

	print "Main Thread waiting"
	ip_queue.join()

	print "Done"


