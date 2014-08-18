from baseclasses import SimpleTestCase
from test import conf
from core.utils import randstr
import os, sys, shutil
from string import ascii_lowercase
sys.path.append(os.path.abspath('..'))
import modules
from tempfile import NamedTemporaryFile, mkdtemp
import modules.generate.php
import modules.generate.img
import core.backdoor
from commands import getstatusoutput
from unittest import skipIf

class Generators(SimpleTestCase):
    
    def __test_new_bd(self, relpathfrom, phpbdname, phpbd_pwd):
 
        
        self.__class__._env_cp(relpathfrom, phpbdname)

        web_base_url = '%s%s' %  (conf['env_base_web_url'], self.basedir.replace(conf['env_base_web_dir'],''))
        phpbd_url = os.path.join(web_base_url, phpbdname)
        
        call = ':shell.php "echo(1+1);"'
        command = '%s %s %s %s' % (conf['cmd'], phpbd_url, phpbd_pwd, call)
        status, output = getstatusoutput(command)
        self.assertEqual('2', output)

        self.__class__._env_rm(phpbdname)
         
    
    def test_php(self):
        
        phpbd_pwd = randstr(4)
        temp_file = NamedTemporaryFile(); temp_file.close(); 
        
        self.assertEqual(self._res(':generate.php %s %s'  % (phpbd_pwd, temp_file.name)),temp_file.name)
        self.assertEqual(self._res(':generate.php %s'  % (phpbd_pwd)),'weevely.php')
        self.assertTrue(os.path.isfile('weevely.php'))
        os.remove('weevely.php')
            
        
        self.assertRegexpMatches(self._warn(':generate.php %s /tmp/sdalkjdas/kjh'  % (phpbd_pwd)), modules.generate.php.WARN_WRITING_DATA)
        self.assertRegexpMatches(self._warn(':generate.php %s %s2'  % (phpbd_pwd[:2], temp_file.name)), core.backdoor.WARN_SHORT_PWD)
        self.assertRegexpMatches(self._warn(':generate.php @>!? %s3'  % (temp_file.name)), core.backdoor.WARN_CHARS)


        # No output expected 
        self.assertEqual(self._outp(':generate.php %s %s'  % (phpbd_pwd, temp_file.name+'2')),'')

        self.__test_new_bd(temp_file.name, '%s.php' % randstr(5), phpbd_pwd)
        
        
    @skipIf(not conf['remote_allowoverride'] or "off" in conf['remote_allowoverride'].lower(), "Skipping for missing AllowOverride")
    def test_htaccess(self):
        
        phpbd_pwd = randstr(4)
        temp_file = NamedTemporaryFile(); temp_file.close(); 
        
        self.assertEqual(self._res(':generate.htaccess %s %s'  % (phpbd_pwd, temp_file.name)),temp_file.name)
        self.assertEqual(self._res(':generate.htaccess %s'  % (phpbd_pwd)),'.htaccess')
        self.assertTrue(os.path.isfile('.htaccess'))
        os.remove('.htaccess')
        
        self.assertRegexpMatches(self._warn(':generate.htaccess %s /tmp/sdalkjdas/kjh'  % (phpbd_pwd)), modules.generate.php.WARN_WRITING_DATA)
        self.assertRegexpMatches(self._warn(':generate.htaccess %s %s2'  % (phpbd_pwd[:2], temp_file.name)), core.backdoor.WARN_SHORT_PWD)
        self.assertRegexpMatches(self._warn(':generate.htaccess @>!?!* %s3'  % (temp_file.name)), core.backdoor.WARN_CHARS)


        # No output expected 
        self.assertEqual(self._outp(':generate.htaccess %s %s'  % (phpbd_pwd, temp_file.name+'2')),'')

        self.__test_new_bd(temp_file.name, '.htaccess', phpbd_pwd)
        

    @skipIf(not conf['remote_allowoverride'] or "off" in conf['remote_allowoverride'].lower(), "Skipping for missing AllowOverride")
    def test_img(self):
        
        phpbd_pwd = randstr(4)
        temp_file = NamedTemporaryFile(); temp_file.close(); 
        temp_imgpathname = '%s.gif' % temp_file.name 
        temp_path, temp_filename = os.path.split(temp_imgpathname)
        
        temp_outputdir = mkdtemp()
        
        status, output = getstatusoutput(conf['env_create_backdoorable_img'] % temp_imgpathname)
        self.assertEqual(0, status)        
        
        self.assertEqual(self._res(':generate.img %s %s'  % (phpbd_pwd, temp_imgpathname)), [os.path.join('bd_output',temp_filename), 'bd_output/.htaccess'])
        self.assertTrue(os.path.isdir('bd_output'))
        shutil.rmtree('bd_output')
        
        self.assertRegexpMatches(self._warn(':generate.img %s /tmp/sdalkj'  % (phpbd_pwd)), modules.generate.img.WARN_IMG_NOT_FOUND)
        self.assertRegexpMatches(self._warn(':generate.img %s %s /tmp/ksdajhjksda/kjdha'  % (phpbd_pwd, temp_imgpathname)), modules.generate.img.WARN_DIR_CREAT)
        self.assertRegexpMatches(self._warn(':generate.img [@>!?] %s %s3'  % (temp_imgpathname, temp_outputdir)), core.backdoor.WARN_CHARS)

        self.assertEqual(self._res(':generate.img %s %s %s'  % (phpbd_pwd, temp_imgpathname, temp_outputdir)), [os.path.join(temp_outputdir,temp_filename), os.path.join(temp_outputdir, '.htaccess')])


        # No output expected 
        self.assertEqual(self._outp(':generate.img %s %s %s'  % (phpbd_pwd, temp_imgpathname, temp_outputdir+'2')), '')

        self.__class__._env_chmod(temp_outputdir, '0777')
        self.__class__._env_cp(os.path.join(temp_outputdir, '.htaccess'), '.htaccess')

        self.__test_new_bd( os.path.join(temp_outputdir,temp_filename), temp_filename, phpbd_pwd)
       