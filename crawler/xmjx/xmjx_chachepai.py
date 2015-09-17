#!/usr/bin/env python

#login to check the chepai user
#joeyxy83@gmail.com

import requests
import json
import sys
import argparse
import hashlib
import re


class check_chepai(object):
	def __init__(self,user,pwd,chepai):
		self.user = user
		self.pwd  = str(pwd)
		self.cp = chepai
		self.cookie = ''
		self.headers = {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H143',}
	
	def login(self):
		key = hashlib.sha256(self.pwd).hexdigest()
		api_url = 'http://www.xmxing.net/wap/bind_info.php?phone=%s&pass=%s' %(self.user,key)
		try:
			req = requests.get(api_url,headers=self.headers,timeout=3)
			#print req.content
			self.cookie = req.cookies['PHPSESSID']
			print self.cookie
			return 0
		except requests.RequestException as e:
			print "request error:%s" % e
			return 1
		#if json.loads(req.content)['state'] == 'false':
		#	return 1
		#else:
		#	self.cookie = req.cookie['PHPSESSID']
		#	print "get cookie:%s" % self.cookie
		#	return 0

	def check(self):
		if (self.login() == 0):
			while 1:
				cp = raw_input("input chepai or quit: ")
				if cp == 'quit':
					sys.exit(1)
				api_url = 'http://www.xmxing.net/wap/car_details.php?hpzl=02&hphm=%s' % cp
				cookies = {'PHPSESSID':self.cookie}
				try:
					req = requests.get(api_url,headers=self.headers,cookies = cookies,timeout=3)
					#print req.content
					pattern = re.compile('<div style="float:left;text-align:left;width:65%">(.*?)</div>',re.S)
					items = re.findall(pattern, req.content)
					print "chepai:%s,car type:%s,color:%s,user:%s,tel:%s " % (items[1],items[3],items[4],items[14],items[15])
				except requests.RequestException as e:
					print "request error:%s" % e




if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="check for chepai")
	parser.add_argument('--mobile',action="store",dest="mobile",type=int,default='13908011116')
	parser.add_argument('--passwd',action="store",dest="passwd",type=int,default='111111')
	parser.add_argument('--chepai',action="store",dest="chepai",default='A11111')
	given_args = parser.parse_args()
	mobile = given_args.mobile
	pwd = given_args.passwd
	chepai = given_args.chepai

	burp = check_chepai(user=mobile,pwd=pwd,chepai=chepai)
	burp.check()