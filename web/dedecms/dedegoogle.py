#!/usr/bin/env python
#coding=utf-8

#http://hi.baidu.com/lxai6/item/47c5bda45d6cf25a6cd455b5

import urllib2,urllib,threading,Queue,os
#import msvcrt
import simplejson
import sys

searchstr = raw_input("key:")
pagenum = 6
print "search txt:%s" % searchstr
#pagenum = raw_input("how many:")
pagenum = int(pagenum)/8+1
line =5 

class googlesearch(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.urls=[]

    def run(self):
        while 1:
            self.catchURL()
            queue.task_done()

    def catchURL(self):
        self.key = searchstr.decode('gbk').encode('utf-8')
        self.page = str(queue.get())
        url = ('https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s&rsz=8&start=%s') % (urllib.quote(self.key),self.page)
        #print "url is:%s" % url
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            results = simplejson.load(response)
            URLinfo = results['responseData']['results']
        except Exception,e:
            print e
        except KeyboardInterrupt:
            os.exit(1)
        else:
            for info in URLinfo:
                print info['url']
                open('list.txt','a').write('%s' % info['url'])

class ThreadGetKey(threading.Thread):
    def run(self):
        while 1:
            try:
                chr ='d'
                #chr = msvcrt.getch()
                if chr == 'q':
                    print "stopped by your action (q)"
                    os._exit(1)
                else:
                    continue
            except KeyboardInterrupt:
                os.exit(1)

if __name__=='__main__':
    pages=[]
    queue = Queue.Queue()

    for i in range(1,pagenum+1):
        pages.append(i)

    for n in pages:
        print n
        queue.put(n)

    #ThreadGetKey().start()

    for p in range(line):
        googlesearch().start()
