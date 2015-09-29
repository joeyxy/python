#!/usr/bin/env python


import requests
import re
import sys
import os
import argparse
import threadpool as tp
from Queue import Queue

queue = Queue()

global debug
debug =0

class sjgo(object):
    def __init__(self,sid,eid):
        self.sid = sid
        self.eid = eid
        self.url = []
        self.username = []
        
    def getusername(self):
        for i in range(self.sid,self.eid):
            url = "http://www.sjgo365.com/%s.html" % i
            self.url.append(url)
            if debug:print url
        print len(self.url)
        pool = tp.ThreadPool(50)
        reqs = tp.makeRequests(start,self.url)
        [pool.putRequest(req) for req in reqs]
        pool.wait()  
    def write_file(self):
        while queue.qsize() > 1:
            url = queue.get()
            f = open("valid_url.list", 'a+')
            f.write('%s\n'% url)
            f.close()
    
    

        

def start(url):
    try:
        req = requests.get(url,timeout=30,allow_redirects=False)
        code = req.status_code
        if code == 200:
            if debug: print "valid url:%s" % url
            queue.put(url)
        else:
            if debug: print "error num!"
    
    except requests.RequestException as e:
        if debug:print "request error:%s" % e  
        pass
            
    
    
    
    




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="get the ip list and test ssl")
    parser.add_argument('--sid',action="store",dest="sid",type=int,default="27739000")
    parser.add_argument('--eid',action="store",dest="eid",type=int,default="27739673")
    given_args = parser.parse_args()
    test=sjgo(sid=given_args.sid,eid=given_args.eid)
    test.getusername()
    test.write_file()




