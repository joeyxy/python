import threading
import time
import subprocess
count = 1
class KissThread(threading.Thread):
    """Pings Hosts in a thread"""
    def ping(self):
        p = subprocess.call("ping", "ip", shell=True)
    def run(self):
        global count
        print "Thread # %s:  Pretending to do stuff" % count
        count += 1
        time.sleep(2)
        print "done with stuff"
for t in range(5):
    KissThread().start()


