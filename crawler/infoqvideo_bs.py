#!/usr/bin/env python
#coding=utf-8

import re,sys
import urllib2
from Queue import Queue
from threading import Thread
from time import strftime
from BeautifulSoup import BeautifulSoup 
import codecs

reload(sys) 
sys.setdefaultencoding('utf8')   

baseUrl='http://www.infoq.com/cn/presentations/'
outPut='bsvideolist.html'
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
        #sres=urlopen(url)
    except Exception,e:
        print '[-] [%s] [Error] [%s]'
	print "url:%s" % url
    if res.getcode()==200:
        html=res.read()
        soup=BeautifulSoup(html)
        resp = soup.findAll('div',attrs = {'class':"news_type_video "})
        for i in xrange(len(resp)):
            title = resp[i].contents[3].text
            url = "http://www.infoq.com"
            time = resp[i].contents[1].text
            desc = resp[i].contents[7].text
            #print title,desc
            urlNum+=1
            urlList.append("<a href=\""+url+"\">"+title+":"+time+"desc:"+desc+"</a>")
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
            #print _url
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

    #f=codecs.open(outPut,'a','utf-8')
    f=open(outPut,'a')
    f.write('<html> <head> <meta http-equiv="Content-Type" content="text/html" charset=utf-8> \n')
    f.write('<title>infoq video List</title></head>\n')
    f.write('<body>\n')
    f.write('<center><h1><b>infoq video List</b></h1>\n'+'Time:'+str(strftime("%Y-%b-%d %X"))+'Count:'+str(len(urlList))+'</center><hr/>\n<h5>\n')
    for line in urlList:
        #print line
        f.write(line+'</br>\n')
    f.write('</body></html>\n')
    f.close()

    print '\n[+] [%s] [End] [All Done!]'%strftime('%X')
    print '[+] [%s] [Save As] [%s]'%(strftime('%X'),outPut)


if __name__=='__main__':
    main()
