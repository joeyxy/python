#!/usr/bin/env python
#coding=utf-8
 
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import base64
 
class prpcrypt():
    def __init__(self,key):
        self.key = key
        self.iv = 'dingding20140901'
        self.mode = AES.MODE_CBC

    def encrypt(self,text):
        cryptor = AES.new(self.key,self.mode,b'dingding20140901')
        length = 16
        count = len(text)
        if count < length:
            add = (length-count)
            text = text + ('\0' * add)
        elif count > length:
            add = (length-(count % length))
            text = text + ('\0' * add)
        print "text is %s ,the length is :%s" % (text,len(text))
        self.ciphertext = cryptor.encrypt(text)
        print b2a_hex( self.iv + cryptor.encrypt(text)) 
        return b2a_hex(self.ciphertext)

     
    def decrypt(self,text):
        cryptor = AES.new(self.key,self.mode,b'dingding20140901')
        plain_text  = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')
 
if __name__ == '__main__':
    pc = prpcrypt('ee648bdb7d0b9698')
    #pc = prpcrypt('dingding20140901')
    import sys
    print len(sys.argv[1])
    e = pc.encrypt(sys.argv[1])
    d = pc.decrypt(e) 
    print "encrypt:",e
    print "decrypt:",d
