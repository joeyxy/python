#!/usr/bin/env python
#! -*- coding:utf-8 -*-
import urllib,urllib2
import json
import os
import shutil
CURR_DIR = os.path.abspath(os.path.dirname(__file__))
HOST_CONF_DIR = os.path.join(CURR_DIR,'hosts')
HOST_TMP = """define host{
    use linux-server
    host_name %(hostname)s
    check_command check-host-alive
    alias %(hostname)s
    address %(ipaddr)s
    contact_groups admins
}"""

def getHosts():
    url = 'http://192.168.1.4:8080/api/gethosts.json'
    return json.loads(urllib2.urlopen(url).read())
def initDir():
    if not os.path.exists(HOST_CONF_DIR):
        os.mkdir(HOST_CONF_DIR)
def writeFIle(f,s):
    with open(f,'w') as fd:
        fd.write(s)

def genNagiosHost(hostdata):
    initDir()
    conf = os.path.join(HOST_CONF_DIR,'hosts.cfg')
    hostconf = ""
    for hg in hostdata:
        for h in hg['members']:
            hostconf +=HOST_TMP %h
    writeFIle(conf,hostconf)
    return "ok"


def main():
    result = getHosts()
    if result['status'] == 0:
        print genNagiosHost(result['data'])
    else:
        print 'Error:%s' % result['message']
    if os.path.exists(os.path.join(HOST_CONF_DIR,'hosts.cfg')):
        os.chdir(HOST_CONF_DIR)
        shutil.copyfile('hosts.cfg','/data/hosts.cfg')


if __name__=="__main__":
    main()

