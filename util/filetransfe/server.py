#!/usr/bin/env python
import SocketServer, time 
import os
import yaml
class MyServer(SocketServer.BaseRequestHandler):  
   ##what the reason that the func of init did not work
    #def __init__(self):
        #try:
            #config = yaml.load(file('config.yaml',"r"))
        #except yaml.YAMLError:
            #print "error in configuration file"
        #self.user = config['userinfo']['username']
        #self.pwd = config['userinfo']['password']
        #self.root_path = config['root']   
        #print ">>>**the process of reading config has done**"
        #print self.user
        #print self.pwd
        #print self.root_path
       
    def init_config(self):
        try:
            config = yaml.load(file('config.yaml',"r"))
        except yaml.YAMLError:
            print "error in configuration file"
        self.user = config['userinfo']['username']
        self.pwd = config['userinfo']['password']
        self.root_path = config['root']   
        print ">>>**the process of reading config has done**"
        print self.user
        print self.pwd
        print self.root_path
       
    def handle(self):  
        print '>>>Connected from', self.client_address           
        self.init_config()        
        while True:  
            receivedData = self.request.recv(8192)  
            if not receivedData:  
                continue 
            #build a connection
            elif receivedData == 'Hi, server':  
                self.request.sendall('hi, client')                      
            elif receivedData.startswith('name'):  
                #the last element of list is the name
                self.clientName = receivedData.split(':')[-1]   
                if self.user==self.clientName:  
                    self.request.sendall('valid')  
                else:  
                    self.request.sendall('invalid')                          
            elif receivedData.startswith('pwd'):  
                self.clientPwd = receivedData.split(':')[-1]
                if self.pwd==self.clientPwd:
                    self.request.sendall('valid')  
                    time.sleep(5)  
                    #***************************************
                    #when the authentication has done,then send the dir
                    #the client choose one and the server reply it
                    #D:\act\python_project\act_a_d\server
                    dirfiles=os.listdir(self.root_path)
                    filedata=""
                    print ">>>**the dir has following files**"
                    for item in dirfiles:
                        print item
                        filedata+=item
                    self.request.sendall(str(dirfiles))                  
                    filename = self.request.recv(8192) 
                    print "receive the user's choose:"+filename
                    sfile = open(filename,'rb')
                    #***************************************                        
                    while True:  
                        data = sfile.read(1024)  
                        if not data:  
                            break 
                        #divide the file into segments and send respectively.
                        while len(data) > 0:  
                            intSent = self.request.send(data)  
                            data = data[intSent:]     
                    time.sleep(3)  
                    #destroy the connect
                    self.request.sendall('EOF')  
                else:  
                    self.request.sendall('invalid')                          
            elif receivedData == 'bye':  
                break    
        self.request.close()              
        print 'Disconnected from', self.client_address  
        print 
 
if __name__ == '__main__':  
    print 'Server is started\nwaiting for connection...\n'  
    srv = SocketServer.ThreadingTCPServer(('127.0.0.1', 5000), MyServer)  
    srv.serve_forever()  
