#!/usr/bin/env python

import argparse
import socket
import errno
from time import time as now

DEFAULT_TIMEOUT = 120
DEFAULT_SERVER_HOST = 'localhost'
DEFAULT_SERVER_PORT = 80


class NetServiceCHecker(object):
	def __init__(self,host,port,timeout=DEFAULT_TIMEOUT):
		self.host = host
		self.port = port
		self.timeout = timeout
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


	def end_wait(self):
		self.sock.close()

	def check(self):
		if self.timeout:
			end_time = now() + self.timeout


		while True:
			try:
				if self.timeout:
					next_timeout = end_time - now()
					if next_timeout < 0:
						return False
					else:
						print "Setting socket next timeout %ss" %round(next_timeout)
						self.sock.settimeout(next_timeout)
				self.sock.connect((self.host,self.port))
			except socket.timeout,err:
				print "Exception1:%s" % err
				if self.timeout:
					return False
			except socket.error,err:
				print "Exception2:%s" % err
			else:
				self.end_wait()
				return True

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="wait for network service")
	parser.add_argument('--host',action="store",dest="host",default=DEFAULT_SERVER_HOST)
	parser.add_argument('--port',action="store",dest="port",type=int,default=DEFAULT_SERVER_PORT)
	parser.add_argument('--timeout',action="store",dest="timeout",type=int,default=DEFAULT_TIMEOUT)
	given_args = parser.parse_args()
	host,port,timeout = given_args.host,given_args.port,given_args.timeout
	service_checker = NetServiceCHecker(host, port,timeout=timeout)
	print "Checking for network server %s:%s ..." % (host,port)
	if service_checker.check():
		print "Service is available again!"






