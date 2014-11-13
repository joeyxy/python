#!/usr/bin/python
# vim: set fileencoding=utf-8:
import sys

###########################################
#
# db数据库类(实现数据库操作)
#
###########################################

class Log_do:

	def __init__(self,filename):
		self.filename=filename

	def w_log(self,text):
		try:
			self.obj=open(self.filename,'a')
			self.obj.write(text+'\n')
			self.obj.close()
		except:
			print "[*] Write Log Error! Programe is Exit!"
			sys.exit(1)
			

#t=Log_do("twa.txt")
#t.w_log("aaaaaa")
