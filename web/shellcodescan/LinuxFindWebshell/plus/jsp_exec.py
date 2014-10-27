#!/usr/bin/python2.7
#coding:utf-8

import re

rule = '((exec)\([\s|\n]{0,30}(request.getParameter\([\'"]{0,1}[\w]{0,15}[\'"]{0,1}\)|(.+[\s|\n]{0,30}\+[\s|\n]{0,30})?(\w{1,15})[\s|\n]{0,30}(.+)?)\))'
#匹配exec(request.getParameter('xx')或者exec(xx))或者exec('cmd /s'+ cmd)或者exec(strCommand,null,new File(strDir));
#rule1='((eval|assert)[\s|\n]{0,30}\((gzuncompress|gzinflate\(){0,1}[\s|\n]{0,30}base64_decode.{0,100})'
rule2='\s{0,10}=\s{0,10}.{0,10}(request.getParameter\(\s{0,10}[\'"]{0,1}[\w]{0,15}[\'"]{0,1}\s{0,10}\))'
#匹配xx = request.getParameter('cmd')或者xx = (String)request.getParameter('cmd')
rule3 = '\s{0,10}\[(\d)\]'
#匹配    strCommand[0]=strShell[0];
#		strCommand[1]=strShell[1];
#		strCommand[2]=strCmd;
#		Process p=Runtime.getRuntime().exec(strCommand,null,new File(strDir));对应正则result2
rule4 = '(\s{0,10}=\s{0,10}((request.getParameter\(\s{0,10}[\'"]{0,1}[\w]{0,15}[\'"]{0,1}\s{0,10}\))|(\w{1,20})))'
vararr=['request.getParameter']



def Check(filestr,filepath):
    if 'exec' in filestr:
        result = re.compile(rule).findall(filestr)
        for group in result:
            for var in vararr:
                if var in group[2]:
                    return result,'exec后门'
            resultson = re.search(group[4]+rule2,filestr)
            try:
                if len(resultson.groups())>0:
                    return ((resultson.group(),),(result[0][0],)),'exec(cmd)动态exec后门'
            except:
                pass

            result2 = re.compile(group[4] + rule3).findall(filestr)
            #匹配数组下标，即strCommand[]的下标
            for item in result2:
                resultson2 = re.compile(group[4]+"\["+item+"\]"+rule4).findall(filestr)
                #print resultson2
                #匹配strCommand[0]=xxx
                try:
                    for var in vararr:
                        if var in resultson2[0][0]:
                            s =  group[4]+resultson2[0][0]+','+result[0][0]
                            return s,'exec(cmd[])后门'
                    #如果xxx中包含可控变量request.getParameter，则是后门

                    resultson2_1 = re.compile(resultson2[0][3]+rule4).findall(filestr)

                    resultson2_1 = re.compile(resultson2[0][3]+rule4).findall(filestr)
                    #print resultson2_1
                    print filepath
                    #匹配动态参数strCommand[0]=xxx,下面的循环即匹配xxx=aaa;aaa=bbb;bbb=request.getParameter()这样的代码
                    resultson2_1_pre = ""
                    while resultson2_1[0][1] != '' and resultson2_1[0][1] != resultson2_1_pre:
                        resultson2_1_pre = resultson2_1[0][1]
                        #判断strCommand[0]的值与下一次的值是否一样，如果不一样，代表参数改变了。防止死循环。
                        for var in vararr:
                            if var in resultson2_1[0][0]:
                                s =  group[4]+resultson2_1[0][0]+','+result[0][0]
                                return s,'exec(cmd[])动态exec后门,动态参数'+group[4]
                        resultson2_1 = re.compile(resultson2_1[0][1]+rule4).findall(filestr)
                        #print resultson2_1

                except:
                    pass

    else:
        return None

    return None