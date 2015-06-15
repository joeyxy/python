#!/usr/bin/env python

import urllib2

BROWSER = 'Mozilla/5.0 (Windows NT 5.1;rv:20.0) Gecko/20100101 Firefox/20.0'
URL = 'http://www.python.org'


def spoof_firefox():
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent',BROWSER)]
	result = opener.open(URL)
	print "Response headers:"
	for header in result.headers.headers:
		print "\t",header

if __name__ == '__main__':
	spoof_firefox()