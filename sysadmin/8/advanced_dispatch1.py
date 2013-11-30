#!/usr/bin/env python
import subprocess
import ConfigParser


def readConfig(file="config.ini"):
	ips = []
	cmds = []
	config = ConfigParser.ConfigParser()
	config.read(file)
	machines = config.items("machines")
	commands = config.items("commands")
	for ip in machines:
		ips.append(ip[1])
	for cmd in commands:
		cmds.append(cmd[1])
	return ips,cmds


ips,cmds = readConfig()

for ip in ips:
	for cmd in cmds:
		print "cmd %s execute on:%s" % (cmd,ip)
		subprocess.call("%s %s" % (cmd,ip),shell=True)
