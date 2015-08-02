#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import requests
import argparse

reload(sys)  
sys.setdefaultencoding('utf8')  

def check_ip_location(city):
	url = 'http://apis.baidu.com/apistore/aqiservice/aqi?city=%s' % city
	headers = {'apikey':"82daebb3d355823f09432a5213f41bf1"}
	try:
		page_content = requests.get(url,headers=headers,timeout=3).text.encode('utf8')
		content = json.loads(page_content)
		print u'city:%s,aqi:%s,level:%s,core:%s' % (content['retData']['city'],content['retData']['aqi'],content['retData']['level'],content['retData']['core'])
	except:
		print "error check ip "

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Check ip location')
	parser.add_argument('--city',action="store",dest='city',default='成都')

	given_args = parser.parse_args()

	check_ip_location(given_args.city)
