#!/usr/bin/env python
import subprocess
import ConfigParser
import time
"""
A ssh based command dispatch system

"""
start = time.time()
def readConfig(file="config.ini"):
    """Extract IP addresses and CMDS from config file and returns tuple"""
    ips = []
    cmds = []
    Config = ConfigParser.ConfigParser()
    Config.read(file)
    machines = Config.items("MACHINES")
    commands = Config.items("COMMANDS")
    for ip in machines:
        ips.append(ip[1])
    for cmd in commands:
        cmds.append(cmd[1])
    return ips, cmds

ips, cmds = readConfig()

#For every ip address, run all commands
for ip in ips:
    for cmd in cmds:
        subprocess.call("ssh root@%s %s" % (ip, cmd), shell=True)

end = time.time()
print "Dispatch Completed in %s seconds" % float(end - start)





