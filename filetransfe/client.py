#!/usr/bin/env python
import socket, time  
class MyClient:     
    def __init__(self):  
        print 'Prepare for connecting...'     
    def connect(self):  
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        sock.connect(('127.0.0.1', 5000))  
        #connect to the server
        sock.sendall('Hi, server')  
        self.response = sock.recv(8192)  
        print 'Server:', self.response     
        #instance's attribute
        self.s = raw_input("Connect to the server?(y/n):")  
        if self.s == 'y':  
            while True:  
                self.name = raw_input('Server: input our name:')  
                sock.sendall('name:' + self.name.strip())  
                self.response = sock.recv(8192)  
                if self.response == 'valid':  
                    break 
                else:  
                    print 'Server: Invalid username'    
            while True:  
                self.pwd = raw_input('Server: input our password:')  
                sock.sendall('pwd:' + self.pwd.strip())  
                self.response = sock.recv(8192)                 
                if self.response == 'valid':  
                    print 'Welcome'+self.name+'\n'+'please wait...'
                    #******************************
                    #we need to change and get the list_dir which is contained by
                    #a list sent by the server.
                    #get the "self.response" and print the content.
                    #input the file wanted and open it below.
                    #*****************************************
                    self.response = sock.recv(8192)
                    print "**FILE LIST**"
                    file_string = self.response
                    file_list=file_string[1:-1]
                    self.count=1
                    for item in file_string[1:-1].split(','):
                        print "[%d]:" %self.count,
                        print item.strip()[1:-1]
                        self.count+=1
                   
                    print "please choose a file to download..."                   
                    while True:
                        self.file_to_down = raw_input('you choose:')
                        sock.sendall(self.file_to_down.strip())
                        break                     
                    f = open(self.file_to_down, 'wb')  
                    while True:  
                        data = sock.recv(1024)  
                        if data == 'EOF':  
                            break 
                        f.write(data)                              
                    f.flush()  
                    f.close()     
                    print 'download finished'  
                    break 
                else:  
                    print 'Server: Invalid password'  
                  
 
        sock.sendall('bye')  
        sock.close()  
        print 'Disconnected'  
 
if __name__ == '__main__':  
    client = MyClient()  
    client.connect() 
