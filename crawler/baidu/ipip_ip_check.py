#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import requests
import argparse

reload(sys)  
sys.setdefaultencoding('utf8')  

def check_ip_location(ip):
	url = 'http://freeapi.ipip.net/?ip=%s' % ip
	try:
		page_content = requests.get(url,timeout=3).text.encode('utf8')
		content = json.loads(page_content)
		print u'conuntry:%s,provice:%s,city:%s,isp:%s' % (content[0],content[1],content[2],content[4])
	except:
		print "error check ip "

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Check ip location')
	parser.add_argument('--ip',action="store",dest='ip',default='4.4.4.4')

	given_args = parser.parse_args()

	check_ip_location(given_args.ip)