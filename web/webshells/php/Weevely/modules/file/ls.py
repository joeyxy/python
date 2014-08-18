from core.moduleguess import ModuleGuess
from core.moduleexception import ProbeException, ProbeSucceed, ModuleException
import time
import datetime

WARN_NO_SUCH_FILE = 'No such file or permission denied'

class Ls(ModuleGuess):
    '''List directory contents'''

    def _set_vectors(self):
        
        self.vectors.add_vector(name='ls_php', interpreter='shell.php', payloads = [ "$p=\"$rpath\"; if(@is_dir($p)) { $d=@opendir($p); $a=array(); if($d) { while(($f = @readdir($d))) { $a[]=$f; }; sort($a); print(join('\n', $a)); } } else { print($p); }" ])
        self.vectors.add_vector(name='ls', interpreter='shell.sh', payloads = [ 'ls "$rpath" $args' ])
        
        self.support_vectors.add_vector('exists_and_writ', 'shell.php',  "$f='$rpath'; if(file_exists($f) && ((is_dir($f) && is_readable($f)) || !is_dir($f))) print(1); else print(0);")

        
    def _set_args(self):
        self.argparser.add_argument('rpath', nargs='?', default='.')
        self.argparser.add_argument('args', nargs='*', help='Optional system shell \'ls\' arguments, preceeded by --')
        self.argparser.add_argument('-vector', choices = self.vectors.keys())
        
    def _prepare(self):

        if self.support_vectors.get('exists_and_writ').execute({ 'rpath' : self.args['rpath'] }) == '0':
            raise ProbeException(self.name, WARN_NO_SUCH_FILE)
    
    def _prepare_vector(self):

        self.formatted_args['rpath'] = self.args['rpath']
        if self.current_vector.name == 'ls':
            self.formatted_args['args'] = ' '.join(self.args['args']) 

    def _verify_vector_execution(self):
        if self._result:
            raise ProbeSucceed(self.name, 'List OK')
            
    def _stringify_result(self):
        if self._result:
            # Fill self._result with file list only with ls_php vector or clean ls execution
            if self.current_vector.name == 'ls_php' or (self.current_vector.name == 'ls' and not self.formatted_args['args']):
                self._result = self._result.split('\n')
                self._output = '\n'.join([ f for f in self._result if f not in ('.', '..')])
            else:
                self._output = self._result           