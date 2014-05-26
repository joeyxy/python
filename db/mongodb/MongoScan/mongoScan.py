#!/usr/bin/env python

from pymongo import MongoClient
import sys,re

if not len(sys.argv) == 3:
    print "Usage: %s ipListFile outPutFile"%(sys.argv[0])
    exit()
inFile = sys.argv[1]
outFile = sys.argv[2]

fp = open(inFile)
lines = fp.read()
ips = re.findall(r'[0-9]+(?:\.[0-9]+){3}',lines)
ips = set(ips)
fp.close()

ip_count = len(ips)
print "%d IP to scan..."%(ip_count)

i = 0
count = 0

for ip in ips:
    i = i + 1
    sys.stdout.write('\r')
    sys.stdout.write("Scanning %d of %d"%(i,ip_count))
    sys.stdout.flush()

    try:
        client = MongoClient(ip,27017,connectTimeoutMS=1000,socketTimeoutMS=1000,waitQueueTimeoutMS=1000)
        #print str(ip)+"      Congratulations, NO auth needed!"


        fo = open(outFile,'a')
        fo.write(str(ip)+'\n')
        fo.close()

        client.close()

        count = count + 1
    except KeyboardInterrupt:
        print "Interrupted by user. Exiting..."
        exit()

    except Exception,e:
        #print e
        #print str(ip)+"      Connection Failed :<"
        pass

raw_input("\n\nScan FINISHED and "+str(count)+" connectable IP are recorded in 'iplist.out'. \nPress ENTER to exit...")


