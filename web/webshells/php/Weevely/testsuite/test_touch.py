from baseclasses import FolderFileFSTestCase
from tempfile import NamedTemporaryFile
import os

class Touch(FolderFileFSTestCase):

        
    def test_ts(self):
        
        filename1 = os.path.join(self.basedir,self.filenames[1])
        dir1 = os.path.join(self.basedir,self.dirs[1])
        
        # Set epoch, get epoch
        self.assertEqual(self._res(""":file.touch -epoch 1 %s """ % (filename1)), self._res(""":file.check %s time_epoch""" % (filename1)))

        # Set timestamp, get epoch
        # 23 Apr 2013 09:15:53 GMT -> 1366701353 
        self.assertEqual(self._res(""":file.touch -time '23 Apr 2013 09:15:53' %s """ % (filename1)),1366701353);
        self.assertEqual(self._res(""":file.check %s time_epoch""" % (filename1)),1366701353)

        # Set timestamp of dir1 as equal as filename1
        self.assertEqual(self._res(""":file.touch -ref %s %s """ % (filename1, dir1)),1366701353);
        self.assertEqual(self._res(""":file.check %s time_epoch""" % (dir1)),1366701353)

        # Set file1 with current timestamp
        self.assertNotEqual(self._res(""":file.touch %s """ % (filename1)),1366701353);
        
        # Reset file1 with oldest timestamp (dir1 one)
        self.assertEqual(self._res(""":file.touch -oldest %s """ % (filename1)),1366701353);
        
        