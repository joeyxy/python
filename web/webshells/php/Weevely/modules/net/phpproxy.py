from modules.file.upload2web import Upload2web
from modules.file.upload import WARN_NO_SUCH_FILE
from core.moduleexception import ModuleException, ProbeException
from core.argparse import ArgumentParser
from core.argparse import SUPPRESS
import re, os
from core.utils import randstr

class Phpproxy(Upload2web):
    '''Install remote PHP proxy'''

    def _set_args(self):
        self.argparser.add_argument('rpath', help='Optional, upload as rpath', nargs='?')
        
        self.argparser.add_argument('-startpath', help='Upload in first writable subdirectory', metavar='STARTPATH', default='.')
        self.argparser.add_argument('-chunksize', type=int, default=1024, help=SUPPRESS)
        self.argparser.add_argument('-vector', choices = self.vectors.keys(), help=SUPPRESS)
        self.argparser.add_argument('-force', action='store_true')


    def _get_proxy_path(self):
        return os.path.join(self.modhandler.modules_path, 'net', 'external', 'phpproxy.php')
    
    def _prepare(self):

        proxy_path = self._get_proxy_path()

        if not self.args['rpath']:
            
            # If no rpath, set content and remote final filename as random
            try:
                content = open(proxy_path, 'r').read()
            except Exception, e:
                raise ProbeException(self.name,  '\'%s\' %s' % (self.args['lpath'], WARN_NO_SUCH_FILE))

            self.args['lpath'] = randstr(4) + '.php'
            self.args['content'] = content
            
        else:
            
            # Else, set lpath as proxy filename
            
            self.args['lpath'] = proxy_path
            self.args['content'] = None
    
    
        Upload2web._prepare(self)
    
    
    def _stringify_result(self):

        Upload2web._stringify_result(self)

        sess_filename = os.path.join(*(self.args['rpath'].split('/')[:-1] + [ 'sess_*']))
        
        self._output = """Php proxy installed, point your browser to %s?u=http://www.google.com .
Delete '%s' and '%s' at session end.""" % ( self.args['url'], self.args['rpath'], sess_filename )

        
        
            
        