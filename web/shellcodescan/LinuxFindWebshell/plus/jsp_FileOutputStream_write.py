#!/usr/bin/python2.7
#coding:utf-8

import re

rule = '(FileOutputStream\(.+\)\.write\((request.getParameter\([\'"]{0,1}([\w]{0,15})[\'"]{0,1}\)|(\w{1,15})).getBytes\(\)\))'
#匹配FileOutputStream(application.getRealPath("\")+request.getParameter("f"))).write(request.getParameter("aa").getBytes()
#或者FileOutputStream(application.getRealPath("\")+request.getParameter("f"))).write(cc.getBytes())
#rule1='((eval|assert)[\s|\n]{0,30}\((gzuncompress|gzinflate\(){0,1}[\s|\n]{0,30}base64_decode.{0,100})'
rule2='\s{0,10}=\s{0,10}(request.getParameter\(\s{0,10}[\'"]{0,1}[\w]{0,15}[\'"]{0,1}\s{0,10}\))'
#匹配xx = request.getParameter('cmd')
vararr=['request.getParameter']



def Check(filestr,filepath):
    if 'write(' in filestr:
        result = re.compile(rule).findall(filestr)
        for group in result:
            for var in vararr:
                if var in group[1]:
                    return result,'write后门'
            resultson = re.search(group[1]+rule2,filestr)
            try:
                if len(resultson.groups())>0:
                    return ((resultson.group(),),(result[0][0],)),'FileOutputStream().write(cmd)动态write后门'
            except:
                continue
    else:
        return None

    return None