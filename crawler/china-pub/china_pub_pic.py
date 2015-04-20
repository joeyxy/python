#!/usr/bin/env python 
#check the pic number
#joeyxy83@gmail.com
#20150329


import re
import time
import json
import urllib
import urllib2
import requests
import pytesseract
from PIL import Image


def downloadImg():
    pic_file = int(time.time())
    pic_url = "http://www.china-pub.com/member/register/imgchk/validatecode.asp"
    print '[+] Download Picture: {}'.format(pic_url)
    try:
        resp = requests.get(pic_url, verify=False, timeout=5)
    except:
        resp = requests.get(pic_url, verify=False, timeout=3)
    with open("./pic/%s.png"%pic_file, 'wb') as fp:
        fp.write(resp.content)
    return pic_file

def check_img():
	pic_file1 = downloadImg()
	pic_file = 2
	img=Image.open('./pic/'+str(pic_file)+'.png')
	vcode = pytesseract.image_to_string(img)
	print vcode


if __name__ == '__main__':
	check_img()



