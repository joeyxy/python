#!/usr/bin/env python
#KISS threads example
import thread
import time

def print_delay(delay):
    while True:
        time.sleep(delay)
        print time.ctime(time.time())

#Start a new thread
thread.start_new_thread(print_delay, (5,))
while True:
    pass

