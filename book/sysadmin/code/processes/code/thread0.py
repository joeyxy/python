from threading import Thread
from time import sleep

class MThread(Thread):
    def run(self):
        print 'Second Thread Has Spawned'
        sleep(5)
        print 'Second Thread Done'

print "Main Program has started"
secondThread = MThread()
secondThread.start()
print 'Main program is done.'
