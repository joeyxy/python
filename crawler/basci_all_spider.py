#!/usr/bin/env python
#test re to get the char

import urllib2;
import re;
from BeautifulSoup import BeautifulSoup

def main():
	userMainUrl="http://www.songtaste.com/user/351979/"
	req = urllib2.Request(userMainUrl);
	resp = urllib2.urlopen(req);
	respHtml = resp.read();
	print "respHtml=",respHtml
	#<h1 class="h1user">crifan</h1>
	foundH1user = re.search('<h1\s+?class="h1user">(?P<h1user>.+?)</h1>',respHtml)
	print "foundH1user=",foundH1user;
	if(foundH1user):
		h1user = foundH1user.group("h1user")
		print "h1user=",h1user;


	print "method 2: use the python BeautifulSoup"
	songtasteHtmlEncoding = "GB2312"
	soup = BeautifulSoup(respHtml,fromEncoding=songtasteHtmlEncoding);
	foundClassH1user = soup.find(attrs={"class":"h1user"})
	print "foundClassH1user=%s" % foundClassH1user
	if(foundClassH1user):
		h1userStr = foundClassH1user.string
		print "h1userStr=",h1userStr;

if __name__=="__main__":
	main();
