from baseclasses import SimpleTestCase
from core.utils import randstr
from test import conf
from unittest import skipIf
import sys, os
sys.path.append(os.path.abspath('..'))


@skipIf(not conf['shell_sh'], "Skipping shell.sh dependent tests")
class SetSh(SimpleTestCase):

    def test_set_sh(self):
        
        module_params = [ x.dest for x in self.term.modhandler.load('shell.sh').argparser._actions if x.dest != 'help' ]

        
        self.assertRegexpMatches(self._res(':shell.sh ls'), '.\n..')

        params_print = self._warn(':help shell.sh')
        # Basic parameter output
        self.assertRegexpMatches(params_print.strip().split('\n')[-1], 'stored arguments: %s=\'.*\'' % '=\'.*\'[\s]+'.join(module_params) )
        
        # Module should have an already set vector
        self.assertRegexpMatches(params_print, 'vector=\'[\w]+\'')        

        #Use shell.php precmd
        self._res(':set shell.php -precmd echo("WEEV");')
        self.assertRegexpMatches(self._res(':shell.sh echo ILY'), 'WEEVILY')


class Set(SimpleTestCase):

        
    def test_set(self):
        
        module_params = [ x.dest for x in self.term.modhandler.load('shell.sh').argparser._actions if x.dest != 'help' ]
        
        filename_rand = randstr(4)
        filepath_rand = os.path.join(self.basedir, filename_rand)

        #Use shell.php precmd
        self._res(':set shell.php -precmd echo("WEEV");')
        self.assertRegexpMatches(self._res(':shell.php print("ILY");'), 'WEEVILY')
        
        #Reset parameters
        self._res(':set shell.sh')
        params_print = self._warn(':help shell.sh')
        self.assertRegexpMatches(params_print.strip().split('\n')[-1], 'stored arguments: %s=\'\'' % '=\'\'[\s]+'.join(module_params) )
        
        #Set wrongly parameter with choices
        #Expected arguments
        self.assertRegexpMatches(self._warn(':set shell.php -precmd'), 'argument -precmd: expected at least one argument')
        #Expected int
        self.assertRegexpMatches(self._warn(':set shell.php -debug asd'), 'argument -debug: invalid int value: \'asd\'')
        #Expected dict
        self.assertRegexpMatches(self._warn(':set shell.php -post 1'), 'argument -post: invalid dict value: \'1\'')
        #Expected list - strings are easily castable as list, so this don\'t fail. not a big deal
        #self.assertRegexpMatches(self._warn(':set bruteforce.sqlusers -wordlist {}'), 'argument -wordlist: invalid list value: \'1\'')        
