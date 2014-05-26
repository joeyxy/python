#!/usr/bin/env python

from pymongo import MongoClient
import sys,re
import threading

result = []

def loop(ip):
    try:
        client = MongoClient(ip,27017,connectTimeoutMS=1000,socketTimeoutMS=1000,waitQueueTimeoutMS=1000)
        client.close()
        result.append(ip)
        #print str(ip)+"      Congratulations, NO auth needed!"
    except KeyboardInterrupt:
        print "Interrupted by user. Exiting..."
        exit()
    except:
        #print str(ip)+"      Connection Failed :<"
        pass


def doThreads(subIPs):
    threads = []
    count = len(subIPs)
    for i in xrange(count):
        ip = str(subIPs[i])
        t = threading.Thread(target=loop,args=(ip,))
        threads.append(t)

    for i in xrange(len(threads)):
        threads[i].start()

    for i in xrange(len(threads)):
        threads[i].join()


def main():
    if not len(sys.argv) == 3:
        print "Usage: %s NumberOfThreads IpListFile"%(sys.argv[0])
        exit()

    threadNum = int(sys.argv[1])

    fp = open(sys.argv[2])
    lines = fp.read()
    fp.close()

    ips = re.findall(r'[0-9]+(?:\.[0-9]+){3}',lines)
    ips = list(set(ips))
    ipCount=len(ips)

    print "%d IPs to scan. Estimated time of finish: %ds\n"%(ipCount,ipCount/threadNum+1)

    sublist = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
    for subIPs in sublist(ips,threadNum):
        doThreads(subIPs)

#    raw_input("Scan finished. Press ENTER to exit...")
    print result


if __name__ == '__main__':
    main()






