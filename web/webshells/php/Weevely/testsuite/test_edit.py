from baseclasses import SimpleTestCase
from tempfile import NamedTemporaryFile
from os import path
from core.utils import randstr
import os, sys
sys.path.append(os.path.abspath('..'))
from test import conf
import modules.file.edit

class Edit(SimpleTestCase):
    
    def setUp(self):

        self.nonwritable_folder = '%s/nonwritable' % conf['env_base_writable_web_dir']
        self.writable_file = '%s/writable' % self.nonwritable_folder
        self.writable_file2 = '%s/writable2' % self.nonwritable_folder
        self.writable_file3 = '%s/writable3' % conf['env_base_writable_web_dir']
        
        self.editor = "echo -n 1 >> "
        
        self.__class__._env_mkdir(self.nonwritable_folder)
        self.__class__._env_newfile(self.writable_file, content='1')
        self.__class__._env_newfile(self.writable_file2, content='1')
        self.__class__._env_chmod(self.writable_file, mode='0777')
        self.__class__._env_chmod(self.nonwritable_folder, mode='0555')        
        
    
    def test_edit(self):
        
        temp_filename = path.join('/tmp', randstr(4) )
        self.assertTrue(self._res(""":file.edit %s -editor "%s" """ % (temp_filename, self.editor)))
        self.assertTrue(self._res(""":file.edit %s -editor "%s" """ % (temp_filename, self.editor)))
        
        self.assertEqual(self._res(":file.read %s" % temp_filename), '11')
        
        self.assertRegexpMatches(self._warn(""":file.edit /tmp/non/existant -editor "%s" """ % (self.editor)), modules.file.edit.WARN_UPLOAD_FAILED)
        self.assertRegexpMatches(self._warn(""":file.edit /etc/protocols -editor "%s" """ % (self.editor)), modules.file.edit.WARN_UPLOAD_FAILED)
        

    def test_edit_on_unwritable_folder(self):
        
        self.assertTrue(self._res(""":file.edit %s -editor "%s" """ % (self.writable_file, self.editor)))
        self.assertEqual(self._res(":file.read %s" % self.writable_file), '11')
        
        
    def test_keeping_timestamp(self):
        
        # Edit keeping timestamp
        self.assertEqual(self._res(""":file.touch -epoch 1 %s """ % (self.writable_file2)), 1)
        self.assertTrue(self._res(""":file.edit %s -editor "%s" -keep-ts""" % (self.writable_file2, self.editor)))
        self.assertEqual(self._res(":file.read %s" % self.writable_file2), '11')
        self.assertEqual(self._res(""":file.check %s time_epoch""" % (self.writable_file2,)), 1)
        
        # Edit unkeeping timestamp
        self.assertTrue(self._res(""":file.edit %s -editor "%s" """ % (self.writable_file2, self.editor)))
        self.assertNotEqual(self._res(""":file.check %s time_epoch""" % (self.writable_file2,)), 1)
        
        # Edit new file keeping timestamp (?)
        self.assertTrue(self._res(""":file.edit %s -editor "%s" -keep-ts""" % (self.writable_file3, self.editor)))
        self.assertEqual(self._res(":file.read %s" % self.writable_file3), '1')
        self.assertNotEqual(self._res(""":file.check %s time_epoch""" % (self.writable_file3,)), 1)
        

        
    def tearDown(self):
        
        self.__class__._env_chmod(self.nonwritable_folder, mode='0777')
        self.__class__._env_rm(self.writable_file)
        self.__class__._env_rm(self.writable_file2)
        self.__class__._env_rm(self.writable_file3)
        self.__class__._env_rm(self.nonwritable_folder)
        
        
        