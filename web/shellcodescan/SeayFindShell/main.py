#!/usr/bin/python2.7
#coding:gbk
#author:Seay
#blog:www.cnseay.com

import os
import sys
import time

#reload(sys)
#sys.setdefaultencoding('gbk')

plusarr=[] #插件列表
backdoor_count=0

def loadplus():
    #if len(plusarr)>0:
    #    for plus in plusarr:
    #        del sys.modules['plus.'+plus]
    #    del plusarr[:]

    for root,dirs,files in os.walk("plus"):
        for filespath in files:
            if filespath[-3:] == '.py':
                plusname = filespath[:-3]
                if plusname=='__init__':
                    continue
                __import__('plus.'+plusname)
                plusarr.append(plusname)

def Scan(path):
    loadplus() #动态加载插件
    global backdoor_count
    for root,dirs,files in os.walk(path):
        for filename in files:
            filepath = os.path.join(root,filename)
            if os.path.getsize(filepath)<500000:
                    for plus in plusarr:
                        file= open(filepath,"rb")
                        filestr = file.read()
                        file.close()
                        result = sys.modules['plus.'+plus].Check(filestr,filepath)

                        if result!=None:
                            print '文件: ',
                            print filepath
                            print '后门描述: ',
                            print result[1]
                            print '后门代码: ',
                            for code in result[0]:
                                print code[0][0:100]
                            print '最后修改时间: '+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(filepath)))+'\n\n'
                            backdoor_count= backdoor_count+1
                            break

def ScanFiletime(path,times):
    global backdoor_count
    times = time.mktime(time.strptime(times, '%Y-%m-%d %H:%M:%S'))
    print '########################################'
    print '文件路径           最后修改时间   \n'

    for root,dirs,files in os.walk(path):
        for curfile in files:
            if '.' in curfile:
                suffix = curfile[-4:].lower()
                filepath = os.path.join(root,curfile)
                if suffix=='.php' or suffix=='.jsp':
                    FileTime =os.path.getmtime(filepath)
                    if FileTime>times:
                        backdoor_count +=1
                        print filepath+'        '+ time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(FileTime))

if __name__ == "__main__":
    print '----------------------------------------'
    print """
         ╭╮　　　　　　　╭╮　　
       　││　　　　　　　││　　
       ╭┴┴———————┴┴╮
       │　　　　　　　　　　　│　　　
       │　　　　　　　　　　　│　　　
       │　●　　　　　　　●　│
       │○　　╰┬┬┬╯　　○│
       │　　　　╰—╯　　　　│　
       ╰——┬Ｏ———Ｏ┬——╯
       　 　╭╮　　　　╭╮　　　　
       　 　╰┴————┴╯
----┏━☆━━━━━━━━━━━━┓----
----┃ SeayFindShell 1.0      ┃----
----┃ Author:Seay                ┃----
----┃ SITE:www.cnseay.com        ┃----
----┗━━━━━━━━━━━━━━┛----
    """

    if len(sys.argv)!=3 and len(sys.argv)!=2:
        print '【参数错误】'
        print '\t按恶意代码查杀: '+sys.argv[0]+' 目录名'
        print '\t按修改时间查杀: '+sys.argv[0]+' 目录名 最后修改时间(格式:"2013-09-09 12:00:00")'
        exit()

    if os.path.lexists(sys.argv[1])==False:
        print '【错误提示】：指定的扫描目录不存在--- '
        exit()

    if len(sys.argv)==2:
        print '\n\n【开始查杀】'
        print sys.argv[1]+'\n'
        Scan(sys.argv[1])
        print '【查杀完成】'
        print '\t后门总数: '+str(backdoor_count)
    else:
        print '\n\n【开始查找】'
        print sys.argv[1]+'\n'
        ScanFiletime(sys.argv[1],sys.argv[2])
        print '\n【查找完成】'
        print '\t文件总数: '+str(backdoor_count)