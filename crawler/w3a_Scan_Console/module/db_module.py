#!/usr/bin/python
# vim: set fileencoding=utf-8:

###########################################
#
#   db数据库类(实现数据库操作)
#
###########################################

import sys
import ConfigParser
import MySQLdb as mdb


class Db_Connector:
    def __init__(self, config_file_path):
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
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
    def find_all(self,sql_script):
        try:
            self.cur.execute(sql_script)
            return self.cur.fetchall()
        except:
            print "[*] DB FindAll Error"
    def find_item(self,sql_script):
        try:
            self.cur.execute(sql_script)
            return self.cur.fetchone()
        except:
            print "[*] DB FindItem Error"
    def insert_item(self,sql_script):
        try:
            self.cur.execute(sql_script)
            self.con.commit()
            return True
        except Exception, e:
            print '[*] DB Insert Into Error'
    def update_item(self,sql_script):
        try:
            self.cur.execute(sql_script)
            self.con.commit()
            return True
        except Exception, e:
            print "[*] DB Update Error"
