#!/usr/bin/env python
#coding=utf8

'''Author: Houkai
DATE: 2013.12.23'''

import re
import json

def sServerData(serverData):
    "Search the server time & nonce from server data"
    
    p = re.compile('\((.*)\)')
    jsonData = p.search(serverData).group(1)
    data = json.loads(jsonData)
    serverTime = str(data['servertime'])
    nonce = data['nonce']
    pubkey = data['pubkey']#
    rsakv = data['rsakv']# 
    print "Server time is:", serverTime
    print "Nonce is:", nonce
    return serverTime, nonce, pubkey, rsakv


def sRedirectData(text):
    p = re.compile('location\.replace\([\'"](.*?)[\'"]\)')
    loginUrl = p.search(text).group(1)
    print 'loginUrl:',loginUrl
    return loginUrl
