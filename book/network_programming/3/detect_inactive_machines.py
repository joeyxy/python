#!/usr/bin/env python

import argparse
import time
import sched
from scapy.all import sr,srp,IP,UDP,ICMP,TCP,ARP,Ether
RUN_FREQUENCY = 10
scheduler = sched.scheduler(time.time, time.sleep)

def detect_inactive_hosts(scan_hosts):
	global scheduler
	scheduler.enter(RUN_FREQUENCY, 1, detect_inactive_hosts, (scan_hosts,))
	inactive_hosts = []
	try:
		ans,unans = sr(IP(dst=scan_hosts)/ICMP(),retry=0,timeout=1)
		ans.summary(lambda(s,r):r.sprintf("%IP.src% is alive"))
		for inactive in unans:
			print "%s is inactive" % inactive.dst
			inactive_hosts.append(inactive.dst)

		print "Total %d hosts are inactive" % (len(inactive_hosts))

	except KeyboardInterrupt:
		exit(0)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Python networking utils')
	parser.add_argument('--scan-hosts',action="store",dest="scan_hosts",required=True)
	given_args = parser.parse_args()
	scan_hosts = given_args.scan_hosts
	scheduler.enter(1, 1, detect_inactive_hosts, (scan_hosts,))
	scheduler.run()