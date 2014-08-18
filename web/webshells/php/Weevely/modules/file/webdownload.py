
from core.moduleguess import ModuleGuess
from core.moduleexception import ProbeException, ProbeSucceed

WARN_DOWNLOAD_OK = 'Downloaded succeed'

class Webdownload(ModuleGuess):
    '''Download web URL to remote filesystem'''

    def _set_vectors(self):
        
        self.vectors.add_vector(name='putcontent', interpreter='shell.php', payloads = [ 'file_put_contents("$rpath", file_get_contents("$url"));' ])
        self.vectors.add_vector(name='wget', interpreter='shell.sh', payloads = [ 'wget $url -O $rpath' ])
        self.vectors.add_vector(name='curl', interpreter='shell.sh', payloads = [ 'curl -o $rpath $url' ])
        
        self.support_vectors.add_vector(name='check_download', interpreter='file.check', payloads = [ '$rpath', 'exists' ])
                
    def _set_args(self):
        self.argparser.add_argument('url')
        self.argparser.add_argument('rpath')
        self.argparser.add_argument('-vector', choices = self.vectors.keys())
        
    
    def  _verify_vector_execution(self):
   
       # Verify downloaded file. Save vector return value in self._result and eventually raise 
       # ProbeException to stop module execution and print error message.

       self._result = self.support_vectors.get('check_download').execute({ 'rpath' : self.args['rpath'] })
       
       if self._result == True:
           raise ProbeSucceed(self.name, WARN_DOWNLOAD_OK)
       