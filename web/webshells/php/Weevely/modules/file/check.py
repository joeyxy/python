from core.module import Module
from core.moduleexception import ProbeException
from core.argparse import ArgumentParser
import datetime

WARN_INVALID_VALUE = 'Invalid returned value'

class Check(Module):
    '''Check remote files type, md5 and permission'''


    def _set_vectors(self):

        self.support_vectors.add_vector('exists', 'shell.php',  "$f='$rpath'; if(file_exists($f) || is_readable($f) || is_writable($f) || is_file($f) || is_dir($f)) print(1); else print(0);")
        self.support_vectors.add_vector("md5" ,'shell.php', "print(md5_file('$rpath'));")
        self.support_vectors.add_vector("read", 'shell.php',  "(is_readable('$rpath') && print(1)) || print(0);")
        self.support_vectors.add_vector("write", 'shell.php', "(is_writable('$rpath') && print(1))|| print(0);")
        self.support_vectors.add_vector("exec", 'shell.php', "(is_executable('$rpath') && print(1)) || print(0);")
        self.support_vectors.add_vector("isfile", 'shell.php', "(is_file('$rpath') && print(1)) || print(0);")
        self.support_vectors.add_vector("size", 'shell.php', "print(filesize('$rpath'));")
        self.support_vectors.add_vector("time_epoch", 'shell.php', "print(filemtime('$rpath'));")
        self.support_vectors.add_vector("time", 'shell.php', "print(filemtime('$rpath'));")
    
    
    def _set_args(self):
        self.argparser.add_argument('rpath', help='Remote path')
        self.argparser.add_argument('attr', help='Attribute to check',  choices = self.support_vectors.keys())

    def _probe(self):
        
        value = self.support_vectors.get(self.args['attr']).execute(self.args)
        
        if self.args['attr'] == 'md5' and value:
            self._result = value
        elif self.args['attr'] in ('size', 'time_epoch', 'time'):
            try:
                self._result = int(value)
            except ValueError, e:
                raise ProbeException(self.name, "%s: '%s'" % (WARN_INVALID_VALUE, value))
            
            if self.args['attr'] == 'time':
                self._result = datetime.datetime.fromtimestamp(self._result).strftime('%Y-%m-%d %H:%M:%S')
            
        elif value == '1':
            self._result = True
        elif value == '0':
            self._result = False
        else:
             raise ProbeException(self.name, "%s: '%s'" % (WARN_INVALID_VALUE, value))
            