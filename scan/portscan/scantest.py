#!/usr/bin/env python
import socket

ports = [22,21,53,80,443,8081,8088,8788,4399,9200,9201,22001,9300,9301]
hosts = ['58.220.7.34','58.220.7.35','58.220.7.36','58.220.7.37','58.220.7.38','58.220.7.39','58.200.7.40','58.220.7.41','58.220.7.47','58.220.7.48','58.220.7.49']

for host in hosts:
	for port in ports:
		try:
			s=socket.socket()
			s.settimeout(3)
			#print "[+]attempting to connect to " + host+":"+str(port)
			s.connect((host,port))
			s.send('absdkfbsdafblabldsfdbfhasss /n')
			banner = s.recv(1024)
			if banner:
				print "[+] "+host + ":"+str(port)+" open:\n"+banner
			s.close()
		except:
			pass

