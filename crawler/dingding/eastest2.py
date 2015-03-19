
from Crypto.Cipher import AES
from Crypto import Random
import binascii
from binascii import b2a_hex, a2b_hex

def AES_File(fs):
    key = b'ee648bdb7d0b9698' #16-bytes password
    iv = b'dingding20140901'
    #iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    print 'if fs is a multiple of 16...'
    #if fs is a multiple of 16
    x = len(fs) % 16
    print 'the fs len is:', len(fs)
    print 'The num to padded is : ', x
    if x != 0:
        fs_pad = fs + '\0'*(16 - x) #It shoud be 16-x not 
        print 'fs_pad is : ', fs_pad
        print len(fs_pad)
        print len(fs_pad)%16
    else:
    	fs_pad = fs
    msg = iv + cipher.encrypt(fs_pad)
    print 'File after AES is like...', binascii.b2a_hex(msg)
    print b2a_hex(cipher.encrypt(fs_pad))
    return b2a_hex(msg)

#Create a Test Src File and Get FileSteam
fc_msg1 = AES_File('9698658532')
print fc_msg1


