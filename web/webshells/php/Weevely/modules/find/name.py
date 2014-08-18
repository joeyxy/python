

from core.moduleguess import ModuleGuess
from core.moduleexception import ModuleException, ProbeException
from core.argparse import ArgumentParser


class Name(ModuleGuess):
    '''Find files with matching name'''


    def _set_vectors(self):
        self.vectors.add_vector('php_recursive', 'shell.php', """swp('$rpath','$mode','$string',$recursion);
function ckdir($df, $f) { return ($f!='.')&&($f!='..')&&@is_dir($df); }
function match($f, $s, $m) { return preg_match(str_replace("%%STRING%%",$s,$m),$f); }
function swp($d, $m, $s,$r){ $h = @opendir($d);
while ($f = readdir($h)) { $df=$d.'/'.$f; if(($f!='.')&&($f!='..')&&match($f,$s,$m)) print($df."\n"); if(@ckdir($df,$f)&&$r) @swp($df, $m, $s, $r); }
if($h) { @closedir($h); } }""")
        self.vectors.add_vector("find" , 'shell.sh', "find $rpath $recursion $mode \"$string\" 2>/dev/null")
    
    def _set_args(self):
        self.argparser.add_argument('string', help='String to match')
        self.argparser.add_argument('-rpath', help='Remote starting path', default ='.', nargs='?')
        self.argparser.add_argument('-equal', help='Match if name is exactly equal (default: match if contains)', action='store_true', default=False)
        self.argparser.add_argument('-case', help='Case sensitive match (default: insenstive)', action='store_true', default=False)
        self.argparser.add_argument('-vector', choices = self.vectors.keys())
        self.argparser.add_argument('-no-recursion', help='Do not descend into subfolders', action='store_true', default=False)


    def _prepare_vector(self):
        
        self.formatted_args = { 'rpath' : self.args['rpath'] }
            
        if self.current_vector.name == 'find':

            if not self.args['equal']:
                self.formatted_args['string'] = '*%s*' % self.args['string']
            else:
                self.formatted_args['string'] = self.args['string']
            
            if not self.args['case']:
                self.formatted_args['mode'] = '-iname'
            else:
                self.formatted_args['mode'] = '-name'
                
            if self.args['no_recursion']:
                self.formatted_args['recursion'] = '-maxdepth 1'
            else:
                self.formatted_args['recursion'] = ''

        elif self.current_vector.name == 'php_recursive':
            
            self.formatted_args['string'] = self.args['string']

            if not self.args['equal']:
                self.formatted_args['mode'] = '/%%STRING%%/'
            else:
                self.formatted_args['mode'] = '/^%%STRING%%$/'
                
            if not self.args['case']:
                self.formatted_args['mode'] += 'i'
                
            
            if self.args['no_recursion']:
                self.formatted_args['recursion'] = 'False'
            else:
                self.formatted_args['recursion'] = 'True'
                

            
    def _stringify_result(self):
        
        # Listify output, to advantage other modules 
        self._output = self._result
        self._result = self._result.split('\n') if self._result else []
