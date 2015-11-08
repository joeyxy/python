#!/usr/bin/env python
from subprocess import call
import sys
from threading import Thread
from Queue import Queue
import subprocess
import os


queue = Queue()
num = 9         #number of worker threads

def stream(i,q,dest = "/tmp/sync_dir_B/"):
    """Spawns stream for each file"""
    while True:
        fullpath = q.get()
        print "Running rsync on %s" % fullpath
        cmd = "rsync -av %s %s" % (fullpath, dest)
        status = call(cmd, shell=True)
        #if status != 0:
        #    print "Stream Failed"
        #    sys.exit(1)
        q.task_done()

def controller():
    #spawn N worker pool threads
    for i in range(num):
        worker = Thread(target=stream, args=(i,queue))
        worker.setDaemon(True)
        worker.start()
    #populate queue with files
    for dirpath, dirnames, filenames in os.walk("/tmp/sync_dir_A"):
        for file in filenames:
            path = os.path.join(dirpath, file)
            print path
            queue.put(path)


    print "Main Thread Waiting"
    queue.join()
    print "Done"
if __name__ == "__main__":
    import time
    start = time.time()
    controller()
    print "finished in %s" % (time.time() - start)

