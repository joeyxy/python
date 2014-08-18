from baseclasses import FolderFileFSTestCase
from test import conf
import os, sys
sys.path.append(os.path.abspath('..'))
import modules
import modules.file.check

class FSCheck(FolderFileFSTestCase):

    def test_check(self):
        
        self.assertEqual(self._outp(':file.check unexistant exists'), 'False')
        self.assertEqual(self._outp(':file.check %s read' % self.basedir), 'True')
        self.assertEqual(self._outp(':file.check %s exec' % self.basedir), 'True')
        self.assertEqual(self._outp(':file.check %s isfile' % self.basedir), 'False')
        self.assertEqual(self._outp(':file.check %s exists' % self.basedir), 'True')
        self.assertEqual(self._outp(':file.check %s isfile' % os.path.join(self.basedir,self.filenames[0])), 'True')
        self.assertEqual(self._outp(':file.check %s md5' % os.path.join(self.basedir,self.filenames[0])), 'c4ca4238a0b923820dcc509a6f75849b')
        self.assertEqual(self._res(':file.check %s size' % os.path.join(self.basedir,self.filenames[0])), 1)
        self.assertRegexpMatches(self._warn(':file.check unexistant size'), modules.file.check.WARN_INVALID_VALUE)

            