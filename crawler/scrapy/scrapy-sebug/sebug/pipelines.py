# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request
from scrapy.exceptions import DropItem
#from scrapy.contrib.pipeline.images import ImagesPipeline
import time
import MySQLdb
import MySQLdb.cursors
import socket
import select
import sys
import os
import errno

class SebugPipeline(object):
    def __init__(self):
	self.dbpool = adbapi.ConnectionPool('MySQLdb',
		db = 'sebug',
		user = 'test',
		passwd = 'test',
		cursorclass = MySQLdb.cursors.DictCursor,
		charset = 'utf8',
		use_unicode = False
	)    

    def process_item(self, item, spider):
	query = self.dbpool.runInteraction(self._conditional_insert,item)
	return item

    def _conditional_insert(self,tx,item):
	tx.execute('insert into vulninfo values (%s, %s, %s, %s, %s)', (item['ssv'],item['appdir'],item['title'],item['content'],item['publishdate']))

