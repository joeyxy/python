from baseclasses import ProxyTestCase
from tempfile import NamedTemporaryFile
from os import path, remove
from commands import getstatusoutput
from test import conf
import PythonProxy
import os, sys
sys.path.append(os.path.abspath('..'))
import core.http.request
from core.sessions import default_session 

rc_content = """
:set shell.php -proxy http://localhost:%i
:shell.php echo(\'WE\'.\'EV\'.\'ELY\');
"""


class SetProxy(ProxyTestCase):
        
    def test_proxy(self):
        
        ## Runtime test
        self.assertRegexpMatches(self._warn(':set shell.php -proxy http://localhost:%i' % self.__class__.proxyport), 'proxy=\'http://localhost:%i\'' % self.__class__.proxyport)
        self.assertEqual(PythonProxy.proxy_counts,0)
        self.assertEqual(self._outp(':shell.php echo(1+1);'), '2')
        self.assertGreater(PythonProxy.proxy_counts,0)
        
        ## Rc load at start test
        PythonProxy.proxy_counts=0

        self.__class__._write_rc(rc_content % self.__class__.proxyport)
        
        # Dump session file
        session_name = self.__class__.rcpath + '.session'

        session = default_session.copy()
        session['global']['url'] = self.term.modhandler.url
        session['global']['password'] = self.term.modhandler.password
        session['global']['rcfile'] = self.__class__.rcpath
        self.term.modhandler.sessions._dump_session(session, session_name)
        
        self.assertEqual(PythonProxy.proxy_counts,0)
        call = "'echo'"
        command = '%s session %s %s' % (conf['cmd'], session_name, call)
        status, output = getstatusoutput(command)
        
        self.assertRegexpMatches(output, '\nWEEVELY')  
        self.assertGreater(PythonProxy.proxy_counts,0)
        
        # Verify that final socket is never contacted without proxy 
        # Dump new session file with unexistant php proxy
        session = default_session.copy()
        session['global']['url'] = 'http://localhost:%i/unexistant.php' % self.__class__.dummyserverport
        session['global']['password'] = self.term.modhandler.password
        session['global']['rcfile'] = self.__class__.rcpath
        self.term.modhandler.sessions._dump_session(session, session_name)
        
        PythonProxy.proxy_counts=0
        fake_url = 'http://localhost:%i/fakebd.php' % self.__class__.dummyserverport
        call = "'echo'"
        command = '%s session %s %s' % (conf['cmd'], session_name, call)
        
        self.assertEqual(PythonProxy.proxy_counts,0)
        self.assertEqual(PythonProxy.dummy_counts,0)
        status, output = getstatusoutput(command)
        self.assertGreater(PythonProxy.proxy_counts,0)
        self.assertGreater(PythonProxy.dummy_counts,0)
        
        # Count that Client never connect to final dummy endpoint without passing through proxy
        self.assertGreaterEqual(PythonProxy.proxy_counts, PythonProxy.dummy_counts)
        
        self.assertRegexpMatches(self._warn(':set shell.php -proxy wrong://localhost:%i' % self.__class__.proxyport), 'proxy=\'wrong://localhost:%i\'' % self.__class__.proxyport)
        self.assertRegexpMatches(self._warn(':shell.php echo(1+1);'), core.http.request.WARN_UNCORRECT_PROXY)
        
        