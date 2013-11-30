#!/usr/bin/env python

from socket import *
from time import ctime
#import sys

HOST=''
PORT=21567
BUFSIZ = 1024
ADDR = (HOST,PORT)


tcpSerSock = socket(AF_INET,SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

try:
	while True:
		print 'waiting for connection...'
		tcpCliSock,addr = tcpSerSock.accept()
		print 'connected from:',addr
		print 'tcpfd:%s' % tcpCliSock

		while True:
			data = tcpCliSock.recv(BUFSIZ)
			if not data:
				break
			print data
			'''if data in [404,300]:
				tcpCliSock.close()
				tcpSerSock.close()
				sys.exit()'''
			tcpCliSock.send('[%s] %s' % (ctime(),data))
		tcpCliSock.close()
except KeyboardInterrupt:
	print "stop by crtl+c\n"
	tcpSerSock.close()

