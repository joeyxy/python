#-------------------------------------------------------------------------------
# Name:        weibo
# Purpose:
#
# Author:      adrain
#
# Created:     14/02/2015
# Copyright:   (c) adrain 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sys
import requests
import re
import base64
import urllib
import rsa
import binascii
import os
import json


class weibo():

    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8&')

    def weibo_login(self,nick,pwd):
        print u'---weibo login----'
        pre_login_url='http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.15)&_=1400822309846' % nick
        pre_logn_data=requests.get(pre_login_url).text;
        #print pre_logn_data
        servertime=re.findall('"servertime":(.*?),',pre_logn_data)[0]
        pubkey = re.findall('"pubkey":"(.*?)",' , pre_logn_data)[0]
        rsakv = re.findall('"rsakv":"(.*?)",' , pre_logn_data)[0]
        nonce = re.findall('"nonce":"(.*?)",' , pre_logn_data)[0]

        login_url='http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'

        su=base64.b64encode(urllib.quote(self.nick))

        rsaPublickey= int(pubkey,16)
        key = rsa.PublicKey(rsaPublickey,65537)
        message = str(servertime) +'\t' + str(nonce) + '\n' + str(self.pwd)
        sp = binascii.b2a_hex(rsa.encrypt(message,key))

        post_data={
                    'entry': 'weibo',
                    'gateway': '1',
                    'from': '',
                    'savestate': '7',
                    'userticket': '1',
                    'pagereferer':'',
                    'vsnf': '1',
                    'su': su,
                    'servertime': servertime,
                    'nonce': nonce,
                    'pwencode': 'rsa2',
                    'rsakv' : rsakv,
                    'sp': sp,
                    'encoding': 'UTF-8',
                    'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
                    'returntype': 'META',
                    'ssosimplelogin': '1',
                    'vsnval': '',
                    'service': 'miniblog',
                    }

        header = {'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'}

        login_data=requests.post(login_url,data=post_data,headers=header).text.decode("utf-8").encode("gbk",'ignore')

        try:
            suss_url=re.findall("location.replace\(\'(.*?)\'\);" , login_data)[0]
            login_cookie=requests.get(suss_url).cookies
            return login_cookie
            print '----login success---'
        except Exception,e:
            print '----login error----'
            exit(0)

    def log(self,type,text):
            fp = open(type+'.txt','a')
            fp.write(text)
            fp.write('\r\n')
            fp.close()

    def check(self,id):
        infoUrl='http://huodong.weibo.com/hongbao/'+str(id)
        html=requests.get(infoUrl).text
        if 'action-type="lottery"' in  html or True: 
                    logUrl="http://huodong.weibo.com/aj_hongbao/detailmore?page=1&type=2&_t=0&__rnd=1423744829265&uid="+str(id)
                    param={}
                    header= {
                            'Cache-Control':'no-cache',
                            'Content-Type':'application/x-www-form-urlencoded',
                            'Pragma':'no-cache',
                            'Referer':'http://huodong.weibo.com/hongbao/detail?uid='+str(id),
                            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 BIDUBrowser/6.x Safari/537.36',
                            'X-Requested-With':'XMLHttpRequest'
                            }
                    res=requests.post(logUrl,data=param,headers=header)
                    pMoney=re.compile(r'<span class="money">(\d+?.+?)\xd4\xaa</span>',re.DOTALL) 
                    luckyLog=pMoney.findall(html,re.DOTALL)

                    if len(luckyLog)==0:
                            maxMoney=0
                    else:
                            maxMoney=float(luckyLog[0])

                    if maxMoney<10: 
                            print u'-----too low money-----'
                            return False
        else:
                    print u"---------too slow---------"
                    print  "----------......----------"
                    return False
        return True

    def getLucky(self,id):
        print u'-----find hongbao:'+str(id)+"-----"

        if self.check(id)==False:
            return

        luck_url='http://huodong.weibo.com/aj_hongbao/getlucky'

        lucky_data={'ouid':id,
                    'share':0,
                    '_t':0}

        header= {
                    'Cache-Control':'no-cache',
                    'Content-Type':'application/x-www-form-urlencoded',
                    'Origin':'http://huodong.weibo.com',
                    'Pragma':'no-cache',
                    'Referer':'http://huodong.weibo.com/hongbao/'+str(id),
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 BIDUBrowser/6.x Safari/537.36',
                    'X-Requested-With':'XMLHttpRequest'
                    }

        cookie=self.weibo_login('joey83@sina.cn','xxxx')

        res=requests.post(luck_url,data=lucky_data,cookies=cookie).text
        #print res
        res_json=json.loads(res)
        print res_json

        if res_json["code"]=='901114': 
            print u"---------up the top---------"
            print  "----------......----------"
            self.log('lucky',str(id)+'---'+str(res_json["code"])+'---'+res_json["data"]["title"])
            exit(0)
        elif res_json["code"]=='100000':
            print u"---------gong xi fa cai---------"
            print  "----------......----------"
            self.log('success',str(id)+'---'+res)
            exit(0)

        if res_json["data"] and res_json["data"]["title"]:
            print res_json["data"]["title"]
            print  "----------......----------"
            self.log('lucky',str(id)+'---'+str(res_json["code"])+'---'+res_json["data"]["title"])
        else:
            print u"---------request error---------"
            print  "----------......----------"
            self.log('lucky',str(id)+'---'+res)