from baseclasses import SimpleTestCase, FolderFSTestCase
from test import conf
from tempfile import NamedTemporaryFile
from unittest import skipIf
import os


class FSUserFiles(SimpleTestCase):
    
    @skipIf(not conf['permtest'] or "false" in conf['permtest'].lower(), "Skipping permission tests")
    def test_userfiles(self):
        
        expected_enum_map = {
            os.path.join(conf['permtest_home_path'],conf['permtest_path_1']): ['exists', 'readable', '', ''],
            os.path.join(conf['permtest_home_path'],conf['permtest_path_2']): ['exists', 'readable', '', '']
            }
        
        path_list = [conf['permtest_path_1'], conf['permtest_path_2'] ]
        
        temp_path = NamedTemporaryFile(); 
        temp_path.write('\n'.join(path_list)+'\n')
        temp_path.flush() 
        
        self.assertDictContainsSubset(expected_enum_map, self._res(":audit.userfiles"))
        self.assertDictContainsSubset(expected_enum_map, self._res(":audit.userfiles -pathlist \"%s\"" % str(path_list)))
        self.assertDictContainsSubset(expected_enum_map, self._res(":audit.userfiles -auto-home"))
        self.assertDictContainsSubset(expected_enum_map, self._res(":audit.userfiles -pathfile %s" % temp_path.name))

        temp_path.close()
      
        print 'Remember to restore \'%s\' permission to \'700\'' % conf['permtest_home_path']