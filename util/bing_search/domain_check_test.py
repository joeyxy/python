#!/usr/bin/env python

import re
import requests

ip = raw_input("input ip for check: ")
r = requests.get('http://www.bing.com/search?q=ip:'+ip+'&count=50')
responseHtml = r.content
match = re.findall(r'<li class=\"b_algo\"><h2><a href=\"(.*?)\"', responseHtml)

for val in match:
	print val