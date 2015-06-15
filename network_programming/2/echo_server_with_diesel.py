#!/usr/bin/env python

import diesel
import argparse


class EchoServer(object):
	def handler(self,remote_addr):
		host,port = remote_addr[0],remote_addr[1]
		print "Echo client connected from:%s:%d" % (host,port)

		while True:
			try:
				message = diesel.until_eol()
				your_message = ': '.join(['You said',message])
				diesel.send(your_message)
			except Exception,e:
				print "Exception:",e

def main(server_port):
	app = diesel.Application()
	server = EchoServer()
	app.add_service(diesel.Service(server.handler,server_port))
	app.run()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Echo server example with Diesel")
	parser.add_argument('--port',action="store",dest="port",type=int,required=True)
	given_args = parser.parse_args()
	port = given_args.port
	main(port)