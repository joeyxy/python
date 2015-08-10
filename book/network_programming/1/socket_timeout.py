#!/usr/bin/env python

import socket

def test_socket_timeout():
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	print "default socket timeout:%s" % s.gettimeout()
	s.settimeout(100)
	print "new socket timeout:%s" % s.gettimeout()

if __name__ == '__main__':
	test_socket_timeout()
