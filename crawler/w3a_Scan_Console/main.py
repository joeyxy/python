#-*- encoding: utf-8 -*-
import os
import sys
import hashlib
import random
import string
#from lib.process_exec import process_class
from lib.log_exec import Log_do
from lib.DB_module import Db_module


class Scan_Main:

	# 程序的主过程
	def __init__(self):
		try:
			# 生成一个随机的名称作为异常日志的记录
			m=hashlib.md5(str(random.randint(1,100000))+"log")
			self.log_name=m.hexdigest()
			# 日志记录初始化
			self.log=Log_do(os.path.split(os.path.realpath(__file__))[0]+"/log/sys/"+self.log_name+".log")
		except:
			print "[*] Create log file is error! Please check directory purview!"
			sys.exit(0)
		try:
			# 输出Logo
			self.readmade()
			# 输出现有模块(并且自检)
			self.__module()
		except:
			self.print_load("Import Module is Error!")
		else:
			try:
				# 导入模块
				self.__loadPlugins()
			except:
				self.print_load("Loading Plugins Error!")
				sys.exit(0)
	
	# 程序LOGO
	def readmade(self):
		print r"----------------------------------------------------"
		print r"																		"
		print r"	 w3a_scan_console		"
		print r"																		"
		print r"	       by:Smart		"
		print r"																		"
		print r"----------------------------------------------------"
	
	# 输出现有模块/并自检
	def __module(self):
		ScanFilepath=os.path.split(os.path.realpath(__file__))[0]
		if os.path.exists(ScanFilepath+"/plugin"):
			self.print_log("Module List:")
			for filename in os.listdir(ScanFilepath+'/plugin'):
				if not filename.endswith('.py') or filename.startswith('_'):
					continue
				self.print_log("+ Module: %s" % os.path.splitext(filename)[0])
			self.print_log("-----------------------------------")
		else:
			# 如果模块文档不存在要退出控制，确保模块存在，不然无法检测。
			self.print_log("Plugins directory not in here!")
			self.print_log("Done")
			sys.exit(0)

	# MAIN 主体程序
	def __mainProgram(self):
		# 加载数据库钥匙，并初始化对象
		db_key=Db_module()
		# 更新数据，将前30条未初始化的任务设置为待调度的状态
		db_key.execute_sql("update w3a_Scan_Task set t_status_num=1 where t_status_num=0 limit 30")
		# 查出10条已经待调度状态的扫描任务，并进行处理
		while True:
			## 1\将任务读取出来并存储
			temp_data=db_key.find_all("select * from w3a_Scan_Task where t_status_num=1 limit 10")
			if temp_data>0:
				## 2\将取出的任务状态更新为正在扫描状态
				db_key.execute_sql("update w3a_Scan_Task set t_status_num=2 where t_status_num=1 limit 10")
				## 3\分析T_type任务类型
				for t_data in temp_data:
					# 如果是Web扫描
					if t_data[2]==0:
						# 选择对应的扫描模板
						t_scan_temp=db_key.find_all("select tl_mode,tl_switch from w3a_Scan_Task_Template where id="+t_data[3]+" and tl_type=0")
						if t_scan_temp:
							# 判断该模板是否启用
							if t_scan_temp[1]==0:
								module_name=t_scan_temp[0].split(';')
								# 传入任务ID\任务目标\模块名称
								self.__loadPlugins(t_data[0],t_data[6],module_name)
							else:
								# 如果没有启用，则直接更新任务状态为异常停止
								db_key.execute_sql("update w3a_Scan_Task set t_status_num=4,t_status=100 where id="+temp_data[0])
								continue
						else:
							db_key.execute_sql("update w3a_Scan_Task set t_status_num=4,t_status=100 where id="+temp_data[0])
							continue

					elif t_data[2]==1:
						pass
			else:
				break

	# 程序加载模块
	def __loadPlugins(self,task_id,task_list,module_name):
		ScanFilepath=os.path.split(os.path.realpath(__file__))[0]
		if os.path.exists(ScanFilepath+"/plugin"):
			for filename in os.listdir(ScanFilepath+'/plugin'):
				if not filename.endswith('.py') or filename.startswith('_'):
					continue
				plugins_name=os.path.splitext(filename)[0]
				plugin=__import__("plugin."+plugins_name,fromlist=[plugins_name])
				clazz=plugin.getPluginClass()
				obj=clazz()
				obj.setScan_Main(self)
				#操作数据
				self.__runPlugins(filename)

	# 程序执行模块
	def __runPlugins(self,filename):
		# 获得模块名称
		plugins_name=os.path.splitext(filename)[0]
		# 导入模块
		plugin=__import__("plugin."+plugins_name,fromlist=[plugins_name])
		# 获得模块对象
		clazz=plugin.getPluginClass()
		o=clazz()
		# 把自身传给模块
		o.setScan_Main(self)
		## 开始处理
		# 任务列表	
		t=Db_module()
		# 每次运行先
		all_item=t.find_all("select * from w3a_Scan_Task where t_status_num=2")
		if all_item:
			print all_item
		else:
			print None
		#all_target=["www.cideko.com;www.henningkarlsen.com","www.moreanartscenter.org","www.tmd.go.th"]
		# 
		#while len(all_target)>0:
		#	for i in all_target:
				# 第一个是目标列表 第二个是模板参数
				# 针对模板会去数据库中查找对应的定义，如果定义了全部扫描，则所有的模块都会扫描
				# 否则只会扫描该扫的插件
				#o.start(i,1)
		#		o.start(i,1)
		#		o.stop()
		#		all_target.remove(i)
	
	# 标准屏幕输出
	def print_log(self,log):
		print "[*] %s" % log

	# 打印提示流/记录日志
	def print_load(self,item):
		flog="[*] %s" % item
		print flog
		self.log.w_log(flog)

if __name__=="__main__":
	scan_main=Scan_Main()
