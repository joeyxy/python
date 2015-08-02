#!/usr/bin/env python 
#check the pic number
#joeyxy83@gmail.com
#20150329


import re
import time
import os
import json
import urllib
import urllib2
import requests
import pytesseract
from PIL import Image
import argparse
import captcha_ock


def downloadImg(pic_url):
    if os.path.exists('./pic/'):
        pass
    else:
        os.makedirs('./pic/')
    pic_file = int(time.time())
    print '[+] Download Picture: {}'.format(pic_url)
    try:
        resp = requests.get(pic_url, verify=False, timeout=5)
    except:
        resp = requests.get(pic_url, verify=False, timeout=3)
    with open("./pic/%s.png"%pic_file, 'wb') as fp:
        fp.write(resp.content)
    return pic_file

def check_img(url):
	pic_file = downloadImg(url)
	img=Image.open('./pic/'+str(pic_file)+'.png')
	vcode = pytesseract.image_to_string(img)
	print vcode


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='using pytesseract check the captcha')
    parser.add_argument('--url',action="store",dest="url")

    given_args = parser.parse_args()
    check_img(given_args.url)
    captcha_ock.check_code(given_args.url)