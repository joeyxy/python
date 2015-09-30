#!/usr/bin/env python
import socket
import sys
import threading
import time

NORMAL = 0
ERROR = 1
TIMEOUT = 5

def ping(ip , port , timeout=TIMEOUT):
	try:
		cs=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		cs.settimeout(float(timeout))
		address=(str(ip),int(port))
		status = cs.connect_ex((address))
		if status == NORMAL :
			print "%d is NORMAL" %port
	except Exception ,e:
		print ERROR
		print "error:%s" %e
		return ERROR
	cs.close()
	return NORMAL

 
class Scan(threading.Thread):
    def __init__(self , ip , timeout):
        threading.Thread.__init__(self)
	self.ip = ip
	self.timeout = timeout

    def run(self):
        global p_begin , p_end , mutex
        threadname = threading.currentThread().getName()
        while 1:
            mutex.acquire()
            p_begin += 1
            if p_begin >  p_end:
		    mutex.release()
		    break
            mutex.release()
	    ping(self.ip , p_begin , self.timeout)

	
 
if __name__ == '__main__':
    if len(sys.argv) < 4:
	print 'format:urlbegin portbegin portend timeout'

    urlbegin = str(sys.argv[1])
    portbegin = int(sys.argv[2])
    portend = int(sys.argv[3])
    timeout = float(sys.argv[4])

    global p_begin , p_end, mutex
    threads = []
    num = 10
    p_begin = portbegin 
    p_end = portend
    mutex = threading.Lock()
    for x in xrange(0 , num):
        t_scan = Scan(urlbegin , timeout)
	t_scan.setDaemon(True)
        threads.append(t_scan)
    for t in threads:
        t.start()
    for t in threads:
        t.join()  

