#!/usr/bin/env python

import urllib2
import re
from BeautifulSoup import BeautifulSoup

def main():
	weatherurl="http://pm25.in/chengdu"
	req = urllib2.Request(weatherurl)
	resp = urllib2.urlopen(req)
	resphtml = resp.read()
	#print "resphtml=",resphtml
	#<td></td>
	foundcity = re.search('<td class.*>(?P<city>.+?)</td>',resphtml)
	print "foundcity=",foundcity
	if(foundcity):
		city = foundcity.group("city")
		print "city=",city
	
	print "method 2:use the beautifulsoup"
	songtasteHtmlEncoding = "GB2312"
	soup = BeautifulSoup(resphtml,fromEncoding=songtasteHtmlEncoding)	
	foundclasscity = soup.find(attrs={"td class":"03_8h_dn"})
	print "foundclasscity",foundclasscity
	if (foundclasscity):
		citystr = foundclasscity.string
		print "citrystr",citystr



if __name__=="__main__":
	main();
