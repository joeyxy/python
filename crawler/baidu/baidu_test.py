#!/usr/bin/env python

# coding=utf8
import string, urllib2

def baidu_tieba(url,begin_page,end_page):   
    for i in range(begin_page, end_page+1):
        sName = string.zfill(i,5) + '.html'
		print 'down' + str(i) + 'web page,store as:' + sName + '......'
        f = open(sName,'w+')
        m = urllib2.urlopen(url + str(i)).read()
        f.write(m)
        f.close()


#ex url:http://tieba.baidu.com/p/2296017831?pn=

bdurl = str(raw_input('input the url:\n'))
begin_page = int(raw_input('input the start page:\n'))


end_page = int(raw_input('input the end page:\n'))

baidu_tieba(bdurl,begin_page,end_page)

