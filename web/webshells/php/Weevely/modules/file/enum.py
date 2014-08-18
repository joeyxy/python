from core.module import Module
from core.moduleexception import ProbeException
from core.argparse import ArgumentParser
from ast import literal_eval
from core.prettytable import PrettyTable
import os


class Enum(Module):
    '''Enumerate remote paths'''

    def _set_vectors(self):
        self.support_vectors.add_vector('getperms','shell.php',  "$f='$rpath'; if(file_exists($f)) { print('e'); if(is_readable($f)) print('r'); if(is_writable($f)) print('w'); if(is_executable($f)) print('x'); }")
    
    def _set_args(self):
        self.argparser.add_argument('pathfile', help='Enumerate paths written in PATHFILE')
        self.argparser.add_argument('-printall', help='Print also paths not found', action='store_true')
        self.argparser.add_argument('-pathlist', help='Enumerate paths written as "[\'/path/1\', \'/path/2\']"', type=type([]), default=[])




    def _prepare(self):
        
        self._result = {}
        
        if not self.args['pathlist']:
            try:
                self.args['pathlist']=open(os.path.expanduser(self.args['pathfile']),'r').read().splitlines()
            except:
                raise ProbeException(self.name,  "Error opening path list \'%s\'" % self.args['pathfile'])
                

    def _probe(self):
        
        for entry in self.args['pathlist']:
            self._result[entry] = ['', '', '', '']
            perms = self.support_vectors.get('getperms').execute({'rpath' : entry})
            
            if perms:
                if 'e' in perms: self._result[entry][0] = 'exists'
                if 'r' in perms: self._result[entry][1] = 'readable'
                if 'w' in perms: self._result[entry][2] = 'writable'
                if 'x' in perms: self._result[entry][3] = 'executable'

    def _stringify_result(self):
    
        table = PrettyTable(['']*5)
        table.align = 'l'
        table.header = False
        
        for field in self._result:
            if self._result[field] != ['', '', '', ''] or self.args['printall']:
                table.add_row([field] + self._result[field])
                
        self._output = table.get_string()
        