#!/usr/bin/env python

from gevent.server import StreamServer

def handle(sock,address):
    sock.recv(1000)
    sock.send("HTTP/1.1 200 OK\r\n\r\nfafdsa")
    

server = StreamServer(('',8000),handle);
server.serve_forever();