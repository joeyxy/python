#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import urllib

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getImage(html):
    reg = r'src="(http://imgsrc.*.jpg)" width'
    #reg = r'src=\'#\'" width'
    imgre = re.compile(reg)
    imagelist = imgre.findall(html)
    x = 0
    for imageurl in imagelist:
        print "img url:%s" % imageurl
        urllib.urlretrieve(imageurl,'pic_%s.jpg' % x)
        x +=1

uri = raw_input("input url:\n")
r = r'^http://'

if re.match(r,uri):
    html2 = getHtml(uri)
else:
    html2 = getHtml("http://"+uri)

getImage(html2)
