#!/usr/bin/env python
#coding=utf-8

import re
import urllib
import urllib2
import cookielib
import base64 
import binascii 
import os
import json
import sys 
import cPickle as p
import rsa



cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
reload(sys)
sys.setdefaultencoding('utf-8')
luckyList=[]
lowest=10

def getData(url) :
	try:
		req  = urllib2.Request(url)
		result = opener.open(req)
		text = result.read()
		text=text.decode("utf-8").encode("gbk",'ignore')
		return text
	except Exception, e:
		print u'请求异常,url:'+url
		print e

def postData(url,data,header) :
	try:
		data = urllib.urlencode(data)  
		req  = urllib2.Request(url,data,header)
		result = opener.open(req)
		text = result.read()
		return text
	except Exception, e:
		print u'请求异常,url:'+url

def login(nick , pwd) :
	print u"----------登录中----------"
	print  "----------......----------"
	prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.15)&_=1400822309846' % nick
	preLogin = getData(prelogin_url)
	servertime = re.findall('"servertime":(.+?),' , preLogin)[0]
	pubkey = re.findall('"pubkey":"(.+?)",' , preLogin)[0]
	rsakv = re.findall('"rsakv":"(.+?)",' , preLogin)[0]
	nonce = re.findall('"nonce":"(.+?)",' , preLogin)[0]
	#print bytearray('xxxx','utf-8')
	su  = base64.b64encode(urllib.quote(nick))

	rsaPublickey= int(pubkey,16)
	key = rsa.PublicKey(rsaPublickey,65537)
	message = str(servertime) +'\t' + str(nonce) + '\n' + str(pwd)
	sp = binascii.b2a_hex(rsa.encrypt(message,key))
	header = {'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'}

	param = {
					'entry': 'weibo',
					'gateway': '1',
					'from': '',
					'savestate': '7',
					'userticket': '1',
					'ssosimplelogin': '1',
					'vsnf': '1',
					'vsnval': '',
					'su': su,
					'service': 'miniblog',
					'servertime': servertime,
					'nonce': nonce,
					'pwencode': 'rsa2',
					'sp': sp,
					'encoding': 'UTF-8',
					'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
					'returntype': 'META',
					'rsakv' : rsakv,
					}
	s = postData('http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)',param,header)
	try:
		urll = re.findall("location.replace\(\'(.+?)\'\);" , s)[0]
		print urll
		login=getData(urll)
		print u"---------登录成功！-------"
		print  "----------......----------"
	except Exception, e:
		print u"---------登录失败！-------"
		print  "----------......----------"
		exit(0)

def log(type,text):
	fp = open(type+'.txt','a')
	fp.write(text)
	fp.write('\r\n')
	fp.close()	

def getLucky(id): #抽奖程序
	print u"---抽红包中："+str(id)+"---"
	print  "----------......----------"

	if checkValue(id)==False: #不符合条件
		return

	luckyUrl="http://huodong.weibo.com/aj_hongbao/getlucky"
	param={
				'ouid':id,
				'share':0,
				'_t':0
			}


	header= {
				'Cache-Control':'no-cache',
				'Content-Type':'application/x-www-form-urlencoded',
				'Origin':'http://huodong.weibo.com',
				'Pragma':'no-cache',
				'Referer':'http://huodong.weibo.com/hongbao/'+str(id),
				'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 BIDUBrowser/6.x Safari/537.36',
				'X-Requested-With':'XMLHttpRequest'
 			}

	res = postData(luckyUrl,param,header)
	hbRes=json.loads(res)
	if hbRes["code"]=='901114': #今天红包已经抢完
		print u"---------已达上限---------"
		print  "----------......----------"
		log('lucky',str(id)+'---'+str(hbRes["code"])+'---'+hbRes["data"]["title"])
		exit(0)
	elif hbRes["code"]=='100000':#成功
		print u"---------恭喜发财---------"
		print  "----------......----------"
		log('success',str(id)+'---'+res)

	try:
		print hbRes["data"]["title"]
		print  "----------......----------"
		log('lucky',str(id)+'---'+str(hbRes["code"])+'---'+hbRes["data"]["title"])
	except Exception, e:
		print u"---------请求错误---------"
		print  "----------......----------"
		log('lucky',str(id)+'---'+res)

