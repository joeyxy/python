from baseclasses import FolderFileFSTestCase
from test import conf
import os, sys
sys.path.append(os.path.abspath('..'))
import modules
from unittest import skipIf

class FSFindCheck(FolderFileFSTestCase):

    def setUp(self):
        self.sorted_files = sorted(['./%s' % x for x in self.filenames])
        self.sorted_folders = sorted(['./%s' % x for x in self.dirs] + ['.'])
        self.sorted_files_and_folders = sorted(self.sorted_files + self.sorted_folders)        

    def test_perms(self):
        
        self.assertEqual(self._path('cd %s' % self.basedir), self.basedir)
        self.assertEqual(sorted(self._outp(':find.perms').split('\n')), self.sorted_files_and_folders)
        self.assertEqual(sorted(self._outp(':find.perms -vector php_recursive').split('\n')), self.sorted_files_and_folders)
        self.assertEqual(sorted(self._outp(':find.perms -vector php_recursive -type f').split('\n')), self.sorted_files)
        self.assertEqual(sorted(self._outp(':find.perms -vector php_recursive -type d').split('\n')), self.sorted_folders)

    @skipIf(not conf['shell_sh'], "Skipping shell.sh dependent tests")
    def test_perms_sh(self):
        self.assertEqual(sorted(self._outp(':find.perms -vector find').split('\n')), self.sorted_files_and_folders)
        self.assertEqual(sorted(self._outp(':find.perms -vector find -type f').split('\n')), self.sorted_files)
        self.assertEqual(sorted(self._outp(':find.perms -vector find -type d').split('\n')), self.sorted_folders)


    def test_specific_perms(self):
        
        self.assertEqual(self._path('cd %s' % self.basedir), self.basedir)
        self.__class__._env_chmod(self.dirs[3], mode='0555', recursive=True) # -xr
        self.assertEqual(self._outp(':find.perms %s -writable' % self.dirs[3]), '')
        self.assertEqual(sorted(self._outp(':find.perms %s -executable' % self.dirs[3]).split('\n')), [self.dirs[3], self.filenames[3]])
        self.assertEqual(sorted(self._outp(':find.perms %s -readable' % self.dirs[3]).split('\n')), [self.dirs[3], self.filenames[3]])

        self.__class__._env_chmod(self.filenames[3], mode='0111') #--x 
        self.assertRegexpMatches(self._outp(':find.perms %s -vector php_recursive -executable' % self.dirs[3]), self.filenames[3])
        self.assertNotRegexpMatches(self._outp(':find.perms %s -vector php_recursive -writable' % self.dirs[3]), self.filenames[3])
        self.assertNotRegexpMatches(self._outp(':find.perms %s -vector php_recursive -readable' % self.dirs[3]), self.filenames[3])
        self.__class__._env_chmod(self.filenames[3], mode='0222') #-w-
        self.assertNotRegexpMatches(self._outp(':find.perms %s -vector php_recursive -executable' % self.dirs[3]), self.filenames[3])
        self.assertRegexpMatches(self._outp(':find.perms %s -vector php_recursive -writable' % self.dirs[3]), self.filenames[3])
        self.assertNotRegexpMatches(self._outp(':find.perms %s -vector php_recursive -readable' % self.dirs[3]), self.filenames[3])
        self.__class__._env_chmod(self.filenames[3], mode='0444') #r--
        self.assertNotRegexpMatches(self._outp(':find.perms %s -vector php_recursive -executable' % self.dirs[3]), self.filenames[3])
        self.assertNotRegexpMatches(self._outp(':find.perms %s -vector php_recursive -writable' % self.dirs[3]), self.filenames[3])
        self.assertRegexpMatches(self._outp(':find.perms %s -vector php_recursive -readable' % self.dirs[3]), self.filenames[3])

    def test_no_recursion(self):

        self.assertEqual(self._path('cd %s' % self.basedir), self.basedir)
        self.assertEqual(sorted(self._res(':find.perms -no-recursion')), self.sorted_files_and_folders[:2])
        self.assertEqual(sorted(self._res(':find.perms -vector php_recursive -no-recursion')), self.sorted_files_and_folders[:2])
        self.assertEqual(sorted(self._res(':find.perms -vector php_recursive -type f -no-recursion')), [])
        self.assertEqual(sorted(self._res(':find.perms -vector php_recursive -type d -no-recursion')), self.sorted_folders[:2])

    @skipIf(not conf['shell_sh'], "Skipping shell.sh dependent tests")
    def test_no_recursion_sh(self):

        self.assertEqual(self._path('cd %s' % self.basedir), self.basedir)
        self.assertEqual(sorted(self._res(':find.perms -no-recursion')), self.sorted_files_and_folders[:2])
        self.assertEqual(sorted(self._res(':find.perms -vector find -no-recursion')), self.sorted_files_and_folders[:2])
        self.assertEqual(sorted(self._res(':find.perms -vector find -no-recursion')), self.sorted_files_and_folders[:2])
        self.assertEqual(sorted(self._res(':find.perms -vector find -type f -no-recursion')), [])
        self.assertEqual(sorted(self._res(':find.perms -vector find -type d -no-recursion')), self.sorted_folders[:2])

    @skipIf(not conf['shell_sh'] , "Skipping shell.sh dependent tests")
    def test_equal_vector(self):

        self.assertEqual(self._path('cd %s' % self.basedir), self.basedir)
        
        # Disable shell.sh stderr to avoid "file not found" warning message pollution
        self._res(":set shell.sh -no-stderr")
        
        self.assertEqual(sorted(self._res(':find.perms -vector php_recursive')), sorted(self._res(':find.perms -vector find')))
        self.assertEqual(sorted(self._res(':find.perms -vector php_recursive -writable')), sorted(self._res(':find.perms -vector find -writable')))
        self.assertEqual(sorted(self._res(':find.perms -vector php_recursive -readable')), sorted(self._res(':find.perms -vector find -readable')))
        self.assertEqual(sorted(self._res(':find.perms -vector php_recursive -executable')), sorted(self._res(':find.perms -vector find -executable')))

        self.assertEqual(sorted(self._res(':find.perms /var/log/ -vector php_recursive ')), sorted(self._res(':find.perms /var/log/ -vector find')))
        self.assertEqual(sorted(self._res(':find.perms /var/log/ -vector php_recursive -writable')), sorted(self._res(':find.perms /var/log/ -vector find -writable')))
        self.assertEqual(sorted(self._res(':find.perms /var/log/ -vector php_recursive -readable')), sorted(self._res(':find.perms /var/log/ -vector find -readable')))
        self.assertEqual(sorted(self._res(':find.perms /var/log/ -vector php_recursive -executable')), sorted(self._res(':find.perms /var/log/ -vector find -executable')))


    