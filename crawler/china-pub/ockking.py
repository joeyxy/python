#!/usr/bin/env python
####
# Copyright (c) 2009 - 2014, Aven's Lab. All rights reserved.
#                     http://www.ocrking.com
# DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS FILE HEADER.
# Id: OcrKing.py,v 0.1 2014/10/29 23:40:18 
# The Python script for OcrKing Api
# By Aven <Aven@OcrKing.Com>
# Welcome to follow us 
# http://weibo.com/OcrKing
# http://t.qq.com/OcrKing
# Warning! 
# Before running this script , you should modify some parameter
# within the post data according to what you wanna do
# To run it manually,just type  python OcrKing.py
# the result will be shown soon
# Just Enjoy The Fun Of OcrKing !
####

# version for Python OcrKing Client #
__version__ = '0.1'
# version for Python OcrKing Client #

# OcrKing Api Url #
__api_url__ = 'http://lab.ocrking.com/ok.html'
# OcrKing Api Url #

### libs need to import ###
import urllib2
import httplib
from xml.etree import ElementTree
### libs need to import ###

### just fix some known bug of Python , ignore this please ###
httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'
### just fix some known bug of Python , ignore this please ###

### post data with file uploading ###
def post_multipart(fields, files):
	content_type, body = encode_multipart(fields, files)
	headers = {'Content-Type': content_type,
	'Content-Length': str(len(body)),
	'Accept-Encoding': 'gzip, deflate',
	'Referer': 'http://lab.ocrking.com/?pyclient' + __version__,
	'Accept':'*/*'}
	r = urllib2.Request(__api_url__, body, headers)
	return urllib2.urlopen(r).read()

### format the data into multipart/form-data ###	
def encode_multipart(fields, files):
	LIMIT = '----------OcrKing_Client_Aven_s_Lab_L$'
	CRLF = '\r\n'
	L = []
	for (key, value) in fields:
		L.append('--' + LIMIT)
		L.append('Content-Disposition: form-data; name="%s"' % key)
		L.append('')
		L.append(value)
	for (key, filename, value) in files:
		L.append('--' + LIMIT)
		L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
		L.append('Content-Type: application/octet-stream' )
		L.append('')
		L.append(value)
	L.append('--' + LIMIT + '--')
	L.append('')
	body = CRLF.join(L)
	content_type = 'multipart/form-data; boundary=%s' % LIMIT
	return content_type, body

def print_node(node):
    print "====="
    for key,value in node.items():
        print "%s:%s" % (key, value)
    for subnode in node.getchildren():
        if subnode.tag == 'Result':
            print "%s:%s" % (subnode.tag, subnode.text)
        if subnode.tag == 'Status':
            print "%s:%s" % (subnode.tag, subnode.text)        
        #print "%s:%s" % (subnode.tag, subnode.text)

def read_xml(text = '', xmlfile = ''):
    root = ElementTree.fromstring(text)
    eitor = root.getiterator("Item")
    for e in eitor:
        print_node(e)

# replace the word KEY below with your apiKey obtained by Email #	
key = 'def1e763f8ebc690cbubfgyKfTjB0MI1egCtrNt4hJNBlxyCRy1bptAc65x1VhI0dCcwTL'
# you need to specify the full path of image you wanna OCR #
# e.x. D:\\Program Files\\004.png #
image = open('./pic/1427617687.png', "rb") 
# you need to modify the filename according to you real filename #
# e.x 004.png #
file = [('ocrfile','1427617687.png',image.read())]
#file = []
# you need to modify parameters according to OcrKing Api Document #
fields = [('url','http://www.china-pub.com/member/register/imgchk/validatecode.asp'),('service', 'OcrKingForCaptcha'),('language','eng'),('charset','7'),('apiKey', key),('type','http://www.china-pub.com/member/register/imgchk/validatecode.asp')]
# just fire the post action #
xml = post_multipart(fields,file)

read_xml(xml)
#print xml