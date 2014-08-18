from core.module import Module
from core.argparse import ArgumentParser


class Suidsgid(Module):
    '''Find files with superuser flags'''
    def _set_vectors(self):
        self.support_vectors.add_vector( "find" , 'shell.sh', "find $rpath $perm 2>/dev/null")
    
        
    def _set_args(self):
        self.argparser.add_argument('-rpath', help='Remote starting path', default='/')
        self.argparser.add_argument('-suid', help='Find only suid', action='store_true')
        self.argparser.add_argument('-sgid', help='Find only sgid', action='store_true')
        
    
    def _probe(self):
        
        if self.args['suid']:
            self.args['perm'] = '-perm -04000'
        elif self.args['sgid']:
            self.args['perm'] = '-perm -02000'
        else:
            self.args['perm'] = '-perm -04000 -o -perm -02000'
            
        self._result = self.support_vectors.get('find').execute(self.args)
        
    def _stringify_result(self):
        
        # Listify output, to advantage other modules 
        self._output = self._result
        self._result = self._result.split('\n') if self._result else []