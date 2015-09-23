#!/usr/bin/env python

from scapy.all import *

def packet_callback(packet):
	print packet.show()

sniff(prn=packet_callback,count=1)
