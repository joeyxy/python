#!/usr/bin/env python
#create at:20131121 joey joeyxy83@gmail.com
#for check the server services status
#file format in each line: ip:port

#import time
#import socket,re,urllib,urllib2,os,sys
#import subprocess
import socket
from threading import Thread
from Queue import Queue
import sys
results = []

timeout = 5
ip_queue = Queue()
num_threads = 100 


def scan_port(iq,timeout=timeout):
    while True:
        line=iq.get()
        ip=line.split(':')[0].strip('\n')
        port=line.split(':')[1].strip('\n')
        try:
            #print "ip:%s,port:%s"% (ip,port)
            cs=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            cs.settimeout(float(timeout))
            address=(str(ip),int(port))
            status=cs.connect_ex(address)
            if status == 0:
                result = "host:%s port:%s ok" % (ip,port)
                results.append(result)
                print "host:%s port:%s ok" % (ip,port)
                iq.task_done()
            else:
                result = "host:%s port:%s ok" % (ip,port)
                results.append(result)
                print "host:%s port:%s down" % (ip,port)
                iq.task_done()

        except Exception,e:
            print "error:%s" % e
            iq.task_done()
        except KeyboardInterrupt:
            print "You pressed Ctrl+c"
            sys.exit(2)

if __name__=="__main__":
    if len(sys.argv) < 2:
        print __doc__
        sys.exit(1)
    file=sys.argv[1]
    f =open(file,'r')

    #place ip into ip_queue
    for eachline in f:
        ip_queue.put(eachline)

    f.close()
    #spawn pool of scan_port threads
    if ip_queue.qsize() < num_threads:
        num_threads = ip_queue.qsize()

    for i in range(num_threads):
        worker = Thread(target=scan_port,args=(ip_queue,5))
        worker.setDaemon(True)
        worker.start()

    ip_queue.join()
    print "print results"
    for i in results:
            print i

