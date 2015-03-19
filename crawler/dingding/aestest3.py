#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from Crypto.Cipher import AES
from Crypto import Random
import binascii
from binascii import b2a_hex, a2b_hex
from base64 import b64encode, b64decode

class MyCrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC
        self.padding = '\0'
 
    def encrypt(self, text):
        cryptor = AES.new(self.key,self.mode,b'dingding20140901')
        length = 16
        count = text.count('')
        if count < length:
            add = (length - count) + 1
            text += (self.padding * add)
        elif count > length:
            add = (length - (count % length)) + 1
            text += (self.padding * add)
        self.ciphertext = cryptor.encrypt(text)
        return self.ciphertext
 
    def decrypt(self, text):
        cryptor = AES.new(self.key,self.mode,b'dingding20140901')
        plain_text = cryptor.decrypt(text)
        return plain_text.rstrip("\0")
 
if __name__ == '__main__':
    key = 'ee648bdb7d0b9698'
    data = '9698658532'
    ec = MyCrypt(key)
    encrpt_data = ec.encrypt(data)
    decrpt_data = ec.decrypt(encrpt_data)
    print encrpt_data, decrpt_data, decrpt_data == data
 
    
    print b64encode(encrpt_data)
    print b2a_hex(encrpt_data)