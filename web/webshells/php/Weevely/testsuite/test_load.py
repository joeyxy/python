from baseclasses import RcTestCase
from tempfile import NamedTemporaryFile
from commands import getstatusoutput
from test import conf
from unittest import skipIf
import ConfigParser
from core.sessions import default_session 
import os

rc_content = """
:shell.php print(\'W\');
:set shell.php -debug 1
echo EE
# echo X
# shell.php print(\'X\');
:set shell.php
echo VELY
"""

@skipIf(not conf['shell_sh'], "Skipping shell.sh dependent tests")
class Load(RcTestCase):

    def test_load(self):
        
        self.__class__._write_rc(rc_content)
        
        self.assertEqual(self._outp(':load %s' % self.__class__.rcpath), 'WEEVELY')
        self.assertRegexpMatches(self._warn(':load %s_UNEXISTANT' % self.__class__.rcpath), 'Error opening')
        
        # Dump session file
        session_name = self.__class__.rcpath + '.session'

        session = default_session.copy()
        session['global']['url'] = self.term.modhandler.url
        session['global']['password'] = self.term.modhandler.password
        session['global']['rcfile'] = self.__class__.rcpath
        self.term.modhandler.sessions._dump_session(session, session_name)
        
        call = "'echo'"
        command = '%s session %s %s' % (conf['cmd'], session_name, call)
        status, output = getstatusoutput(command)
        
        # Remove session
        os.remove(session_name)
        
        self.assertRegexpMatches(output, '\nW[\s\S]+\nEE[\s\S]+\nVELY')  
        