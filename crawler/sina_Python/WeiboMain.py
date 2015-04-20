#!/usr/bin/env python
#coding=utf8


'''Author: Houkai
DATE: 2013.12.23'''

import urllib2
import cookielib

import WeiboEncode
import WeiboSearch

class WeiboLogin:
    
    def __init__(self, user, pwd, enableProxy = False):
        "初始化WeiboLogin，enableProxy表示是否使用代理服务器，默认关闭"

        print "Initializing WeiboLogin..."
        self.userName = user
        self.passWord = pwd
        self.enableProxy = enableProxy
        print "UserName:", user
        print "Password:", pwd
        
        self.serverUrl = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.11)&_=1379834957683"
        self.loginUrl = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.11)"
        self.postHeader = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'}

    def Login(self):
        "登陆程序"
    
        self.EnableCookie(self.enableProxy)#cookie或代理服务器配置
        
        serverTime, nonce, pubkey, rsakv = self.GetServerTime()#登陆的第一步
        postData = WeiboEncode.PostEncode(self.userName, self.passWord, serverTime, nonce, pubkey, rsakv)#加密用户和密码
        print "Post data length:\n", len(postData)

        req = urllib2.Request(self.loginUrl, postData, self.postHeader)
        print "Posting request..."
        result = urllib2.urlopen(req)#登陆的第二步——解析新浪微博的登录过程中3
        text = result.read()
        try:
            loginUrl = WeiboSearch.sRedirectData(text)#解析重定位结果
            urllib2.urlopen(loginUrl)
        except:
            print 'Login error!'
            return False
            
        print 'Login sucess!'
        return True

         
    def GetServerTime(self):
        "Get server time and nonce, which are used to encode the password"
        
        print "Getting server time and nonce..."
        serverData = urllib2.urlopen(self.serverUrl).read()#得到网页内容
        print serverData

        try:
	    serverTime, nonce, pubkey, rsakv = WeiboSearch.sServerData(serverData)#解析得到serverTime，nonce等
	    return serverTime, nonce, pubkey, rsakv
        except:
	    print 'Get server time & nonce error!'
	    return None


    def EnableCookie(self, enableProxy):
        "Enable cookie & proxy (if needed)."
        
        cookiejar = cookielib.LWPCookieJar()#建立cookie
        cookie_support = urllib2.HTTPCookieProcessor(cookiejar)

        if enableProxy:
            proxy_support = urllib2.ProxyHandler({'http':'http://xxxxx.pac'})#使用代理
            opener = urllib2.build_opener(proxy_support, cookie_support, urllib2.HTTPHandler)
            print "Proxy enabled"
        else:
            opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)

        urllib2.install_opener(opener)#构建cookie对应的opener

if __name__ == '__main__':
    weiboLogin = WeiboLogin('joey83@sina.cn', '')#邮箱（账号）、密码
    if weiboLogin.Login() == True:
        print "登陆成功！"
