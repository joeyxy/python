#!/usr/bin/python
#-*-coding:utf-8-*-
import urllib2,urlib
import simplejson
import os,time,threading
import common,html_filter

keywords = raw_input('Enter the keywords: ')

rnum_perpage=8
pages=8

def thread_scratch(url,rnum_perpage,page):
    
