#!/usr/bin/python
# vim: set fileencoding=utf-8:

###########################################
#
#   sprider 爬虫类(实现页面爬虫)
#
###########################################

import sys
import urllib2
import re
from BeautifulSoup import BeautifulSoup

class SpriderUrl:
    # 初始化
    def __init__(self,url):
        self.url=url
        self.con=Db_Connector('sprider.ini')

#获得目标url的第一次url清单
    def get_self(self):
        urls=[]
        try:
            body_text=urllib2.urlopen(self.url).read()
        except:
            print "[*] Web Get Error:checking the Url"
        soup=BeautifulSoup(body_text)
        links=soup.findAll('a')
        for link in links:
            # 获得了目标的url但还需要处理
            _url=link.get('href')
             # 接着对其进行判断处理
             # 先判断它是否是无意义字符开头以及是否为None值
             # 判断URL后缀,不是列表的不抓取
            if re.match('^(javascript|:;|#)',_url) or _url is None or re.match('.(jpg|png|bmp|mp3|wma|wmv|gz|zip|rar|iso|pdf|txt|db)$',_url):
                continue
            # 然后判断它是不是http|https开头,对于这些开头的都要判断是否是本站点， 不做超出站点的爬虫
            if re.match('^(http|https)',_url):
                if not re.match('^'+self.url,_url):
                    continue
                else:
                    urls.append(_url)
            else:
                urls.append(self.url+_url)
        rst=list(set(urls))
        for rurl in rst:
            if self.con.find_item("select * from url_sprider where url='"+rurl+"' and domain='"+self.url+"'"):
                continue
            else:
                try:
                    self.con.insert_item("insert into url_sprider(url,tag,domain)values('"+rurl+"',0,'"+self.url+"')")
                except:
                    print "[*] insert into is Error!"


    def sprider_self_all(self,domain):
        urls=[]
        try:
            body_text=urllib2.urlopen(domain).read()
        except:
            print "[*] Web Get Error:checking the Url"
            sys.exit(0)
        soup=BeautifulSoup(body_text)
        links=soup.findAll('a')
        for link in links:
            # 获得了目标的url但还需要处理
            _url=link.get('href')
             # 接着对其进行判断处理
             # 先判断它是否是无意义字符开头以及是否为None值
             # 判断URL后缀,不是列表的不抓取
            try:
                if re.match('^(javascript|:;|#)',str(_url)) or str(_url) is None or re.match('.(jpg|png|bmp|mp3|wma|wmv|gz|zip|rar|iso|pdf|txt|db)$',str(_url)):
                    continue
            except TypeError:
                print "[*] Type is Error! :"+str(_url)
                continue
            # 然后判断它是不是http|https开头,对于这些开头的都要判断是否是本站点， 不做超出站点的爬虫
            if re.match('^(http|https)',_url):
                if not re.match('^'+self.url,_url):
                    continue
                else:
                    urls.append(_url)
            else:
                urls.append(self.url+_url)
        res=list(set(urls))
        for rurl in res:
            if self.con.find_item("select * from url_sprider where url='"+rurl+"' and domain='"+self.url+"'"):
                continue
            else:
                try:
                    self.con.insert_item("insert into url_sprider(url,tag,domain)values('"+rurl+"',0,'"+self.url+"')")
                except:
                    print "[*] insert into is Error!"

    def sprider_self(self):        
        while  True:
            wat_list=self.con.find_all("select url from url_sprider where domain='"+self.url+"' and tag=0")
            if len(wat_list)>0:
                for url in wat_list:
                    try:
                        self.con.update_item("update url_sprider set tag=1 where url='"+url[0]+"'")
                    except:
                        print "[*] DB update Error!"
                        continue
                    try:
                        self.sprider_self_all(url[0])
                    except:
                        print "[*]Sprider Error!"
                        continue
            else:
                print "[*] Sprider is Finish!"
                break

# spi="http://www.baidu.com/"
# t=SpriderUrl(spi)
# # 第一次捕获
# t.get_self()
# # 开始深度爬虫
# t.sprider_self()
