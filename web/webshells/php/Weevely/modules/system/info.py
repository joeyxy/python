'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module
from core.moduleexception import ModuleException
from core.argparse import ArgumentParser
from core.vector import VectorsDict
import urllib2

from re import compile

re_lsb_release = compile('Description:[ \t]+(.+)')
re_etc_lsb_release = compile('(?:DISTRIB_DESCRIPTION|PRETTY_NAME)="(.+)"')
re_exitaddress = compile('\nExitAddress[\s]+([^\s]+)')


WARN_NO_EXITLIST = 'Error downloading TOR exit list'

class Info(Module):
    """Collect system information"""

    def _set_vectors(self):
            self.support_vectors.add_vector('document_root', 'shell.php', "@print($_SERVER['DOCUMENT_ROOT']);"),
            self.support_vectors.add_vector('whoami', 'shell.php', "$u=@posix_getpwuid(posix_geteuid()); if($u) { $u = $u['name']; } else { $u=getenv('username'); } print($u);"),
            self.support_vectors.add_vector('hostname', 'shell.php', "@print(gethostname());"),
            self.support_vectors.add_vector('cwd', 'shell.php', "@print(getcwd());"),
            self.support_vectors.add_vector('open_basedir', 'shell.php', "$v=@ini_get('open_basedir'); if($v) print($v);"),
            self.support_vectors.add_vector('safe_mode', 'shell.php', "(ini_get('safe_mode') && print(1)) || print(0);"),
            self.support_vectors.add_vector('script', 'shell.php', "@print($_SERVER['SCRIPT_NAME']);"),
            self.support_vectors.add_vector('uname', 'shell.php', "@print(php_uname());"),
            self.support_vectors.add_vector('os', 'shell.php', "@print(PHP_OS);"),
            self.support_vectors.add_vector('client_ip', 'shell.php', "@print($_SERVER['REMOTE_ADDR']);"),
            self.support_vectors.add_vector('max_execution_time', 'shell.php', '@print(ini_get("max_execution_time"));'),
            self.support_vectors.add_vector('php_self', 'shell.php', '@print($_SERVER["PHP_SELF"]);')
            self.support_vectors.add_vector('dir_sep' , 'shell.php',  '@print(DIRECTORY_SEPARATOR);')
            self.support_vectors.add_vector('php_version' , 'shell.php',  "$v=''; if(function_exists( 'phpversion' )) { $v=phpversion(); } elseif(defined('PHP_VERSION')) { $v=PHP_VERSION; } elseif(defined('PHP_VERSION_ID')) { $v=PHP_VERSION_ID; } print($v);")
    
            self.release_support_vectors = VectorsDict(self.modhandler)
            self.release_support_vectors.add_vector('lsb_release' , 'shell.sh',  'lsb_release -d')
            self.release_support_vectors.add_vector('read' , 'file.read',  '$rpath')
    
    def _set_args(self):
        additional_args = ['all', 'release', 'check_tor']
        self.argparser.add_argument('info', help='Information',  choices = self.support_vectors.keys() + additional_args, default='all', nargs='?')

    def __check_tor(self):
        
        exitlist_urls = ('http://exitlist.torproject.org/exit-addresses', 'http://exitlist.torproject.org/exit-addresses.new')
        
        exitlist_content = ''
        for url in exitlist_urls:
            try:
                exitlist_content += urllib2.urlopen(url, timeout=1).read() + '\n'
            except Exception, e:
                self.mprint('%s: \'%s\'' % ( WARN_NO_EXITLIST, url))
            
        addresses = re_exitaddress.findall(exitlist_content)
        client_ip = self.support_vectors.get('client_ip').execute()
        
        return client_ip in addresses
            


    def __guess_release(self):
        
        lsb_release_output = self.release_support_vectors.get('lsb_release').execute()
        if lsb_release_output: 
            rel = re_lsb_release.findall(lsb_release_output)
            if rel: return rel[0]
            
        for rpath in ('/etc/lsb-release', '/etc/os-release',):
            etc_lsb_release_content =  self.release_support_vectors.get('read').execute({'rpath' : rpath})
            if etc_lsb_release_content:
                rel = re_etc_lsb_release.findall(etc_lsb_release_content)
                if rel: return rel[0]

        for rpath in ('/etc/issue.net', '/etc/issue',):
            etc_issue_content =  self.release_support_vectors.get('read').execute({'rpath' : rpath}).strip()
            if etc_issue_content:
                return etc_issue_content

        return ''

    def _probe(self):
        
        if self.args['info'] == 'check_tor':
            self._result = self.__check_tor()
        elif self.args['info'] == 'release':
            self._result = self.__guess_release().strip()
        elif self.args['info'] != 'all':
            self._result = self.support_vectors.get(self.args['info']).execute()
        else:
            
            self._result = {}

            for vect in self.support_vectors.values():
                self._result[vect.name] = vect.execute()
                
            self._result['release'] = self.__guess_release()
            self._result['check_tor'] = self.__check_tor()
                
                    
        
