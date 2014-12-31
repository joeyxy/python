#!/usr/bin/env python

import socket

def print_machine_info():
	host_name = socket.gethostname()
	ip = socket.gethostbyname(host_name)
	print "your name is:%s" % host_name
	print "your ip is:%s" % ip

if __name__ ==  '__main__':
	print_machine_info()
