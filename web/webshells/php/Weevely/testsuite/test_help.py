from baseclasses import SimpleTestCase
from tempfile import NamedTemporaryFile
import os, sys
sys.path.append(os.path.abspath('..'))
import modules.shell.sh
import modules.shell.php


class FSEnum(SimpleTestCase):
    
    def test_help(self):
        help_output = self._warn(":help" )
        self.assertRegexpMatches(help_output, '|[\s]module[\s]+|[\s]description[\s]+|[\n]{%i}' % (len(self.term.modhandler.modules_classes)+2))       
        self.assertNotRegexpMatches(help_output, '\n'*4)       
        
        help_shell_output = self._warn(":help shell" )
        sh_descr = modules.shell.sh.Sh.__doc__
        php_descr = modules.shell.php.Php.__doc__
        self.assertRegexpMatches(help_shell_output, '\[shell\.sh\] %s[\s\S]+usage:[\s\S]+\[shell\.php\] %s[\s\S]+usage:[\s\S]+' % (sh_descr, php_descr))
        self.assertNotRegexpMatches(help_shell_output, '\n'*4)       
        
        help_nonexistant_output = self._warn(":help nonexistant" )
        self.assertRegexpMatches(help_nonexistant_output, '')
        
        help_shell_sh_output = self._warn(":help shell.sh" )
        self.assertRegexpMatches(help_shell_sh_output, 'usage:[\s\S]+%s[\s\S]+positional arguments:[\s\S]+optional arguments:[\s\S]+stored arguments:[\s\S]+' % (sh_descr))
        self.assertNotRegexpMatches(help_shell_sh_output, '\n'*3)       
        