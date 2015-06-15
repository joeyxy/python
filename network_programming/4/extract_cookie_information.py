#!/usr/bin/env python

import cookielib
import urllib
import urllib2

ID_USERNAME = 'id_username'
ID_PASSWORD = 'id_password'
USERNAME = ''
PASSWORD = ''
LOGIN_URL = 'https://bitbucket.org/account/signin/?next=/'
NORMAL_URL = 'https://bitbucket.org/'


def extract_cookie_info():
	cj = cookielib.CookieJar()
	login_data = urllib.urlencode({ID_USERNAME:USERNAME,ID_PASSWORD:PASSWORD})

	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	resp = opener.open(LOGIN_URL,login_data)

	for cookie in cj:
		print "----First time cookie:%s-->%s" % (cookie.name,cookie.value)

	print "Headers:%s" % resp.headers


	resp = opener.open(NORMAL_URL)

	for cookie in cj:
		print "+++second time cookie:%s-->%s" % (cookie.name,cookie.value)

	print "Headers: %s" % resp.headers 

if __name__ == '__main__':
	extract_cookie_info()