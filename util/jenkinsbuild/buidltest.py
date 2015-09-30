#!/usr/bin/env python
#used for start the jenkins job build-20140930 joey.x@qq.com

import jenkinsapi
from jenkinsapi.jenkins import Jenkins
import os,sys
from termcolor import colored

def build_job(name):
    api=Jenkins('http://192.168.2.39:8080','','test123!')
#    job=api.get_job('deploy_dh_client_resource_to_test')
    job=api.get_job(name)
    try:
        result = job.invoke(build_params=None, cause=None)

        print result
    except Exception,e:
        print colored("catch the exption:%s" % e,'red')

def main():
    if len(sys.argv) == 2:
        build_job(sys.argv[1])
    else:
        print colored("useage:%s jobname" % sys.argv[0],'red')
        sys.exit(1)


if __name__ == '__main__':
    main()
