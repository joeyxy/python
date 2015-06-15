#!/usr/bin/env python

import urllib
import urllib2
import re

class BDTB:
	def __init__(self,baseUrl,seeLZ):
		self.baseUrl = baseUrl
		self.seeLZ = '?see_lz='+str(seeLZ)

	def getPage(self,pageNum):
		try:
			url = self.baseUrl+self.seeLZ+'&pn='+str(pageNum)
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			print response.read()
			return response
		except urllib2.URLError,e:
			if hasattr(e, "reason"):
				print "error:",e.reason
				return None

baseURL = 'http://tieba.baidu.com/p/3138733512'
bdtb = BDTB(baseURL, 1)
bdtb.getPage(1)