#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import requests
import argparse

reload(sys)  
sys.setdefaultencoding('utf8')  

def check_ip_location(ip):
	url = 'http://apis.baidu.com/apistore/iplookupservice/iplookup?ip=%s' % ip
	headers = {'apikey':"82daebb3d355823f09432a5213f41bf1"}
	try:
		page_content = requests.get(url,headers=headers,timeout=3).text.encode('utf8')
		content = json.loads(page_content)
		print u'ip:%s,conuntry:%s,provice:%s,city:%s,district:%s,isp:%s' % (content['retData']['ip'],content['retData']['country'],content['retData']['province'],content['retData']['city'],content['retData']['district'],content['retData']['carrier'])
	except:
		print "error check ip "

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Check ip location')
	parser.add_argument('--ip',action="store",dest='ip',default='4.4.4.4')

	given_args = parser.parse_args()

	check_ip_location(given_args.ip)
