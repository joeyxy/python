#!/usr/bin/env python
#coding=utf-8

import re,sys
from urllib import urlopen
from Queue import Queue
from threading import Thread
from time import strftime
import urllib2

baseUrl='http://www.infoq.com/cn/presentations/'
outPut='videolist.html'
pageNum=822
threadNum=50
urlList=[]
threadList=[]
urlNum=0

def spiderIndex(url):
    global urlNum

    try:
        req = urllib2.Request(url=url)
        res = urllib2.urlopen(req,timeout=5)
        #res=urlopen(url)
    except Exception,e:
        print '[-] [%s] [Error] [%s]'
	print "url:%s" % url
    if res.getcode()==200:
        html=res.read()
        lines=html.split('\n')
        for line in lines:
            #rex=re.search(r'(<a href=\")(/cn/presentations/\w*)(\" title=\".*\">).*',line)
            #rex=re.search(r'(<a href=\")(/cn/presentations/\w*)',line)
            #http://www.infoq.com/
            rex=re.search(r'(<a href=\")(/cn/presentations/\w*.*)(#theCommentsSection)',line)


            if rex !=None:
                urlNum+=1
                urlList.append(rex.group(1)+"http://www.infoq.com"+rex.group(2)+"\">"+rex.group(2)+"</a>")
                sys.stdout.write('\r[*] [%s] [Working] [%s]'%(str(strftime('%X')),str(urlNum)))


class WorkThread(Thread):

    def __init__(self,q):
        Thread.__init__(self)
        self.q=q

    def run(self):
        while True:
            if self.q.empty()==True:
                break
            _url=baseUrl+str(self.q.get())
            print _url
            spiderIndex(_url)
            self.q.task_done()


def main():
    q=Queue(maxsize=0)
    for i in xrange(1,pageNum,1):
        q.put(i)

    print '[+] [%s] [Start]'%strftime('%X')

    #spiderIndex('http://www.freebuf.com/tools')

    for i in xrange(threadNum):
        t=WorkThread(q)
        threadList.append(t)

    for i in threadList:
        i.start()

    for i in threadList:
        i.join()

    f=open(outPut,'ab')
    f.write('<html> <meta http-equiv="Content-Type" content="text/html";charset=utf-8 />\n')
    f.write('<title>infoq video List</title>\n')
    f.write('<body>\n')
    f.write('<center><h1><b>infoq video List</b></h1>\n'+'Time:'+str(strftime("%Y-%b-%d %X"))+'Count:'+str(len(urlList))+'</center><hr/>\n<h5>\n')
    for line in urlList:
        f.write(line+'</br>\n')
    f.write('</body></html>\n')
    f.close()

    print '\n[+] [%s] [End] [All Done!]'%strftime('%X')
    print '[+] [%s] [Save As] [%s]'%(strftime('%X'),outPut)


if __name__=='__main__':
    main()
