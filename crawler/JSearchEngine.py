#!/usr/bin/python
#-*-coding:utf-8-*-
# JSearchEngine
# Author: Jam <810441377@qq.com>
# Git: https://github.com/codejam1024/JSearchEngine
# -------//-------//----
# TODO:
#	1.线程太过粗糙,待优化

import os
import sys
import cgi
import time
import gzip
import threading
import urllib2
import MySQLdb
from threading import Thread
from bs4 import BeautifulSoup
from cStringIO import StringIO
from urlparse import urlparse

Version = "1.0"
reload(sys)
sys.setdefaultencoding('utf8')

#调试编码
#sys.path.append('/src/chardet-1.1')
#import chardet
#print chardet.detect(htmlText)

################################################################
class DataBase(object):
	Host = "localhost"
	User = "root"
	Pass = "143205"
	DataBaseName = ""
	DataConn = None
	def __init__(self, dataBaseName):
		self.DataBaseName = dataBaseName.replace(".", "_")

	def Connect(self):
		self.DataConn = MySQLdb.connect(host=self.Host, user=self.User, passwd=self.Pass, db=self.DataBaseName, charset='utf8', port=3306)

	def Create(self):
		self.DataConn = MySQLdb.connect(host=self.Host, user=self.User, passwd=self.Pass, charset='utf8', port=3306)
		c = self.DataConn.cursor()
		try:
			c.execute('create database if not exists %s DEFAULT CHARACTER SET utf8 COLLATE utf8_bin' % (self.DataBaseName))
			self.DataConn.select_db(self.DataBaseName)
			c.execute("create table Link(Title Text, Link Text, Date Text, Status Text);")
		except Exception, e:
			print "[E]->Class->DataBase->Create:%s" % (e)

		c.close()
		self.DataConn.commit()

	def Remove(self):
		self.DataConn = MySQLdb.connect(host=self.Host, user=self.User, passwd=self.Pass, charset='utf8', port=3306)
		c = self.DataConn.cursor()
		try:
			self.DataConn.select_db(self.DataBaseName)
			print "[I]Drop table LinkFactory, Drop table Link."
			c.execute("drop table if exists Link")
			#得自行删除数据库，否则某些情况MySQL会卡机
			#c.execute('drop database if exists %s' % (self.DataBaseName))
		
		except Exception, e:
			pass

		c.close()
		self.DataConn.commit()

	def LinkIsHaveWork(self):
		c = self.DataConn.cursor()
		try:
			sql = "select * from Link where Status='work';"
			c.execute(sql)
			link = c.fetchone()
			c.close()
			if link != None:
				return True
			else:
				return False

		except Exception, e:
			print "[E]->Class->DataBase->LinkIsHaveWork:" + str(e)

		c.close()

	def LinkStatusGet(self, link):
		c = self.DataConn.cursor()
		try:
			sql = "select * from Link where Link='%s';" % (link)
			c.execute(sql)
			link = c.fetchone()
			c.close()
			if link != None:
				return link[3]
			else:
				return None

		except Exception, e:
			print "[E]->Class->DataBase->LinkStatusGet:" + str(e)

		c.close()

	def LinkUnreadGet(self):
		c = self.DataConn.cursor()
		try:
			sql = "select * from Link where Status='unread';"
			c.execute(sql)
			link = c.fetchone()
			c.close()
			if link != None:
				return link[1]
			else:
				return None

		except Exception, e:
			print "[E]->Class->DataBase->LinkUnreadGet:" + str(e)

		c.close()

	def LinkDel(self, link):
		c = self.DataConn.cursor()
		try:
			sql = "delete from Link where Link='%s';" % (link)
			c.execute(sql)
		except Exception, e:
			print "[E]->Class->DataBase->LinkDel:" + str(e)

		self.DataConn.commit()
		c.close()

	def LinkInsert(self, link):
		c = self.DataConn.cursor()
		try:
			sql = "select * from Link where Link='%s';" % (link)
			c.execute(sql)
			if c.fetchone() == None:
				sql = "insert into Link values('', '%s', '', 'unread');" % (link)
				c.execute(sql)
				c.close()
				#print sql
			else:
				return False

		except Exception, e:
			print "[E]->Class->DataBase->LinkInsert:" + str(e)
			return False

		self.DataConn.commit()
		c.close()
		return True;

	def LinkUpdate(self, link, title, date, status):
		c = self.DataConn.cursor()
		try:
			sql = "update Link SET Title='%s',Date='%s',Status='%s' where Link='%s';" % (title, date, status, link)
			c.execute(sql)
			print sql

		except Exception, e:
			print "[E]->Class->DataBase->LinkUpdate:" + str(e)

		self.DataConn.commit()
		c.close()
		return;

	def LinkUpdateWork(self):
		c = self.DataConn.cursor()
		try:
			sql = "update Link SET Status='unread' where Status='work';"
			c.execute(sql)
			print sql

		except Exception, e:
			print "[E]->Class->DataBase->LinkUpdateWork:" + str(e)

		c.close()
		self.DataConn.commit()
		return;

	def LinkSearch(self, title):
		c = self.DataConn.cursor()
		try:
			sql = "select * from Link where Title like '%" + title + "%';"
			c.execute(sql)
			data = c.fetchall()
			c.close()
			return data

		except Exception, e:
			print "[E]->Class->DataBase->LinkSearch:" + str(e)

		c.close()
		return [];


	def __del__(self):
		self.DataConn.close()



