from baseclasses import FolderFileFSTestCase
from tempfile import NamedTemporaryFile
import sys, os
sys.path.append(os.path.abspath('..'))
import modules
from unittest import skipIf
from test import conf


class FSDownload(FolderFileFSTestCase):

    def setUp(self):
        self.temp_path = NamedTemporaryFile(); self.temp_path.close(); 
        self.remote_path = os.path.join(self.basedir, self.filenames[0])
        self.remote_path_empty = os.path.join(self.basedir, self.filenames[0] + '_empty')
        
        self.__class__._env_newfile(self.remote_path_empty, content='')

    def test_download(self):
        
        self.assertRegexpMatches(self._warn(':file.download /etc/gne /tmp/asd') , modules.file.download.WARN_NO_SUCH_FILE)
        self.assertRegexpMatches(self._warn(':file.download /etc/passwd /tmpsaddsaas/asd') , 'Errno')
        self.assertRegexpMatches(self._warn(':file.download /etc/shadow /tmp/asd') , modules.file.download.WARN_NO_SUCH_FILE)

        # False and True printout
        self.assertEqual(self._outp(':file.download /etc/issue %s'  % (self.temp_path.name)), 'True')
        self.assertEqual(self._outp(':file.download /etc/issue2 %s'  % (self.temp_path.name)).rstrip().split('\n')[-1], 'False')

        self.assertEqual(self._res(':file.download %s %s -vector file'  % (self.remote_path, self.temp_path.name)), 'c4ca4238a0b923820dcc509a6f75849b')
        self.assertEqual(self._res(':file.download %s %s -vector fread'  % (self.remote_path, self.temp_path.name)), 'c4ca4238a0b923820dcc509a6f75849b')
        self.assertEqual(self._res(':file.download %s %s -vector file_get_contents'  % (self.remote_path, self.temp_path.name)), 'c4ca4238a0b923820dcc509a6f75849b')
        self.assertEqual(self._res(':file.download %s %s -vector copy'  % (self.remote_path, self.temp_path.name)), 'c4ca4238a0b923820dcc509a6f75849b')
        self.assertEqual(self._res(':file.download %s %s -vector symlink'  % (self.remote_path, self.temp_path.name)), 'c4ca4238a0b923820dcc509a6f75849b')

        #Test download empty file
        self.assertEqual(self._outp(':file.download %s %s'  % (self.remote_path_empty, self.temp_path.name)), 'True')
        self.assertEqual(self._res(':file.download %s %s'  % (self.remote_path_empty, self.temp_path.name)), 'd41d8cd98f00b204e9800998ecf8427e')
        


    @skipIf(not conf['shell_sh'], "Skipping shell.sh dependent tests")
    def test_download_sh(self):
        self.assertEqual(self._res(':file.download %s %s -vector base64'  % (self.remote_path, self.temp_path.name)), 'c4ca4238a0b923820dcc509a6f75849b')
        
    def test_read(self):
        
        self.assertRegexpMatches(self._warn(':file.read /etc/gne') , modules.file.download.WARN_NO_SUCH_FILE)
        self.assertRegexpMatches(self._warn(':file.read /etc/shadow') , modules.file.download.WARN_NO_SUCH_FILE)

        self.assertEqual(self._outp(':file.read %s -vector file'  % (self.remote_path)), '1')
        self.assertEqual(self._outp(':file.read %s -vector fread'  % (self.remote_path)), '1')
        self.assertEqual(self._outp(':file.read %s -vector file_get_contents'  % (self.remote_path)), '1')
        self.assertEqual(self._outp(':file.read %s -vector copy'  % (self.remote_path)), '1')
        self.assertEqual(self._outp(':file.read %s -vector symlink'  % (self.remote_path)), '1')
        
    @skipIf(not conf['shell_sh'], "Skipping shell.sh dependent tests")
    def test_read_sh(self):
        self.assertEqual(self._outp(':file.read %s -vector base64'  % (self.remote_path)), '1')
        