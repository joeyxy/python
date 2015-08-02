#!/usr/bin/env python

import argparse
import socket
import sys

def scan_hosts(host,start_port,end_port):
	try:
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	except socket.error,err_msg:
		print 'Socket creating failed.Error code:'+str(err_msg[0])+'Error message:'+err_msg[1]
		sys.exit()

	try:
		remote_ip = socket.gethostbyname(host)
	except socket.error,error_msg:
		print error_msg
		sys.exit()

	end_port +=1
	for port in range(start_port,end_port):
		try:
			sock.connect((host,port))
			print 'Port'+str(port)+'is open'
			sock.close()
			sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		except socket.error:
			print "error:port %s" % port 
			pass


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Remote Port scanner')
	parser.add_argument('--host',action="store",dest="host",default='localhost')
	parser.add_argument('--start-port',action="store",dest="start_port",default=1,type=int)
	parser.add_argument('--end-port',action="store",dest="end_port",default=100,type=int)

	given_args = parser.parse_args()
	host,start_port,end_port = given_args.host,given_args.start_port,given_args.end_port
	scan_hosts(host, start_port, end_port)