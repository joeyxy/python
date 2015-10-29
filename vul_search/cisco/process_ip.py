#!/usr/bin/env python
#process ip list transfer to ip/mask format


import sys
import os 
import math

global debug
debug = 1

def main(file):
	ips=[]
	f = open(file,'r')
	for item in f:
		mask = item.split()[1]
		if debug:print mask
		new_mask = 32-int(math.log(float(mask),2))
		if debug:print new_mask
		new_ip = "%s/%s" %(item.split()[0],new_mask)
		if debug: print new_ip
		ips.append(new_ip)

	f.close()

	new = open('./ip.txt', 'w')
	for ip in ips:
		new.write('%s\n'%ip)

	new.close()



if __name__ == '__main__':
	if len(sys.argv) < 1:
		sys.exit(1)
	file = sys.argv[1]
	main(file)