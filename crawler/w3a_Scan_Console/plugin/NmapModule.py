#!/usr/bin/python
#-*- encoding: utf-8 -*-

###########################################
#
#   Nmap 扫描类(生成扫描结果)
#
###########################################

import nmap
import time
import sys

class Web_Scan_Frame:
	
	def setScan_Main(self, scan_main):
		self.scan_main=scan_main

	def start(self,target,temple):
		# 在这要判断temple的类型,如果类型中存在该扫描项目
		# 则运行
		# 否则就忽略
		self.__object_do(target)
		
	# 放置:扫描目标,扫描模板
	def __object_do(self,target):
		# 需要根据扫描模板来查询是否有该模块扫描的功能
		self.scan_main.print_log('Nmap Scan Target: %s' % target)
		nm=nmap.PortScanner()
		# 判断长度,查看到底是多个还是一个。
		if(target.split(';') >=2):
			self.target_list=" ".join(target.split(';'))
		else:
			self.target_list=target
		nm.scan(hosts=self.target_list,arguments='-T4 -O')
		# 操作扫描结果
		for ip in nm.all_hosts():
			self.scan_main.print_log('Result ip: %s' % ip)
			for item in nm[ip].all_protocols():
				# 系统指纹识别
				if item=="osmatch":
					for os in nm[ip]['osmatch']:
						self.scan_main.print_log("os name: %s, persend: %s%% " % (os['name'],os['accuracy']))
				elif item=="tcp":
					for port in nm[ip]['tcp'].keys():
						self.scan_main.print_log("port: %s ,status: %s , servie: %s" % (port,nm[ip]['tcp'][port]['state'],nm[ip]['tcp'][port]['name']))

	def stop(self):
		self.scan_main.print_log("Finish Nmap target:%s" % self.target_list)

def getPluginClass():
	return Web_Scan_Frame
