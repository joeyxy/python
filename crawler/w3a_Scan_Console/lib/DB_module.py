#!/usr/bin/python
# vim: set fileencoding=utf-8:

###########################################
#
# db数据库类(实现数据库操作)
#
###########################################

import sys
import ConfigParser
import MySQLdb as mdb
import os

class Db_module:
	def __init__(self):
		confini_path=os.path.split(os.path.realpath(__file__))[0]+"/../conf/db.ini"
		cf = ConfigParser.ConfigParser()
		cf.read(confini_path)
		db_host = cf.get("mysql_db", "host")
		db_port = cf.getint("mysql_db", "port")
		db_user = cf.get("mysql_db", "username")
		db_pwd = cf.get("mysql_db", "password")
		db_data=cf.get("mysql_db","db_name")
		try:
			self.con=mdb.connect(db_host,db_user,db_pwd,db_data)
			self.cur=self.con.cursor()
		except:
			print "[*] DB Connect Error"

	# 查找所有数据
	def find_all(self,sql_script):
		try:
			self.cur.execute(sql_script)
			results=self.cur.fetchall()
			if results==None:
				return None
			else:
				return results
		except:
			print "[*] DB FindAll Error SQL: %s" % sql_script

	# 查找单条数据
	def find_item(self,sql_script):
		try:
			self.cur.execute(sql_script)
			return self.cur.fetchone()
		except:
			print "[*] DB FindItem Error SQL: %s" % sql_script

	# 执行操作
	def execute_sql(self,sql_script):
		try:
			self.cur.execute(sql_script)
			self.con.commit()
			return True
		except:
			print "[*] DB Exec Error SQL:  %s" % sql_script

	# 统计数据
	def select_count(self,db_table):
		try:
			sql_script="select count(*) from %s" % db_table
			self.cur.execute(sql_script)
			results=self.cur.fetchone()
			return results[0]
		except:
			print "[*] DB count execute Error: %s" % sql_script
