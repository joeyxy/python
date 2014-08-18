#!/usr/bin/env python
import sys, os, socket, unittest, shlex, random, atexit
sys.path.append(os.path.abspath('..'))
import core.terminal
from core.modulehandler import ModHandler
from core.sessions import cfgfilepath
from ConfigParser import ConfigParser
from string import ascii_lowercase, Template
from tempfile import NamedTemporaryFile
from PythonProxy import start_server, start_dummy_tcp_server  
from thread import start_new_thread    
from shutil import move, rmtree
from time import sleep
from test import conf
from core.utils import randstr
from commands import getstatusoutput


class SimpleTestCase(unittest.TestCase):
    
    @classmethod  
    def setUpClass(cls):  
        
        cls.term = core.terminal.Terminal (ModHandler(conf['url'], conf['pwd']))
        cls._setenv()        

    @classmethod  
    def tearDownClass(cls):  
        cls._rm_sess()
        cls._unsetenv()

    @classmethod 
    def _rm_sess(cls):
        
        atexit._exithandlers[:] = []
          
        if not cfgfilepath.startswith('/') and os.path.exists(cfgfilepath):
            rmtree(cfgfilepath)
        
    @classmethod  
    def _setenv(cls):  
        cls.basedir = os.path.join(conf['env_base_writable_web_dir'], randstr(4))
        cls._env_mkdir(cls.basedir)
        
    @classmethod     
    def _unsetenv(cls):  
        cls._env_rm()        

    @classmethod
    def _run_test(cls, command):
        if not conf['showtest']:
            stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')  
        else:
            print command
            
        cls.term.run_cmd_line(shlex.split(command))
        
        if not conf['showtest']: 
            sys.stdout = stdout
        

    def _outp(self, command):
        self.__class__._run_test(command)
        return self.term._last_output
 
    def _warn(self, command):
        self.__class__._run_test(command)
        return self.term.modhandler._last_warns

    def _res(self, command):
        self.__class__._run_test(command)
        return self.term._last_result

    @classmethod  
    def _run_cmd(cls, cmd, weevely = True):
        if weevely:
            command = '%s %s %s %s' % (conf['cmd'], conf['url'], conf['pwd'], cmd)
        else:
            command = cmd
            
        status, output = getstatusoutput(command)
        
        if conf['showcmd']:
            print '\n%s> %s' % (command, output)
         
    @classmethod  
    def _env_mkdir(cls, relpath):
        abspath = os.path.join(cls.basedir, relpath)
        cmd = Template(conf['env_mkdir_command']).safe_substitute(path=abspath)
        cls._run_cmd(cmd)
        
    @classmethod  
    def _env_newfile(cls, relpath, content = '1'):
    
        file = NamedTemporaryFile()
        file.close()
        frompath = file.name
        
        f = open(frompath, 'w')
        f.write(content)
        f.close()
        
        abspath = os.path.join(cls.basedir, relpath)
        cmd = Template(conf['env_cp_command']).safe_substitute(frompath=frompath, topath=abspath)
        cls._run_cmd(cmd)


    @classmethod  
    def _env_chmod(cls, relpath, mode='0744'):
        
        
        
        abspath = os.path.join(cls.basedir, relpath)
        
        cmd = Template(conf['env_chmod_command']).safe_substitute(path=abspath, mode=mode)

        cls._run_cmd(cmd)

    @classmethod  
    def _env_rm(cls, relpath = ''):
        abspath = os.path.join(cls.basedir, relpath)
        
        # Restore modes
        cls._env_chmod(cls.basedir)
        
        if cls.basedir.count('/') < 3:
            print 'Please check %s, not removing' % cls.basedir
            return
        
        cmd = Template(conf['env_rm_command']).safe_substitute(path=abspath)

        cls._run_cmd(cmd)


    @classmethod  
    def _env_cp(cls, absfrompath, reltopath):
        
        abstopath = os.path.join(cls.basedir, reltopath)
        cmd = Template(conf['env_cp_command']).safe_substitute(frompath=absfrompath, topath=abstopath)
            
        cls._run_cmd(cmd)


class FolderFSTestCase(SimpleTestCase):

    @classmethod
    def _setenv(cls):
        
        SimpleTestCase._setenv.im_func(cls)
        
        cls.dirs =  []
        newdirs = ['w1', 'w2', 'w3', 'w4']
        
        for i in range(1,len(newdirs)+1):
            folder = os.path.join(*newdirs[:i])
            cls._env_mkdir(os.path.join(folder))
            cls.dirs.append(folder)
        
        

    @classmethod
    def _unsetenv(cls):
        SimpleTestCase._unsetenv.im_func(cls)


    def _path(self, command):
        self.__class__._run_test(command)
        return self.term.modhandler.load('shell.php').stored_args_namespace['path']


class FolderFileFSTestCase(FolderFSTestCase):
    
    @classmethod
    def _setenv(cls):    
        FolderFSTestCase._setenv.im_func(cls)
        
        cls.filenames = []
        i=1
        for dir in cls.dirs:
            filename = os.path.join(dir, 'file-%d.txt' % i )
            cls._env_newfile(filename)
            cls.filenames.append(filename)
            i+=1

        # Restore modes
        cls._env_chmod(cls.basedir, recursive=True)

    @classmethod  
    def _env_chmod(cls, relpath, mode='0744', recursive = False):
        
        
        if recursive:
            items = sorted(cls.filenames + cls.dirs)
        else:
            items = [ relpath ]
        
        for item in items:
            abspath = os.path.join(cls.basedir, item)
            cmd = Template(conf['env_chmod_command']).safe_substitute(path=abspath, mode=mode)
            cls._run_cmd(cmd)

class RcTestCase(SimpleTestCase):
    
    @classmethod
    def _setenv(cls):
        
        SimpleTestCase._setenv.im_func(cls)
        cls.rcfile = NamedTemporaryFile()
        cls.rcpath = cls.rcfile.name
        

    @classmethod
    def _write_rc(cls, rc_content):
        # Create rc to load
        cls.rcfile.write(rc_content)
        cls.rcfile.flush()

    @classmethod
    def _unsetenv(cls):
        SimpleTestCase._unsetenv.im_func(cls)    
        cls.rcfile.close()

    
class ProxyTestCase(RcTestCase):
    
    @classmethod
    def _setenv(cls):
        RcTestCase._setenv.im_func(cls)

        cls.proxyport = random.randint(50000,65000)
        start_new_thread(start_server, ('localhost', cls.proxyport))
        cls.dummyserverport = cls.proxyport+1
        start_new_thread(start_dummy_tcp_server, ('localhost', cls.dummyserverport))


    @classmethod
    def _unsetenv(cls):
        RcTestCase._unsetenv.im_func(cls)    

    
            
