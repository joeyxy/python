#!/usr/bin/env python
#test re to get the char

import urllib2;
import re;

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

if __name__=="__main__":
	main();
