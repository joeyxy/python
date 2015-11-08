#!/usr/bin/env python

from threading import Thread
from time import sleep
import atexit
from datetime import datetime

class SpawnThread(Thread):
    """Runs threads"""
    count = 0
    def run(self):
        SpawnThread.count += 1
        threadnum = SpawnThread.count
        print "Thread %s begins at %s" % (threadnum, datetime.now())
        sleep(5)
        print "Thread %s is done at %s" % (threadnum, datetime.now())

def cleanup():
    print "All Threads are finished"

if __name__ == "__main__":
    try:
        for i in range(5):
            secondThread = SpawnThread()
            secondThread.start()
    finally:
        atexit.register(cleanup)


