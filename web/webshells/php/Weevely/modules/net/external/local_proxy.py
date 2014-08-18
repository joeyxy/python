import SocketServer
import urllib
from thread import start_new_thread
from sys import argv, exit
import re

class ProxyHandler(SocketServer.StreamRequestHandler):

    def __init__(self, request, client_address, server):

        self.proxies = {}
        self.useragent = server.agent
        self.phpproxy = server.rurl

        try:
            SocketServer.StreamRequestHandler.__init__(self, request, client_address,server)
        except Exception, e:
            raise


    def handle(self):
        req, body, cl, req_len, read_len = '', 0, 0, 0, 4096
        try:
            while 1:
                if not body:
                    line = self.rfile.readline(read_len)
                    if line == '':
                        # send it anyway..
                        self.send_req(req)
                        return
                    #if line[0:17].lower() == 'proxy-connection:':
                    #    req += "Connection: close\r\n"
                    #    continue
                    req += line
                    if not cl:
                        t = re.compile('^Content-Length: (\d+)', re.I).search(line)
                        if t is not None:
                            cl = int(t.group(1))
                            continue
                    if line == "\015\012" or line == "\012":
                        if not cl:
                            self.send_req(req)
                            return
                        else:
                            body = 1
                            read_len = cl
                else:
                    buf = self.rfile.read(read_len)
                    req += buf
                    req_len += len(buf)
                    read_len = cl - req_len
                    if req_len >= cl:
                        self.send_req(req)
                        return
        except Exception, e:
            raise

    def send_req(self, req):
        #print req
        if req == '':
            return
        ua = urllib.FancyURLopener(self.proxies)
        ua.addheaders = [('User-Agent', self.useragent)]
        r = ua.open(self.phpproxy, urllib.urlencode({'req': req}))
        while 1:
            c = r.read(2048)
            if c == '': break
            self.wfile.write(c)
        self.wfile.close()
        
        
if __name__ == "__main__":
    
    if len(argv) < 5:
        print '[!] Usage: ./local_proxy.py <localhost> <localport> <rurl> <useragent>'
        exit(1)
        
    lhost = argv[1]
    lport = int(argv[2])
    rurl = argv[3]
    agent = argv[4]
    
    SocketServer.TCPServer.allow_reuse_address = True
    server = SocketServer.ThreadingTCPServer((lhost, lport), ProxyHandler)
    server.rurl = rurl
    server.agent = agent
    server.serve_forever()
