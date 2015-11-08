#!/usr/bin/env python
import subprocess

"""
A ssh based command dispatch system

"""
machines = ["10.0.1.40",
"10.0.1.50",
"10.0.1.51",
"10.0.1.60",
"10.0.1.80"]

cmd = "python /src/fingerprint.py"
for machine in machines:
    subprocess.call("ssh root@%s %s" % (machine, cmd), shell=True)






