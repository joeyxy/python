#!/usr/bin/python
# vim: set fileencoding=utf-8:

###########################################
#
#   目录测试(探测敏感目录是否存在)
#	 1) 容错测试
#	 2) 服务器指纹识别
#	 3) 404重定向识别
#	 4) 获得响应头
#
###########################################

import hashlib
import random
from httplib2 import Http


class Directory_testing:

	def __init__(self,target):
		self.target=target

	# 找出404页面
	def Error404(self):
		# 生成随机的测试目录
		text=hashlib.sha1(str(random.uniform(1,100000))).hexdigest()
		try:
			# 测试404的标准是什么
			# 如果状态是404则证明是标准的404页面
			# 如果状态是302则证明会直接跳转,就以302作为标准
			# 如果状态是200的情况,则证明存在自定义的404页面,抓下来作为指标
			resp,content=Http().request(self.target+'/'+text,"GET")
			if resp['status']==404:
				return "default"
			elif resp['status']==302:
				return "Jump"
			elif resp['status']==200:
				return content
		except:
			print "[*] 404 Page GET Error!"

	# 获得目录测试返回的值
	def get_results(self,text):
		results=[]
		try:
			resp,content=Http().request(self.target+text,"GET")
			results.append(self.target+text)
			results.append(resp['status'])
			results.append(resp['server'])
			results.append(content)
			return results
		except:
			print "[*] testing "+self.target+" Error!"

	# 导入目录字典
	def load_dictionary(self,patch):
		tmp_data=[]
		for  line in open(patch):
			tmp_data.append(line.strip("\n"))
		return tmp_data

	# 主程序调用
	def _main(self):
		if self.Error404()=="default":
			self.default_mode()

t=Directory_testing("http://www.163.com")
 t.load_dictionary("../dic/dictionary.dic")
# for i in a:
# 	print t.get_results(i)
