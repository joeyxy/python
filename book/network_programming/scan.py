import threading
import time
import socket
import os
import struct
from netaddr import IPNetwork,IPAddress
from ICMPHeader import ICMP
import ctypes

HOST = '192.168.10.70'
SUBNET ='192.168.10.0/24'

MESSAGE = 'helloooo'

def udp_sender(SUBNET,MESSAGE):
	time.sleep(5)
	sender = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	for ip in IPNetwork(SUBNET):
		try:
			sender.sendto(MESSAGE,("%s" % ip,65512))
		except:
			pass


def main():
	t = threading.Thread(target=udp_sender,args=(SUBNET,MESSAGE))
	t.start()

	socket_protocol = socket.IPPROTO_ICMP
	sniffer = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocol)
	sniffer.bind((HOST,0))
	sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)

	while 1:
		raw_buffer = sniffer.recvfrom(65565)[0]
		ip_header = raw_buffer[0:20]
		iph = struct.unpack('!BBHHHBBH4s4s',ip_header)

		version_ihl = iph[0]
		ihl = version_ihl & 0xF
		iph_length = ihl * 4
		src_addr = socket.inet_ntoa(iph[8])

		buf = raw_buffer[iph_length:iph_length+ctypes.sizeof(ICMP)]
		icmp_header = ICMP(buf)

		if icmp_header.code ==3 and icmp_header.type ==3:
			if IPAddress(src_addr) in IPNetwork(SUBNET):
				if raw_buffer[len(raw_buffer) - len(MESSAGE):] == MESSAGE:
					print ("host up: %s" % src_addr)


if __name__ == '__main__':
	main()