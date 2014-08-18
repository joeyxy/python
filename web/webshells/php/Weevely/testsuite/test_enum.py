from baseclasses import SimpleTestCase
from tempfile import NamedTemporaryFile
import os


class FSEnum(SimpleTestCase):
    
    def test_enum(self):
        
        
        writable_file_path = os.path.join(self.basedir,'writable')
        self.__class__._env_newfile(writable_file_path)
        
        expected_enum_map = {
                    '/etc/passwd': ['exists', 'readable', '', ''],
                    writable_file_path: ['exists', 'readable', 'writable', ''],
                    '/etc/shadow': ['exists', '', '', ''],
                    'unexistant': ['', '', '', '']
                    }
        
        temp_path = NamedTemporaryFile(); 
        temp_path.write('\n'.join(expected_enum_map.keys()))
        temp_path.flush() 
        
        self.assertEqual(self._res(":file.enum a -pathlist \"%s\"" % str(expected_enum_map.keys())), expected_enum_map)        
        self.assertNotRegexpMatches(self._outp(":file.enum a -pathlist \"%s\"" % str(expected_enum_map.keys())), 'unexistant')        
        self.assertRegexpMatches(self._outp(":file.enum a -pathlist \"%s\" -printall" % str(expected_enum_map.keys())), 'unexistant')        

        self.assertEqual(self._res(":file.enum %s" % temp_path.name), expected_enum_map)        
        self.assertNotRegexpMatches(self._outp(":file.enum %s" % temp_path.name), 'unexistant')        
        self.assertRegexpMatches(self._outp(":file.enum %s -printall" % temp_path.name), 'unexistant')        
        
        temp_path.close();