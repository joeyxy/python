#!/usr/bin/python
#http://rtoodtoo.net/2012/12/20/port-scanner-in-python/
import socket,sys

try:
  sys.argv[3]
except:
  print "Usage: port_scanner.py [hostname|IP] [port_start] [port_end]"
  sys.exit()

host = sys.argv[1]
start_port = int(sys.argv[2])
end_port = int(sys.argv[3])

#CREATE SOCKET
try:
  s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except socket.error,err_msg:
  print 'Socket creation failed. Error code: '+ str(err_msg[0]) + ' Error mesage: ' + err_msg[1]
  sys.exit()

#RESOLVE HOSTNAME
try:
  remote_ip = socket.gethostbyname(host)

except socket.error,error_msg:
  print 'ERROR:'
  print error_msg
  sys.exit()

#ITERATE PORT RANGE
end_port+=1
for port in range(start_port,end_port):
  try:
    s.connect((remote_ip,port))
    print 'port ' + str(port) + ' open'

    s.close()
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  except socket.error:
    pass
