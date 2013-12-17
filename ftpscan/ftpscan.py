#!/usr/bin/env python
 
"""
FtpScan.py - Scans for FTP servers allowing Anonymous Login
          Written by Sotd - twitter.com/#!/Sotd_
          Performance update by q8r9e4
"""
import sys
import threading
import Queue
import ftplib
import socket
import time
 
 
 
global ftpqueue
ftpqueue = Queue.Queue()
 
 
class Ftp(threading.Thread):
    """Handles connections"""
 
    def __init__(self, queue):
        threading.Thread.__init__(self)  
        self.queue = queue
         
    def run(self):
        """Connects and checks for anonymous login"""
        while True:
            try:
                ip_add = self.queue.get(False)
            except Queue.Empty:
                break
            try:
                ftp = ftplib.FTP(ip_add)
                ftp.login()
            except ftplib.all_errors:
                print 'Not Working: %s' % (ip_add)
            else:
                print 'Working: %s' % (ip_add)
                write = open('Ftp.txt', "a+")
                write.write(ip_add + '\n')
                write.close()  
                ftp.quit()
            finally:
                self.queue.task_done()  
 
class Scanner(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)  
        self.queue = queue
 
    def run(self):
        """Connects and checks for anonymous login"""
        global ftpqueue
        while True:
            try:
                ip_add = self.queue.get(False)
            except Queue.Empty:
                break
 
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                check = s.connect_ex((str(ip_add), 21))
                if check == 0:
                    ftpqueue.put(ip_add)
                else:
                    print 'No FTP: %s' % (ip_add)
                s.close()
 
            finally:
                self.queue.task_done()
       
 
def iprange():
    """Creates list of Ip's from Start_Ip to End_Ip and checks for port 21"""
    start_ip = sys.argv[1]
    end_ip = sys.argv[2]
    ip_range = Queue.Queue()
    start = list(map(int, start_ip.split(".")))
    end = list(map(int, end_ip.split(".")))
    tmp = start
    socket.setdefaulttimeout(3)
   
    ip_range.put(start_ip)
    while tmp != end:
        start[3] += 1
        for i in (3, 2, 1):
            if tmp[i] == 256:
                tmp[i] = 0
                tmp[i-1] += 1
        ip_range.put(".".join(map(str, tmp)))
 
    for i in range(10):
        time.sleep(0.1)
        thread = Scanner(ip_range)
        thread.setDaemon(True)
        thread.start()
    ip_range.join()
 
    if ftpqueue.empty():
        print '\nNo FTP servers found\n'
        sys.exit(0)
 
    for i in range(10):
        thread = Ftp(ftpqueue)
        thread.setDaemon(True)
        thread.start()
    ftpqueue.join()
 
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: ./FtpScan <start_ip> <end_ip>'
        print 'Example: ./FtpScan 127.0.0.1 127.0.0.5'
        sys.exit(1)
    else:
        iprange()
