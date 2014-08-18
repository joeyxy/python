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
from core.sessions import default_session, WARN_NOT_FOUND, WARN_BROKEN_SESS, WARN_LOAD_ERR

class Sessions(SimpleTestCase):
    
    def _install_new_bd(self, relpathfrom, phpbdname):
 
        self.__class__._env_cp(relpathfrom, phpbdname)

        web_base_url = '%s%s' %  (conf['env_base_web_url'], self.basedir.replace(conf['env_base_web_dir'],''))
        phpbd_url = os.path.join(web_base_url, phpbdname)
        
        return phpbd_url
    
    def test_sessions(self):
        
        phpbd_pwd = randstr(4)
        temp_file1 = NamedTemporaryFile(); temp_file1.close(); 
        temp_file2 = NamedTemporaryFile(); temp_file2.close(); 
        temp_file3 = NamedTemporaryFile(); temp_file2.close(); 
        
        self.assertEqual(self._res(':generate.php %s %s'  % (phpbd_pwd, temp_file1.name)),temp_file1.name)
        self.assertEqual(self._res(':generate.php %s %s'  % (phpbd_pwd, temp_file2.name)),temp_file2.name)
        self.assertEqual(self._res(':generate.php %s %s'  % (phpbd_pwd, temp_file3.name)),temp_file3.name)
        
        url1 = self._install_new_bd(temp_file1.name, '%s.php' % randstr(5))
        url2 = self._install_new_bd(temp_file2.name, '%s.php' % randstr(5))
        url3 = self._install_new_bd(temp_file3.name, '%s.php' % randstr(5))
        
        # Check current session
        curr1 = self.term.modhandler.sessions.current_session_name
        outp = self._warn(':session')
        self.assertEqual(outp, "Current session: '%s'%sLoaded: '%s'%sAvailable: '%s'%s%s" % (curr1, os.linesep, curr1, os.linesep, curr1, os.linesep, os.linesep))
        
        # Load bd1 by url
        outp = self._warn(':session %s %s' % (url1, phpbd_pwd))
        curr2 = self.term.modhandler.sessions.current_session_name
        outp = self._warn(':session')
        self.assertEqual(outp, "Current session: '%s'%sLoaded: '%s'%sAvailable: '%s'%s%s" % (curr2, os.linesep, "', '".join(sorted([curr2, curr1])), os.linesep, curr1, os.linesep,os.linesep))
        
        # Load bd2 by session file
        outp = self._warn(':session %s %s' % (url1, phpbd_pwd))
        curr2 = self.term.modhandler.sessions.current_session_name
        outp = self._warn(':session')
        self.assertEqual(outp, "Current session: '%s'%sLoaded: '%s'%sAvailable: '%s'%s%s" % (curr2, os.linesep, "', '".join(sorted([curr2, curr1])), os.linesep, curr1, os.linesep,os.linesep))
                
        # Create bd3 session file, not in session
        curr3 = '/tmp/%s.session' % randstr(5)
        session = default_session.copy()
        session['global']['url'] = url3
        session['global']['password'] = phpbd_pwd
        self.term.modhandler.sessions._dump_session(session, curr3)
        
        # Load bd3 by session file
        outp = self._warn(':session %s' % (curr3))
        outp = self._warn(':session')
        self.assertEqual(outp, "Current session: '%s'%sLoaded: '%s'%sAvailable: '%s'%s%s" % (curr3, os.linesep, "', '".join(sorted([curr2, curr3, curr1])), os.linesep, curr1, os.linesep,os.linesep))

        # Unexistant session file
        self.assertRegexpMatches(self._warn(':session /tmp/asd'), WARN_NOT_FOUND)

        # Unexpected session file
        self.assertRegexpMatches(self._warn(':session /etc/motd'), WARN_BROKEN_SESS)

        # Create session file without fields
        curr4 = '/tmp/%s.session' % randstr(5)
        open(curr4,'w').write("""[global]
url = asd
username = 
hostname = 
rcfile =""")
        
        # Broken session file
        self.assertRegexpMatches(self._warn(':session %s' % curr4), WARN_BROKEN_SESS)
        
        # Load broken session file at start
        call = "'echo'"
        command = '%s session %s %s' % (conf['cmd'], curr4, call)
        status, output = getstatusoutput(command)
        self.assertRegexpMatches(output, WARN_BROKEN_SESS)
        