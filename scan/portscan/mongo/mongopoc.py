#!/usr/bin/env python
#coding:utf-8
#joey -20150225 joeyxy83@gmail.com
#refer:https://github.com/yangbh/Hammer/blob/master/plugins/System/mongodb_unauth_access.py
#http://linux.im/2014/12/11/mongodb_unauthorized_access_vulnerability_global_probing_report.html

import pymongo
import sys
#from IPy import IP
#from dummy import * 



def Audit(services):
	ip = services['ip']
	port = services['ports']
	if port:
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

		except pymongo.errors.OperationFailure,e:
			logger('Exception:\t'+str(e))
		except Exception,e:
			print "error is:%s" % e
			#pass
		except KeyboardInterrupt:
			print "You pressed Ctrl+c"
			sys.exit()
			# pass


if __name__=='__main__':
	#ips =IP(raw_input('input ip list: '))
	file = raw_input("Enter the file to check: ")
	port = int(raw_input("Enter the port to check: "))
	f = open(file,'r')
	ips = []
	for eachline in f:
		ips.append(eachline.strip())
	for ip in ips:
		services = {'ip':ip,'ports':port}
		Audit(services)
		#print(services)