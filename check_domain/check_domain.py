#!/usr/bin/python
# coding: utf-8
# author: GuangHongwei
# date: 2014/7/28
# mail: lastimac@gmail.com

import time
import urllib
import re

api = "http://panda.www.net.cn/cgi-bin/check.cgi?area_domain=%s"  # api地址
string = "abcdefghijklmnopqrstuvwxyz1234567890"                   # 所有字母
string_len = len(string)                                          # 长度
fname = 'name.txt'                                                # 还没被注册的域名写入该文件
suffix = '.com'                                                   # 域名后缀
domain_lenth_range = range(3, 5)                                  # 字母组合的长度，3到5但不包括5


def min(num):
    """初始化第一个值数字列表"""
    name = []
    for i in range(num):
        name.append(0)
    return name

def max(num, max_num):
    """返回最大的值数字列表"""
    name =  []
    for i in range(num):
        name.append(max_num)
    return name
    
def num_2_string(name, string):
    """将数字列表转化为字母组合列表"""
    new_name = []
    for i in name:
        new_name.append(string[i])
    return ''.join(new_name)

	
def is_ava(domain):
    """判断该域名是否被注册"""
    data = urllib.urlopen(api % domain).read()
    ava_pattern = re.compile(r'<original>(.*) : .*</original>')
    perm_pattern = re.compile(r'Forbidden')
    result = ava_pattern.findall(data)
    if '210' in result:
        print '%s ---------> Ok' % domain
        return True
    elif '211' in result:
        print '%s ---------> No' % domain
        return False
    else:
        print 'Forbidden'
        return False
        
def domain_name(num):
    """域名组合生成器"""
    name = min(num)
    last = max(num, string_len-1)
    while True:
        yield num_2_string(name, string)
        if name == last:
            break
        name[num-1] += 1
        while string_len in name:
            index = name.index(string_len)
            name[index] = 0
            name[index-1] += 1
            
def run(domain_lenth):
    """执行，如果每被注册就写到文件中"""
    f = open(fname, 'a')
    for domain in domain_name(domain_lenth):
        domain += suffix
        if is_ava(domain):
            f.write('%s\n' % domain)
            f.flush()
        time.sleep(0.5)
    
 
if __name__ == '__main__':
    """最终执行， 循环执行每种长度组合"""
    for i in domain_lenth_range:
        run(i)