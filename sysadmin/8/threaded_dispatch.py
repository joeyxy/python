#!/usr/bin/env python
import subprocess
import ConfigParser
from threading import Thread
from Queue import Queue
import time

start = time.time()
queue = Queue()

def readConfig(file="config.ini"):
	ips = []
	cmds = []
	config = ConfigParser.ConfigParser()
	config.read(file)
	machines = config.items("machines")
	commands = config.items("commands")
	for ip in machines:
		ips.append(ip[1])
	for cmd in commands:
		cmds.append(cmd[1])
	return ips,cmds

def launcher(i,q,cmd):
	while True:
		ip = q.get()
		print "Thread %s: Running %s to %s" % (i,cmd,ip)
		subprocess.call("%s %s" % (cmd,ip),shell=True)
		q.task_done()


ips,cmds = readConfig()

if len(ips) < 25:
	num_threads = len(ips)
else:
	num_threads = 25


#start the thread pool
for i in range(num_threads):
	for cmd in cmds:
		worker = Thread(target=launcher,args=(i,queue,cmd))
		worker.setDaemon(True)
		worker.start()

print "main thread waiting"
for ip in ips:
	queue.put(ip)
queue.join()
#end = time.time()
#print "dispatch Completed in %s seconds" % end - start
