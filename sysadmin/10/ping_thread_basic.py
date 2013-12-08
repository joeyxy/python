#!/usr/bin/env python

from threading import Thread
import subprocess
from Queue import Queue

num_threads = 3
queue = Queue()
ips = ["192.168.1.1","192.168.1.2","192.168.1.3","192.168.1.4","192.168.1.5","192.168.1.6"]

def pinger(i,q):
    """ping subnet"""
    while True:
        ip = q.get()
        print "Thread %s:Pinging %s" % (i,ip)
        ret = subprocess.call("ping -c 1 %s" % ip,shell=True,stdout=open('/dev/null','w'),stderr=subprocess.STDOUT)
        if ret == 0:
            print "%s: is alive" % ip
        else:
            print "%s: did not respond" % ip
        q.task_done()
        print "Thread %s: done at %s" % (i,ip)


for i in range(num_threads):
    worker = Thread(target=pinger,args=(i,queue))
    worker.setDaemon(True)
    worker.start()


for ip in ips:
    queue.put(ip)


print "Main thread waiting"
queue.join()
print "Done"
