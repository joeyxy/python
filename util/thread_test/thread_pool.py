#!/usr/bin/env python
# -*- coding:utf-8 -*-

import Queue
import threading
import time

class WorkManager(object):
    def __init__(self, work_num=1000,thread_num=2):
        self.work_queue = Queue.Queue()
        self.threads = []
        self.__init_work_queue(work_num)
        self.__init_thread_pool(thread_num)

    def __init_thread_pool(self,thread_num):
        for i in range(thread_num):
            self.threads.append(Work(self.work_queue))


    def __init_work_queue(self, jobs_num):
        for i in range(jobs_num):
            self.add_job(do_job, i)


    def add_job(self, func, *args):
        self.work_queue.put((func, list(args)))

 
    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive():item.join()

class Work(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()

    def run(self):
        while True:
            try:
                do, args = self.work_queue.get(block=False)
                do(args)
                self.work_queue.task_done()
            except:
                break


def do_job(args):
    time.sleep(0.1)
    print threading.current_thread(), list(args)

if __name__ == '__main__':
    start = time.time()
    work_manager =  WorkManager(5000, 10)
    work_manager.wait_allcomplete()
    end = time.time()
    print "cost all time: %s" % (end-start)
