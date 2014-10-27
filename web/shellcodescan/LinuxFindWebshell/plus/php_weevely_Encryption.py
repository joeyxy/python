#!/usr/bin/python2.7
#coding:utf-8

import re

#rule1='(preg_replace[\s\n]{0,10}\([\s\n]{0,10}((["\'].{0,15}[/@\'][is]{0,2}e[is]{0,2}["\'])|\$[a-zA-Z_][\w"\'\[\]]{0,15})\s{0,5},\s{0,5}.{0,40}(\$_(GET|POST|REQUEST|SESSION|SERVER)|str_rot13|urldecode).{0,30})'

rule1 = 'str_replace\("(.+)","","(.+)"\)'

def Check(filestr,filepath):

    if 'str_replace' in filestr:
        result1 = re.compile(rule1).search(filestr)
        try:
            type(result1)       #如果没搜索到，是NoneType，是不能type()的
            p1 = result1.group(1)
            p3 = result1.group(2)

            result = re.sub(p1, '', p3)     #查看str_replace的结果是不是还是str_replace
            if result == 'str_replace':
                return result1.group(),'weevely_Encryption后门'

        except:
            return None

    else:
        return None
