from core.module import Module
from core.moduleexception import ProbeException
from core.argparse import ArgumentParser
from ast import literal_eval
from core.utils import chunks
from re import findall
from types import ListType
from core.prettytable import PrettyTable, ALL
import os

MSG_BASEDIR='Your base directory is presently set to $$BASEDIR$$ - PHP scripts will not be able to access the file system outside of this directory.'

ERR_CONFIG_BASEDIR='Enabled base_dir conf '
ERR_CONFIG_BASEDIR_NOT_SET='not restricted '
ERR_CONFIG_BASEDIR_CHDIR='\nchangeable because of \'.\' '
ERR_CONFIG_BASEDIR_SLASH='\nwithout trailing "/" '

ERR_CONFIG_PHPUSER='Root account could be abuse'
WARN_CONFIG_PHPUSER_WIN='Ensure that this user is not an administrator'

ERR_FUNCTION_PROFILE='Enabled functs to gather\nPHP configuration'
WARN_FUNCTION_FILES='Enabled functs to access\nto the filesystem'
ERR_FUNCTION_EXECUTE='Enabled functs to execute\ncommands'
ERR_FUNCTION_LOGGING='Enabled functs to tamper\nlog files'
ERR_FUNCTION_DISRUPT='Enabled functs to disrupt\nother process'

ERR_CONFIG_EXECUTE='Enabled confs that allow\ncommand executions'
ERR_CONFIG_ERRORS='Enble confs that displays\ninformation on errors'

WARN_CONFIG_SAFEMODE='Enabled confs that restrict\nfilesystem access and\nsystem command execution'
WARN_SESS_PATH = 'Disabled conf to move sessions\nfiles in a protected folder'

WARN_CONFIG_UPLOAD='Enabled confs to\nupload files'
ERR_CONFIG_INCLUDES='Enabled confs to allow\nremote files opening'
ERR_CONFIG_PROFILE='Enabled confs to gather\nPHP configuration infos'
ERR_CONFIG_GLOBALS='Enabled conf register_globals\nallows malicious variable manipulation'
WARN_MAGIC_QUOTES='Enabled confs that provide\nineffective SQLi protection'
ERR_SESS_TRANS='Enabled conf to pass\nsession ID via the URL'

insecure_features = """
$insecure_features = array();

$insecure_features['expose_php'] = 'ERR_CONFIG_PROFILE';
$insecure_features['file_uploads'] = 'WARN_CONFIG_UPLOAD';
$insecure_features['register_globals'] = 'ERR_CONFIG_GLOBALS';
$insecure_features['allow_url_fopen'] = 'ERR_CONFIG_INCLUDES';
$insecure_features['display_errors'] = 'ERR_CONFIG_ERRORS';
$insecure_features['enable_dl'] = 'ERR_CONFIG_EXECUTE';
$insecure_features['safe_mode'] = 'WARN_CONFIG_SAFEMODE';
$insecure_features['magic_quotes_gpc'] = 'WARN_MAGIC_QUOTES';
$insecure_features['allow_url_include'] = 'ERR_CONFIG_INCLUDES';
$insecure_features['session.use_trans_sid'] = 'ERR_SESS_TRANS';

foreach ( $insecure_features as $feature_key => $feature_message )
    if ((bool)ini_get($feature_key) ) print($feature_key . " " . $feature_message. "|");"""

insecure_classes = """
$insecure_classes = array();
$insecure_classes['splFileObject'] = 'ERR_CONFIG_EXECUTE';
foreach ( $insecure_classes as $class_key => $class_message )
{
    if ( class_exists($class_key) ) print($class_key . "() " . $class_message . "|");
}"""

insecure_functions = """
$insecure_functions = array();
$insecure_functions['apache_child_terminate'] = 'ERR_FUNCTION_PROFILE';
$insecure_functions['apache_get_modules'] = 'ERR_FUNCTION_PROFILE';
$insecure_functions['apache_get_version'] = 'ERR_FUNCTION_PROFILE';
$insecure_functions['apache_getenv'] = 'ERR_FUNCTION_PROFILE';
$insecure_functions['get_loaded_extensions'] = 'ERR_FUNCTION_PROFILE';
$insecure_functions['phpinfo'] = 'ERR_FUNCTION_PROFILE';
$insecure_functions['phpversion'] = 'ERR_FUNCTION_PROFILE';
$insecure_functions['chgrp'] = 'WARN_FUNCTION_FILES';
$insecure_functions['chmod'] = 'WARN_FUNCTION_FILES';
$insecure_functions['chown'] = 'WARN_FUNCTION_FILES';
$insecure_functions['copy'] = 'WARN_FUNCTION_FILES';
$insecure_functions['link'] = 'WARN_FUNCTION_FILES';
$insecure_functions['mkdir'] = 'WARN_FUNCTION_FILES';
$insecure_functions['rename'] = 'WARN_FUNCTION_FILES';
$insecure_functions['rmdir'] = 'WARN_FUNCTION_FILES';
$insecure_functions['symlink'] = 'WARN_FUNCTION_FILES';
$insecure_functions['touch'] = 'WARN_FUNCTION_FILES';
$insecure_functions['unlink'] = 'WARN_FUNCTION_FILES';
$insecure_functions['openlog'] = 'ERR_FUNCTION_LOGGING';
$insecure_functions['proc_nice'] = 'ERR_FUNCTION_DISRUPT';
$insecure_functions['syslog'] = 'ERR_FUNCTION_LOGGING';
$insecure_functions['apache_note'] = 'ERR_FUNCTION_EXECUTE';
$insecure_functions['apache_setenv'] = 'ERR_FUNCTION_EXECUTE';
$insecure_functions['dl'] = 'ERR_FUNCTION_EXECUTE';
$insecure_functions['exec'] = 'ERR_FUNCTION_EXECUTE';
$insecure_functions['passthru'] = 'ERR_FUNCTION_EXECUTE';
$insecure_functions['pcntl_exec'] = 'ERR_FUNCTION_EXECUTE';
$insecure_functions['popen'] = 'ERR_FUNCTION_EXECUTE';
$insecure_functions['proc_close'] = 'ERR_FUNCTION_EXECUTE';
$insecure_functions['proc_open'] = 'ERR_FUNCTION_EXECUTE';
$insecure_functions['proc_get_status'] = 'ERR_FUNCTION_EXECUTE';
$insecure_functions['proc_terminate'] = 'ERR_FUNCTION_EXECUTE';
$insecure_functions['putenv'] = 'ERR_FUNCTION_EXECUTE';
$insecure_functions['shell_exec'] = 'ERR_FUNCTION_EXECUTE';
$insecure_functions['system'] = 'ERR_FUNCTION_EXECUTE';
$insecure_functions['virtual'] = 'ERR_FUNCTION_EXECUTE';

foreach ( $insecure_functions as $function_key => $function_message )
{
    if ( function_exists($function_key) )
        print($function_key . "() " . $function_message. "|");
}"""



