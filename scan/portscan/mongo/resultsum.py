#!/usr/bin/env python
# encoding:utf8
# author:f2#ff0000team

s = set()
fo1 = open('./port27017_aliip_1.txt', 'wb')
for eachLine in open('port27017_aliip.txt', 'rbU'):
    s.add(eachLine)
fo1.writelines(s)

# 统计
d = {}
for eachLine in s:
    ip, country = eachLine.strip().split('---')
    d[country] = d.get(country, 0) + 1
fo2 = open('port27017_aliip_2.txt', 'wb')
for x in sorted(d.iteritems(), key=lambda i: i[1], reverse=True):
    fo2.write(x[0]+'\t'+str(x[1])+'\n')