def getList():
	print u"---------查找目标---------"
	print  "----------......----------"

	themeUrl={ #主题列表
		'theme':'http://huodong.weibo.com/hongbao/theme',
		'pinpai':'http://huodong.weibo.com/hongbao/special_pinpai',
		'daka':'http://huodong.weibo.com/hongbao/special_daka',
		'youxuan':'http://huodong.weibo.com/hongbao/special_youxuan',
		'qiye':'http://huodong.weibo.com/hongbao/special_qiye',
		'quyu':'http://huodong.weibo.com/hongbao/special_quyu',
		'meiti':'http://huodong.weibo.com/hongbao/special_meiti',
		'hezuo':'http://huodong.weibo.com/hongbao/special_hezuo'
	}

	topUrl={ #排行榜列表
		'mostmoney':'http://huodong.weibo.com/hongbao/top_mostmoney',
		'mostsend':'http://huodong.weibo.com/hongbao/top_mostsend',
		'mostsenddaka':'http://huodong.weibo.com/hongbao/top_mostsenddaka',
		'mostsendpartner':'http://huodong.weibo.com/hongbao/top_mostsendpartner',
		'cate':'http://huodong.weibo.com/hongbao/cate?type=',
		'clothes':'http://huodong.weibo.com/hongbao/cate?type=clothes',
		'beauty':'http://huodong.weibo.com/hongbao/cate?type=beauty',
		'fast':'http://huodong.weibo.com/hongbao/cate?type=fast',
		'life':'http://huodong.weibo.com/hongbao/cate?type=life',
		'digital':'http://huodong.weibo.com/hongbao/cate?type=digital',
		'other':'http://huodong.weibo.com/hongbao/cate?type=other'
	}


	for (theme,url) in themeUrl.items():
		print "----------"+theme+"----------"
		print  url
		print  "----------......----------"
		getThemeList(url,1)

	for (top,url) in topUrl.items():
		print "----------"+top+"----------"
		print  url
		print  "----------......----------"
		getTopList(url,0,1)
		getTopList(url,1,1)


	
def getThemeList(url,p):#主题红包
	print  u"---------第"+str(p)+"页---------"
	print  "----------......----------"
	html=getData(url+'?p='+str(p))
	pWrap=re.compile(r'<div class="info_wrap">(.+?)<span class="rob_txt"></span>',re.DOTALL) #h获取所有info_wrap的正则
	pInfo=re.compile(r'.+<em class="num">(.+)</em>.+<em class="num">(.+)</em>.+<em class="num">(.+)</em>.+href="(.+)" class="btn"',re.DOTALL) #获取红包信息
	List=pWrap.findall(html,re.DOTALL)
	n=len(List)
	if n==0:
		return
	for i in range(n): #遍历所有info_wrap的div
 		s=pInfo.match(List[i]) #取得红包信息
 		info=list(s.groups(0))
 		info[0]=float(info[0].replace('\xcd\xf2','0000')) #现金,万->0000
 		try:
 			info[1]=float(info[1].replace('\xcd\xf2','0000')) #礼品价值
 		except Exception, e:
 			info[1]=float(info[1].replace('\xd2\xda','00000000')) #礼品价值
 		info[2]=float(info[2].replace('\xcd\xf2','0000')) #已发送
 		if info[2]==0:
 			info[2]=1 #防止除数为0
 		if info[1]==0:
 			info[1]=1 #防止除数为0
 		info.append(info[0]/(info[2]+info[1])) #红包价值,现金/（领取人数+礼品价值）
 		# if info[0]/(info[2]+info[1])>100:
 		# 	print url
 		luckyList.append(info)
	if 'class="page"' in html:#存在下一页
		p=p+1
		getThemeList(url,p) #递归调用自己爬取下一页


