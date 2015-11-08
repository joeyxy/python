#!/usr/bin/env python
import os, sys

def counter(count):
    for i in range(count): print '[%s] => %s' % (os.getpid(), i)

    for i in range(10):
        pid = os.fork()
        if pid !=0:
            print 'Process %d spawned' % pid
        else:
            counter(100)
            sys.exit()
counter(2)
print "Main process exiting."

