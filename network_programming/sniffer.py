import os
import socket

HOST = '192.168.10.70'

def sniffing(host,win,socket_port):
	while 1:
		sniffer = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_port)
		sniffer.bind((host,0))
		sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)

		if win == 1:
			sniffer.ioctl(socket.SIO_RCVAL,socket_RCVALL_ON)

		print sniffer.recvfrom(65535)

def main(host):
	if os.name == 'nt':
		sniffing(host, 1, socket.IPPROTO_IP)
	else:
		sniffing(host, 0, socket.IPPROTO_ICMP)

if __name__ == '__main__':
	main(HOST)
