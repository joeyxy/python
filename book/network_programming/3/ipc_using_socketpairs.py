#!/usr/bin/env python


import socket
import os

BUFSIZE = 1024
def test_socketpair():
	parent,child = socket.socketpair()
	pid = os.fork()
	try:
		if pid:
			print "@parent,sending message..."
			child.close()
			parent.sendall("Hello from parent!")
			response = parent.recv(BUFSIZE)
			print "response from child:",response
			parent.close()
		else:
			print "@child,waiting for message from parent"
			parent.close()
			message = child.recv(BUFSIZE)
			print "message from parent:",message
			child.sendall("Hello from child!!")
			child.close()
	except Exception,err:
		print "Error:%s" % err 


if __name__ == '__main__':
	test_socketpair()