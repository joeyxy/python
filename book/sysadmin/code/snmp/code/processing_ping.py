#!/usr/bin/env python
from processing import Process, Queue, Pool
import time
import subprocess
from IPy import IP
import sys

q = Queue()
ping_out_queue = Queue()
snmp_out_queue = Queue()
ips = IP("10.0.1.0/24")
num_ping_workers = 10
num_snmp_workers = 10

def ping(i,q,out=out_queue):
    while True:
        if q.empty():
            sys.exit()
        #print "Process Number: %s" % i
        ip = q.get()
        ret = subprocess.call("ping -c 1 %s" % ip,
                        shell=True,
                        stdout=open('/dev/null', 'w'),
                        stderr=subprocess.STDOUT)
        if ret == 0:
            print "%s: is alive" % ip
            out.put(ip)
        else:
            pass

def snmp(i,q=ping_out_queue,out=snmp_out_queue)
    while True:
        if q.empty()
            sys.exit()
        #print "Process Number: %s" % i
        ip = q.get()
        ret = 
for ip in ips:
    q.put(ip)

for i in range(num_ping_workers):
    p = Process(target=ping, args=[i,q])
    p.start()

for i in range(num_snmp_workers):
    p = Process(target=f, args=[i,q])
    p.start()

print "main process joins on queue"
p.join()
print "Main Program finished"
