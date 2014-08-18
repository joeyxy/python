from baseclasses import FolderFSTestCase
import os
from test import conf
from unittest import skipIf


@skipIf(not conf['shell_sh'], "Skipping shell.sh dependent tests")
class ShellsFSBrowse(FolderFSTestCase):

        
    def test_ls(self):
        
        self.assertEqual(self._outp('ls %s' % self.basedir), self.dirs[0])
        self.assertEqual(self._outp('ls %s' % os.path.join(self.basedir,self.dirs[0])), self.dirs[1].split('/')[-1])
        self.assertEqual(self._outp('ls %s' % os.path.join(self.basedir,self.dirs[1])), self.dirs[2].split('/')[-1])
        self.assertEqual(self._outp('ls %s' % os.path.join(self.basedir,self.dirs[2])), self.dirs[3].split('/')[-1])
        self.assertEqual(self._outp('ls %s' % os.path.join(self.basedir,self.dirs[3])), '')
        self.assertEqual(self._outp('ls %s/.././/../..//////////////./../../%s/' % (self.basedir, self.basedir)), self.dirs[0])

    def test_cwd(self):
        
        
        self.assertEqual(self._path('cd %s' % self.basedir), self.basedir)
        self.assertEqual(self._path('cd %s' % os.path.join(self.basedir,self.dirs[3])), os.path.join(self.basedir,self.dirs[3]))
        self.assertEqual(self._path('cd .'), os.path.join(self.basedir,self.dirs[3]))
        self.assertEqual(self._path('cd ..'), os.path.join(self.basedir,self.dirs[2]))
        self.assertEqual(self._path('cd ..'), os.path.join(self.basedir,self.dirs[1]))
        self.assertEqual(self._path('cd ..'), os.path.join(self.basedir,self.dirs[0]))
        self.assertEqual(self._path('cd ..'), self.basedir)
        self.assertEqual(self._path('cd %s' % os.path.join(self.basedir,self.dirs[3])), os.path.join(self.basedir,self.dirs[3]))
        self.assertEqual(self._path('cd .././/../..//////////////./../%s/../' % self.dirs[0]), self.basedir)
