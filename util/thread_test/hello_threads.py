#!/usr/bin/env python

import threading
import datetime

class ThreadClass(threading.Thread):
	def run(self):
		now = datetime.datetime.now()
		print "%s says hello world at time:%s" % (self.getName(),now)


for i in range(2):
	t = ThreadClass()
	t.start()