###############################################################
#爬虫类，爬虫的一些操作都在这里执行
class Crawler(object):
	#全局变量
	TargetHost  = ""
	UserAgent   = ""

	UserAgent  = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'
	BadFilterRules  = ['#', '.jpeg','.jpg','.rar','.png','.zip','.rar','.7z','javascript:','mailto:']

	ThreadMax   = 25 # 最大线程
	ThreadLock  = threading.Lock()
	ThreadTotal = 0
	ThreadSignal = ""
	MyDataBase   = DataBase

	def AnalyzePage():return; # 预定义函数,以便在该函数前面的函数调用该函数

	def __init__(self, host):
		self.TargetHost = host

	def ToUtf8(self, text):
		try:
			return text.decode("gbk")
		except Exception, e:
			return text

	def GetHtmlText(self, url):
		request  = urllib2.Request(url)
		request.add_header('Accept', "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp")
		request.add_header('Accept-Encoding', "*")
		request.add_header('User-Agent', self.UserAgent)
		rp = urllib2.urlopen(request)
		rpHtmlText = ""
		contentEncoding =  rp.headers.get('Content-Encoding')
		if  contentEncoding == 'gzip':
			compresseddata = rp.read()
			compressedstream = StringIO(compresseddata)
			gzipper = gzip.GzipFile(fileobj=compressedstream)
			rpHtmlText = gzipper.read()
		else:
			rpHtmlText = rp.read()
		return rpHtmlText

	def UrlEscape(self, url):
		try:
			url = urllib2.unquote(url)
			url = urllib2.quote(url.encode('utf8'))
			url = url.replace("%3A", ":")
		except Exception, e:
			print "[E]UrlEscape->%s,Url:%s" % (e, url) 
		
		return url;

	def UrlFilter(self, host, urls):
		returnUrls = []
		for url in urls:
			url_lower = url.lower()
			isBadUrl = False

			#判断是否为其他域名
			if url_lower.find("http:") >= 0 or url_lower.find("https:") >= 0:
				urlHost = ''
				try:
					urlHost = str(urlparse(url).hostname) # Have Bug
				except Exception, e:
					print "[E]->UrlFilter: %s" % (e)
				
				if urlHost.find(host) == -1:
					#print "!!! Fuck->Host:%s,Url:%s" % (urlHost, url)
					isBadUrl = True

			#链接是否超长
			if len(url) >= 200:
				isBadUrl = True


			#进行过滤规则筛选
			for rule in self.BadFilterRules:
				if url_lower.find(rule) != -1: 
					#print url + "-" + rule
					isBadUrl = True

			if isBadUrl : continue

			#网址智能补全
			if url.find("http:") == -1 and url.find("https:") == -1:
				if url[0] != "/" : url = "/" + url
			if url.find("http:") == -1 and url.find("https:") == -1:
				url = "http://" + host + url
			
			url = self.UrlEscape(url)
			returnUrls.append(url)
		
		return returnUrls

	def ThreadOpen(self, func, argv):
		while self.ThreadTotal >= self.ThreadMax:
			time.sleep(2)

		self.ThreadLock.acquire()
		self.ThreadTotal += 1
		self.ThreadLock.release()
		t = threading.Thread(target=func,args=(argv,))
		t.setDaemon(True)
		t.start()
		time.sleep(1)

	def AddUrls(self, urls):
		myDataBase = DataBase(self.TargetHost)
		myDataBase.Connect()
		for url in urls:
			isOk = myDataBase.LinkInsert(url)
			if isOk:
				if self.ThreadTotal < self.ThreadMax:
					self.ThreadOpen(self.AnalyzePage, url)

		return;


	def AnalyzePage(self, link):
		print "[I]AnalyzePage:" + link
		myDataBase = DataBase(self.TargetHost)
		myDataBase.Connect()
		myDataBase.LinkUpdate(link,'','','work')

		try:
			htmlText = self.GetHtmlText(link)
			htmlText = self.ToUtf8(htmlText)
			soup = BeautifulSoup(htmlText, from_encoding="utf8")
			docTitle = '404 - Not Found'

			try:
				docTitle = soup.title.string

			except Exception, e:
				print "[E]soup.title.string:" + link

			
			
			tags = soup.findAll('a')
			urls = [];
			for tag in tags:
				url = tag.get('href','')
				if url!= '' : urls.append(url)

			urls = self.UrlFilter(self.TargetHost, urls)
			print "Links length:%s" % (len(urls))

			self.AddUrls(urls)

			timeText = time.strftime('%Y-%m-%d',time.localtime(time.time()))
			myDataBase.LinkUpdate(link, docTitle, timeText, "ok")

		except urllib2.HTTPError,e:
			myDataBase.Connect()
			myDataBase.LinkDel(link)
			print "[E]->HTTP Error:%s,Link:%s" % (e, link)

		self.ThreadLock.acquire()
		self.ThreadTotal -= 1
		self.ThreadLock.release()
		print "[I]ThreadTotal:%s" % (self.ThreadTotal)


	def RunWork(self):

		myDataBase = DataBase(self.TargetHost)
		myDataBase.Connect()

		while True:
			myDataBase.Connect()
			self.ThreadLock.acquire()
			link = myDataBase.LinkUnreadGet()
			self.ThreadLock.release()

			if link == None:
				
				self.ThreadLock.acquire()
				if myDataBase.LinkIsHaveWork() == False:
					self.ThreadLock.release()
					print "No task."
					break
				else:
					self.ThreadLock.release()
					print "Wait task. ThreadTotal:%s" % (self.ThreadTotal)
					time.sleep(2)
					continue
				
				
			else:
				while True:
					myDataBase.Connect()
					self.ThreadOpen(self.AnalyzePage, link)
					self.ThreadLock.acquire()
					status = myDataBase.LinkStatusGet(link)
					self.ThreadLock.release()
					
					if status != 'unread':
						print "Work Get:" + link
						break

					time.sleep(1)
					print "Wait,status:" + status 
		return;

	def Work(self):
		self.MyDataBase = DataBase(self.TargetHost)
		self.MyDataBase.Connect()
		self.MyDataBase.LinkUpdateWork()
		self.RunWork()
		return;

	def NewWork(self):
		self.MyDataBase = DataBase(self.TargetHost)
		self.MyDataBase.Remove()
		self.MyDataBase.Create()
		self.MyDataBase.Connect()
		self.MyDataBase.LinkUpdateWork()
		self.MyDataBase.LinkInsert("http://" + self.TargetHost)
		print "[I]New work:" + "http://" + self.TargetHost
		self.RunWork()
		return;

	def Search(self, keyWord):
		print "You KeyWord:" + keyWord
		self.MyDataBase = DataBase(self.TargetHost)
		self.MyDataBase.Connect()
		data = self.MyDataBase.LinkSearch(keyWord)
		for row in data:
			print "Title:%s,Link:%s" % (row[0],row[1])

		return;



	def Stop(self):
		self.ThreadSignal = "stop"
		return;

def ThreadWork(host):
	newCrawler = Crawler(host)
	newCrawler.NewWork()


def Explain(argv):
	if len(argv) == 2:
		if argv[1] == "version":
			print "JSearchEngine v" + Version
			return;

	if len(argv) == 3:
		### Test
		if argv[1] == "fuck" and argv[2] == "this":
			print "Are you kidding me?"
			return;

		if(argv[1] == "newwork" and argv[2] != ""):
			newCrawler = Crawler(argv[2])
			newCrawler.NewWork()
			return;

		if(argv[1] == "work" and argv[2] != ""):
			newCrawler = Crawler(argv[2])
			newCrawler.Work()
			return;

	if len(argv) == 4:
		if(argv[1] == "search" and argv[2] != ""):
				newCrawler = Crawler(argv[2])
				newCrawler.Search(argv[3])
				return;

	print "JSearchEngine v" + Version
	print "python JSearchEngine.py newwork HOST \r\n         #Create a new work to search for HOST"
	print "python JSearchEngine.py work HOST \r\n         #Continue a work to search for HOST"
	print "python JSearchEngine.py search HOST title \r\n         #Search a title in DataBase"
	return;

def Main():
	Explain(sys.argv)

#___Main____
Main()