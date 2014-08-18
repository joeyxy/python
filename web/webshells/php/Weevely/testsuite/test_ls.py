from baseclasses import FolderFSTestCase
import os
from test import conf
from unittest import skipIf
import modules.file.ls


class ShellsLS(FolderFSTestCase):

        
    def test_ls(self):
        
        self.assertEqual(self._outp(':file.ls %s' % self.basedir), self.dirs[0])
        self.assertEqual(self._outp(':file.ls %s' % os.path.join(self.basedir,self.dirs[0])), self.dirs[1].split('/')[-1])
        self.assertEqual(self._outp(':file.ls %s' % os.path.join(self.basedir,self.dirs[1])), self.dirs[2].split('/')[-1])
        self.assertEqual(self._outp(':file.ls %s' % os.path.join(self.basedir,self.dirs[2])), self.dirs[3].split('/')[-1])
        self.assertEqual(self._outp(':file.ls %s' % os.path.join(self.basedir,self.dirs[3])), '')
        self.assertEqual(self._outp(':file.ls %s/.././/../..//////////////./../../%s/' % (self.basedir, self.basedir)), self.dirs[0])

        self.assertEqual(self._outp(':file.ls -vector ls_php %s' % os.path.join(self.basedir,self.dirs[3])), '')
        self.assertEqual(self._outp(':file.ls -vector ls_php %s/.././/../..//////////////./../../%s/' % (self.basedir, self.basedir)), self.dirs[0])
 
        # Unexistant and not-readable folders
        self.assertRegexpMatches(self._warn(':file.ls /asdsdadsa'), modules.file.ls.WARN_NO_SUCH_FILE)
        self.assertRegexpMatches(self._warn(':file.ls /root/'), modules.file.ls.WARN_NO_SUCH_FILE)
 
        # Not readable files
        self.assertEqual(self._outp(':file.ls /etc/shadow'), '/etc/shadow')
 
 
    @skipIf(not conf['shell_sh'], "Skipping shell.sh dependent tests")
    def test_system_ls(self):
        
        # Check vector correspondance
        self.assertEqual(self._outp(':file.ls -vector ls %s' % os.path.join(self.basedir,self.dirs[3])), self._outp(':file.ls -vector ls_php %s' % os.path.join(self.basedir,self.dirs[3])))
        self.assertEqual(self._outp(':file.ls -vector ls %s/.././/../..//////////////./../../%s/' % (self.basedir, self.basedir)), self._outp(':file.ls -vector ls_php %s/.././/../..//////////////./../../%s/' % (self.basedir, self.basedir)))

        # Check ls arguments
        self.assertRegexpMatches(self._outp(':file.ls -vector ls / -- -al'), 'root[\s]+root[\s]')
        