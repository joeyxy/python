#!/usr/bin/env python
#coding=utf-8
import requests,json,urllib,sys,os
from bs4 import BeautifulSoup
import socket
import time
import re
import threadpool as tp
from IPy import IP

global port
global dede_res 

'''
IP reverse class 
demo:
get 202.20.2.1 domain list
ipre = IPReverse();
ipre.getDomainsList('202.20.2.1')
'''
class IPReverse():
	#get the page content
	def getPage(self,ip,page):
	    r = requests.get("http://dns.aizhan.com/index.php?r=index/domains&ip=%s&page=%d" % (ip,page))
	    return r

	#get the max page
	def getMaxPage(self,ip):
	    r = self.getPage(ip,1)
	    json_data = {}
	    json_data = r.json()
	    if json_data == None:
	    	return None
	    maxcount = json_data[u'conut']
	    maxpage = int(int(maxcount)/20) + 1    
	    return maxpage

	#get the domain list
	def getDomainsList(self,ip):
	    maxpage = self.getMaxPage(ip)
	    if maxpage == None:
	    	return None
	    result = []
	    for x in xrange(1,maxpage+1):
	        r = self.getPage(ip,x)
	        result.append(r.json()[u"domains"])
	    return result

'''
check DEDEcms
1.robots.txt
2.check the html Powered by 
'''
class DetectDeDeCMS():
	#check robots.txt
	def detectingRobots(self,url):
		robots_content = ("Disallow: /plus/feedback_js.php" or "Disallow: /plus/mytag_js.php"
		or "Disallow: /plus/rss.php" or "Disallow: /plus/search.php" or "Disallow: /plus/recommend.php"
		or "Disallow: /plus/stow.php" or "Disallow: /plus/count.php")
		robots_url = "%s/%s" % (url,'robots.txt')
		robots_page = requests.get(robots_url,timeout=3)
		if robots_page.status_code != 200:
			return False
		content = robots_page.content
		if content.count(robots_content) != 0:
			return True
		else:
			return False

	#powered by dede detect
	def detectingPoweredBy(self,raw_page):		
		pattern = re.compile(r'DedeCMS.*?')
		try:
			soup = BeautifulSoup(raw_page)
			text = soup.a.text
		except Exception, e:
			return False
		if pattern.findall(text) != []:
			return True
		else:
			return False

	def getResult(self,url):
		url = 'http://%s' % url
		try:
			r = requests.get(url,timeout=3)
			raw_page = r.content
			#print raw_page
		except Exception, e:
			return False
		if (not r) or (r.status_code != 200) or (not raw_page):
			return False
		is_robots_exists = self.detectingRobots(url)
		is_poweredby_exists = self.detectingPoweredBy(raw_page)
		if is_poweredby_exists or is_robots_exists:
			return True
		else:
			return False


def portScanner(ip):
	global port
	server = (ip,port)
	sockfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sockfd.settimeout(0.8)
	ret = sockfd.connect_ex(server)  #return is sucess
	if not ret:
	    sockfd.close()
	    print '%s:%s is opened...' % (ip,port)
	    return True
	else:
	    sockfd.close()
	    return False


def step(args):
	global dede_res
	dede_res = []
	ip = args
	if portScanner(ip):
		ipreverse = IPReverse()
		dededetector = DetectDeDeCMS()
		domain_list = []
		tmp_list = []
		tmp_list = ipreverse.getDomainsList(ip)
		if tmp_list != None:
			domain_list = domain_list + tmp_list
			#print "domain number:%s" % len(domain_list)
			for x in domain_list:
				for i in x:
					print i 
					if dededetector.getResult(i):
						dede_res.append(i)
		



if __name__ == '__main__':
	begin = time.time()
	dede_res = []
	#myworker = Worker('219.235.5.52','219.235.5.52')
	#if len(sys.argv) != 3:
	#	print "usage: %s ip1 ip2" % sys.argv[0]
	#	sys.exit(1)
	#ip1 = sys.argv[1]
	#ip2 = sys.argv[2]
	ips =IP(raw_input('input ip list: '))
	port = int(raw_input('input the check port: '))
	args=[]
	for ip in ips:
		args.append(str(ip))
	pool = tp.ThreadPool(50)
	reqs = tp.makeRequests(step,args)
	[pool.putRequest(req) for req in reqs]
	pool.wait()
	current = time.time() - begin
	print 'Cost :%s' % str(current)
	if dede_res == []:
		print 'can not find the result'
	else:
		print  'the result is:' , dede_res
