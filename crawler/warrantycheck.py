#!/usr/bin/env python
#use for dell server check the warranty date-joey 20140527
import os,sys
import urllib2
from BeautifulSoup import BeautifulSoup


def check(SN):
    url = "http://www.dell.com/support/home/en/zh/cnbsd1/product-support/servicetag/%s/maintain?s=BSD" % SN;
    print url
    req = urllib2.Request(url);
    resp = urllib2.urlopen(req);
    respHtml = resp.read();
    soup = BeautifulSoup(respHtml);
    date = soup.find('a',{'id':'VerifyReqRV'});
    #print "found date = %s",date
    if(date):
        wdate = date.string;
        print "SN:%s warranty date is: %s" % (SN,wdate);

def getsn():
    cmd = "dmidecode |grep Number: | head -1 | awk -F': ' '{print $2}'"
    sn = subprocess.Popen(cmd ,shell=True,stdout=subprocess.PIPE).stdout.readline().strip();
    #sn = subprocess.Popen("dmidecode |grep "Serial Nu" | head -1 | awk -F': ' '{print $2}'" ,shell=True,stdout=subprocess.PIPE).stdout.readline()
    check(sn);

if __name__="__main__":
    getsn();
