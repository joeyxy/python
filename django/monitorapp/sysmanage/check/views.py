#from django.shortcuts import render
from django.shortcuts import render_to_response
#import  xmjx_chachepai as cha
import requests
import json
import sys
import argparse
import hashlib
import re
# Create your views here.


def cp(request):
	error = False
	if 'cp' in request.GET:
		cp = request.GET['cp']
		if not cp:
			#error = True
			return render_to_response('cp_form.html')
		else:
			burp = check_chepai(user='13908011116',pwd='111111',chepai=cp)
			(result1,result2,result3,result4,result5)=burp.check_one()
			if result1:
				return render_to_response('cp_results.html',{'result1':result1,'result2':result2,'result3':result3,'result4':result4,'result5':result5,'cp':cp})
			else:
				return render_to_response('cp_form.html',{'error':error})


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



	def check_one(self):
		if (self.login() == 0):
			api_url = 'http://www.xmxing.net/wap/car_details.php?hpzl=02&hphm=%s' % self.cp
			cookies = {'PHPSESSID':self.cookie}
			try:
				req = requests.get(api_url,headers=self.headers,cookies = cookies,timeout=3)
				#print req.content
				pattern = re.compile('<div style="float:left;text-align:left;width:65%">(.*?)</div>',re.S)
				items = re.findall(pattern, req.content)
				print "chepai:%s,car type:%s,color:%s,user:%s,tel:%s " % (items[1],items[3],items[4],items[14],items[15])
				return items[1],items[3],items[4],items[14],items[15]
				#return "%s,%s,up" % (ip,port)
			except requests.RequestException as e:
				print "request error:%s" % e
				pass
			except :
				pass