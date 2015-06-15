#!/usr/bin/env python

import urllib
import urllib2
import re
import os
import spider_tool

class Spider:
	def __init__(self):
		self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'
		self.tool = spider_tool.Tool()

	def getPage(self,pageIndex):
		url = self.siteURL+"?page="+str(pageIndex)
		request = urllib2.Request(url)
		response = urllib2.urlopen(request)
		return response.read().decode('gbk')


	def getContents(self,pageIndex):
		page = self.getPage(pageIndex)
		pattern = re.compile('<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',re.S)
		items = re.findall(pattern, page)
		contents = []
		for item in items:
			contents.append(["http:"+item[0],"http:"+item[1],item[2],item[3],item[4]])
		return contents

	def getDetailPage(self,infoURL):
		response = urllib2.urlopen(infoURL)
		return response.read().decode('gbk')

	def getBrief(self,page):
		pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
		result = re.search(pattern, page)
		return self.tool.replace(result.group(1))

	def getAllImg(self,page):
		pattern =  re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
		content = re.search(pattern, page)
		patternImg = re.compile('<img.*?src="(.*?)"',re.S)
		images = re.findall(patternImg, content.group(1))
		return images

	def saveImgs(self,images,name):
		number = 1
		print u"find",name,"have",len(images),"photo"
		for imageURL in images:
			splitPath  = imageURL.split('.')
			fTail = splitPath.pop()
			if fTail == "jpg":
				fileName = name+"/"+str(number)+"."+fTail
				self.saveImg(imageURL, fileName)
				number += 1

	def saveIcon(self,iconURL,name):
		splitPath = iconURL.split('.')
		fTail = splitPath.pop()
		fileName = name="/icon."+fTail
		self.saveImg(iconURL,fileName)


	def saveBrief(self,content,name):
		fileName = name+"/"+name+".txt"
		f = open(fileName,"w+")
		print "save her information as",fileName
		f.write(content.encode('utf-8'))

	def printBrief(self,content,name):
		pattern = re.compile(r'1\d{10}')
		tel = re.findall(pattern, content)
		pattern2 = re.compile(r'\d{6,10}')
		qq = re.findall(pattern2, content)
		print "name:%s,Tel is:%s,QQ is:%s" % (name,tel,qq)



	def saveImg(self,imageURL,fileName):
		u = urllib.urlopen(imageURL)
		data = u.read()
		f = open(fileName,'wb')
		f.write(data)
		print "save her photo",fileName
		f.close()

	def mkdir(self,path):
		path = path.strip()
		isExists = os.path.exists(path)
		if not isExists:
			print "create folder",path
			os.makedirs(path)
			return True
		else:
			print "have folder",path
			return False


	def savePageInfo(self,pageIndex):
		contents = self.getContents(pageIndex)
		for item in contents:
			#print "find model,name:",item[2],",age:",item[3],",at:",item[4]
			print "find model,name:",item[2]
			print "find her blog:",item[0]
			detailURL = item[0]
			detailPage = self.getDetailPage(detailURL)
			brief = self.getBrief(detailPage)
			self.printBrief(brief,item[2])
			#images = self.getAllImg(detailPage)
			#self.mkdir(item[2])
			#self.saveBrief(brief, item[2])
			#self.saveIcon(item[1], item[2])
			#self.saveImgs(images, item[2])

	def savePagesInfo(self,start,end):
		for i in range(start,end+1):
			print "find mm at place:",i
			self.savePageInfo(i)

spider = Spider()
spider.savePagesInfo(1, 3)


