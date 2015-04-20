#!/usr/bin/env python
#coding=utf8

'''Author: Houkai
DATE: 2013.12.23'''

import urllib
import base64
import rsa
import binascii

def PostEncode(userName, passWord, serverTime, nonce, pubkey, rsakv):
    "Used to generate POST data"
        
    encodedUserName = GetUserName(userName)#用户名使用base64加密
    encodedPassWord = get_pwd(passWord, serverTime, nonce, pubkey)#目前密码采用rsa加密
    postPara = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'userticket': '1',
        'ssosimplelogin': '1',
        'vsnf': '1',
        'vsnval': '',
        'su': encodedUserName,
        'service': 'miniblog',
        'servertime': serverTime,
        'nonce': nonce,
        'pwencode': 'rsa2',
        'sp': encodedPassWord,
        'encoding': 'UTF-8',
        'prelt': '115',
        'rsakv': rsakv,     
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }
    postData = urllib.urlencode(postPara)#网络编码
    return postData


def GetUserName(userName):
    "Used to encode user name"
    
    userNameTemp = urllib.quote(userName)
    userNameEncoded = base64.encodestring(userNameTemp)[:-1]
    return userNameEncoded


def get_pwd(password, servertime, nonce, pubkey):
    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537) #创建公钥
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password) #拼接明文js加密文件中得到
    passwd = rsa.encrypt(message, key) #加密
    passwd = binascii.b2a_hex(passwd) #将加密信息转换为16进制。
    return passwd