#!/usr/bin/env python
from Crypto.Cipher import AES
from Crypto import Random
from binascii import b2a_hex, a2b_hex

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[0:-ord(s[-1])]
 
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
 
if __name__== "__main__":
    key = "ee648bdb7d0b9698"
    ciphertext = "8d24f6708eeccda90827d0c2f47a1fe4";
    decryptor = AESCipher(key)
    print decryptor.encrypt('9698658532')
    plaintext = decryptor.decrypt(ciphertext)
    print "%s" % plaintext