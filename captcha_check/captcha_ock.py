#!/usr/bin/env python 
#check the pic number
#joeyxy83@gmail.com
#20150628

import os 
import re
import time
import json
import urllib
import urllib2
import requests
import pytesseract
from PIL import Image
import httplib
from xml.etree import ElementTree
import argparse

__version__ = '0.1'
# version for Python OcrKing Client #

# OcrKing Api Url #
#get api url:http://api.ocrking.com/server.html
__api_url__ = 'http://39.65.100.4:6080/ok.html'

#httplib.HTTPConnection._http_vsn = 10
#httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'


def downloadImg(pic_url):
    if os.path.exists('./pic/'):
        pass
    else:
        os.makedirs('./pic/')
    pic_file = int(time.time())
    print '[+] Download Picture: {}'.format(pic_url)
    try:
        resp = requests.get(pic_url, verify=False, timeout=5)
    except:
        resp = requests.get(pic_url, verify=False, timeout=3)
    with open("./pic/%s.png"%pic_file, 'wb') as fp:
        fp.write(resp.content)
    return pic_file



def post_multipart(fields, files):
    content_type, body = encode_multipart(fields, files)
    httplib.HTTPConnection._http_vsn = 10  #must using the http 1.0
    httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'
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


def check_code(url):
    pic_file = downloadImg(url)
    #print pic_file
    file = str(pic_file)+'.png'
    path = './pic/'+file
    key = 'def1e763f8ebc690cbubfgyKfTjB0MI1egCtrNt4hJNBlxyCRy1bptAc65x1VhI0dCcwTL'
    #print file,path
    image = open(path, "rb") 
    file = [('ocrfile',file,image.read())]
    fields = [('url',url),('service', 'OcrKingForCaptcha'),('language','eng'),('charset','11'),('apiKey', key),('type',url)]
    xml = post_multipart(fields,file)
    read_xml(xml)
    #print xml


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='input the captcha url ')
	parser.add_argument('--url',action="store",dest="url")

	given_args = parser.parse_args()
	url = given_args.url
	check_code(url)



