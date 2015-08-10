#!/usr/bin/env python

import socket
import sys

import argparse

host  = 'localhost'

def echo_client(port):
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server_address = (host,port)
	print "connectiong to %s port %s" % server_address
	sock.connect(server_address)

	try:
		message = "test message.This will be echoed"
		print "Sending %s" % message
		sock.sendall(message)
		amount_recevied = 0
		amount_expected = len(message)
		while amount_recevied < amount_expected:
			data = sock.recv(16)
			amount_recevied += len(data)
			print "Received:%s" % data 
	except socket.errno,e:
		print "Socket error:%s" % str(e)
	except Exception,e:
		print "other exception:%s" % str(e)
	finally:
		print "Closing connectiong to the server"
		sock.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="socket server example")
	parser.add_argument('--port',action="store",dest="port",type=int,required=True)
	given_args = parser.parse_args()
	port = given_args.port
	echo_client(port)