def getTopList(url,daily,p):#排行榜红包
	print  u"---------第"+str(p)+"页---------"
	print  "----------......----------"
	html=getData(url+'?daily='+str(daily)+'&p='+str(p))
	pWrap=re.compile(r'<div class="list_info">(.+?)<span class="list_btn"></span>',re.DOTALL) #h获取所有list_info的正则
	pInfo=re.compile(r'.+<em class="num">(.+)</em>.+<em class="num">(.+)</em>.+<em class="num">(.+)</em>.+href="(.+)" class="btn rob_btn"',re.DOTALL) #获取红包信息
	List=pWrap.findall(html,re.DOTALL)
	n=len(List)
	if n==0:
		return
	for i in range(n): #遍历所有info_wrap的div
 		s=pInfo.match(List[i]) #取得红包信息
 		topinfo=list(s.groups(0))
 		info=list(topinfo)

		info[0]=topinfo[1].replace('\xd4\xaa','') #元->''
 		info[0]=float(info[0].replace('\xcd\xf2','0000')) #现金,万->0000
 		info[1]=topinfo[2].replace('\xd4\xaa','') #元->''

 		try:
 			info[1]=float(info[1].replace('\xcd\xf2','0000')) #礼品价值
 		except Exception, e:
 			info[1]=float(info[1].replace('\xd2\xda','00000000')) #礼品价值

 		info[2]=topinfo[0].replace('\xb8\xf6','') #个->''
 		info[2]=float(info[2].replace('\xcd\xf2','0000')) #已发送
 		if info[2]==0:
 			info[2]=1 #防止除数为0
 		if info[1]==0:
 			info[1]=1 #防止除数为0
 		info.append(info[0]/(info[2]+info[1])) #红包价值,现金/（领取人数+礼品价值）
 		# if info[0]/(info[2]+info[1])>100:
 		# 	print url

 		luckyList.append(info)
	if 'class="page"' in html:#存在下一页
		p=p+1
		getTopList(url,daily,p) #递归调用自己爬取下一页


def checkValue(id):
	infoUrl='http://huodong.weibo.com/hongbao/'+str(id)
	html=getData(infoUrl)
	if 'action-type="lottery"' in  html or True: #存在抢红包按钮
		logUrl="http://huodong.weibo.com/aj_hongbao/detailmore?page=1&type=2&_t=0&__rnd=1423744829265&uid="+id #查看排行榜数据
 		param={}
		header= {
				'Cache-Control':'no-cache',
				'Content-Type':'application/x-www-form-urlencoded',
				'Pragma':'no-cache',
				'Referer':'http://huodong.weibo.com/hongbao/detail?uid='+str(id),
				'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 BIDUBrowser/6.x Safari/537.36',
				'X-Requested-With':'XMLHttpRequest'
 			}
		res = postData(logUrl,param,header)
		pMoney=re.compile(r'<span class="money">(\d+?.+?)\xd4\xaa</span>',re.DOTALL) #h获取所有list_info的正则
		
		luckyLog=pMoney.findall(html,re.DOTALL)
		if len(luckyLog)==0:
			maxMoney=0
		else:	
			try:
				maxMoney=float(luckyLog[0])
			except Exception, e:
				mnum=re.findall(r'(\w*[0-9]+)\w*',luckyLog[0])
				maxMoney=float(mnum[0])

		if maxMoney<lowest: #记录中最大红包小于设定值
			return False

	else:
		print u"---------手慢一步---------"
		print  "----------......----------"
		return False
	return True

 
def start(username,password,low,fromFile):
	gl=False
	lowest=low

	login(username , password)

	if fromfile=='y':
		if os.path.exists('luckyList.txt'):
			try:
				f = file('luckyList.txt')  
				newList = p.load(f)
				print u'---------装载列表---------'
				print  "----------......----------"
			except Exception, e:
				print u'解析本地列表失败，抓取在线页面。'
				print  "----------......----------"
				gl=True
		else:
			print u'本地不存在luckyList.txt，抓取在线页面。'
			print  "----------......----------"
			gl=True

	if gl==True:
		getList()
		from operator import itemgetter
		newList=sorted(luckyList, key=itemgetter(4),reverse=True)
		f = file('luckyList.txt', 'w')  
		p.dump(newList, f) #把抓到的列表存到文件里，下次就不用再抓了
		f.close() 

	for lucky in newList:
		if not 'http://huodong.weibo.com' in lucky[3]: #不是红包
			continue
		print lucky[3]
		id=re.findall(r'(\w*[0-9]+)\w*',lucky[3])
		getLucky(id[0])
 

if __name__ == "__main__":  
	print  "-------------------------------------------------"
	try:
		uname=raw_input(u"请输入微博账号: ".decode('utf-8').encode('gbk'))
		pwd=raw_input(u"请输入微博密码: ".decode('utf-8').encode('gbk'))
		low=int(raw_input(u"红包领取最高现金大于n时参与: ".decode('utf-8').encode('gbk')))
		fromfile=raw_input(u"是否使用luckyList.txt中红包列表:(y/n) ".decode('utf-8').encode('gbk'))
	except Exception, e:
		print u"参数错误"
		print  "----------......----------"
		print e
		exit(0)


	print u"---------程序开始---------"
	print  "----------......----------"
	start(uname,pwd,low,fromfile)
	print u"---------程序结束---------"
	print  "----------......----------"
	os.system('pause')