class Phpconf(Module):
    '''Check php security configurations'''

    def _set_vectors(self):
                
        self.support_vectors.add_vector('os', 'system.info', ["os"])
        self.support_vectors.add_vector('whoami', 'system.info', ["whoami"])
        self.support_vectors.add_vector('php_version', 'system.info', ['php_version'])
        self.support_vectors.add_vector('open_basedir', 'system.info', ['open_basedir'])
        self.support_vectors.add_vector('check_functions', 'shell.php', [ insecure_functions ])
        self.support_vectors.add_vector('check_classes', 'shell.php', [ insecure_classes ])
        self.support_vectors.add_vector('check_features', 'shell.php', [ insecure_features ])
    
    def __check_os(self):

        os = self.support_vectors.get('os').execute()
        if 'win' in os.lower():
            os = 'win'
        else:
            os = 'Linux'
            
        self._result['os'] = [ os ]
    
    def __check_version(self):
        
        self._result['PHP version'] = [  self.support_vectors.get('php_version').execute() ]
    
    def __check_username(self):
        
        username = [ self.support_vectors.get('whoami').execute() ]
        
        if self._result['os'] == 'win':
            self._result['username\n(%s)' % WARN_CONFIG_PHPUSER_WIN] = username
        elif  username == 'root':
            self._result['username\n(%s)' %  ERR_CONFIG_PHPUSER] = username
        else:
            self._result['username'] = username

    def __check_openbasedir(self):
        basedir_str = self.support_vectors.get('open_basedir').execute()
        
        err_msg = ERR_CONFIG_BASEDIR
        

        if not basedir_str:
            err_msg += ERR_CONFIG_BASEDIR_NOT_SET
            self._result_insecurities[err_msg] = [ ]
        else:
            
            if self._result['os'] == 'win':
                dirs = basedir_str.split(';')
            else:
                dirs = basedir_str.split(':') 
                 
            if '.' in dirs: 
                err_msg += ERR_CONFIG_BASEDIR_CHDIR
                
            trailing_slash = True
            for d in dirs:
                if self._result['os'] == 'win' and not d.endswith('\\') or self._result['os'] == 'Linux' and  not d.endswith('/'):
                    trailing_slash = False
            
            if not trailing_slash:
                err_msg += ERR_CONFIG_BASEDIR_SLASH 
            
            self._result_insecurities[err_msg] = dirs
            
                        
                
                
    def __check_insecurities(self):
        
        functions_str = self.support_vectors.get('check_functions').execute() + self.support_vectors.get('check_classes').execute() + self.support_vectors.get('check_features').execute()
        if functions_str:
            functions = findall('([\S]+) ([^|]+)\|',functions_str)
            for funct, err in functions:
                if err in globals():
                    error_msg = globals()[err]
                    if error_msg not in self._result_insecurities:
                        self._result_insecurities[error_msg] = []
                        
                    self._result_insecurities[error_msg].append(funct)

    def _prepare(self):
        self._result = {}
        self._result_insecurities = {}
    
    def _probe(self):

        self.__check_os()
        self.__check_version()
        self.__check_username()
        self.__check_openbasedir()
        self.__check_insecurities()

            
    def _stringify_result(self):
        
        Module._stringify_result(self)

        table_insecurities = PrettyTable(['']*(2))
        table_insecurities.align = 'l'
        table_insecurities.header = False
        table_insecurities.hrules = ALL
        
        for res in self._result_insecurities:
            if isinstance(self._result_insecurities[res], ListType):
                field_str = ''

                for chunk in list(chunks(self._result_insecurities[res],3)):
                    field_str += ', '.join(chunk) + '\n'
                    
                table_insecurities.add_row([res, field_str.rstrip() ])


        self._output += '\n%s' % ( table_insecurities.get_string())
        
                        