#!/usr/bin/env python
import subprocess
import time

class Pipes(object):
    """simplifies piping and automating the subprocess module"""

    def __init__(self, *args):
        self.args = list(args)

    def call(self):
        for cmd in self.args:
            p = subprocess.call(cmd,
                            shell=True)

    def chain(self):
        if len(self.args) > 1:
            input = self.args.pop(0)
            ip = subprocess.Popen(input,
                                shell=True,
                                stdout = subprocess.PIPE) 
            clist = list(ip.stdout)
            for cmd in self.args:
                #inpipe = clist.pop(0)
                op = subprocess.Popen(cmd,
                                    shell=True,
                                    stdin=clist.pop(0),
                                    stdout=subprocess.PIPE)
                clist.append(op.stdout)
                print op.stdout.read()     

