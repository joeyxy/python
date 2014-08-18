

from core.moduleguess import ModuleGuess
from core.moduleexception import ModuleException
from core.argparse import ArgumentParser


class Perms(ModuleGuess):
    '''Find files with write, read, execute permissions'''


    def _set_vectors(self):
        self.vectors.add_vector('php_recursive', 'shell.php', """$fdir='$rpath';$ftype='$type';$fattr='$attr';$fqty='$first';$recurs=$recursion;
swp($fdir, $fdir,$ftype,$fattr,$fqty,$recurs); 
function ckprint($df,$t,$a) { if(cktp($df,$t)&&@ckattr($df,$a)) { print($df."\\n"); return True;}   }
function ckattr($df, $a) { $w=strstr($a,"w");$r=strstr($a,"r");$x=strstr($a,"x"); return ($a=='')||(!$w||is_writable($df))&&(!$r||is_readable($df))&&(!$x||is_executable($df)); }
function cktp($df, $t) { return ($t==''||($t=='f'&&@is_file($df))||($t=='d'&&@is_dir($df))); }
function swp($fdir, $d, $t, $a, $q,$r){ 
if($d==$fdir && ckprint($d,$t,$a) && ($q!="")) return; 
$h=@opendir($d); while ($f = @readdir($h)) { if(substr($fdir,0,1)=='/') { $df='/'; } else { $df=''; }
$df.=join('/', array(trim($d, '/'), trim($f, '/')));
if(($f!='.')&&($f!='..')&&ckprint($df,$t,$a) && ($q!="")) return;
if(($f!='.')&&($f!='..')&&cktp($df,'d')&&$r){@swp($fdir, $df, $t, $a, $q,$r);}
} if($h) { closedir($h); } }""")
        self.vectors.add_vector("find" , 'shell.sh', "find $rpath $recursion $type $attr $first 2>/dev/null")
    
    def _set_args(self):
        self.argparser.add_argument('rpath', help='Remote starting path', default ='.', nargs='?')
        self.argparser.add_argument('-first', help='Quit after first match', action='store_true')
        self.argparser.add_argument('-type', help='File type',  choices = ['f','d'])
        self.argparser.add_argument('-writable', help='Match writable files', action='store_true')
        self.argparser.add_argument('-readable', help='Matches redable files', action='store_true')
        self.argparser.add_argument('-executable', help='Matches executable files', action='store_true')
        self.argparser.add_argument('-vector', choices = self.vectors.keys())
        self.argparser.add_argument('-no-recursion', help='Do not descend into subfolders', action='store_true', default=False)


    def _prepare_vector(self):
        
        self.formatted_args = { 'rpath' : self.args['rpath'] }
        
        if self.current_vector.name == 'find':
            
            # Set first
            self.formatted_args['first'] = '-print -quit' if self.args['first'] else ''
            
            # Set type
            type = self.args['type'] if self.args['type'] else ''
            if type:
                type = '-type %s' % type
            self.formatted_args['type'] = type
                    
            # Set attr
            self.formatted_args['attr'] = '-writable' if self.args['writable'] else ''
            self.formatted_args['attr'] += ' -readable' if self.args['readable'] else ''
            self.formatted_args['attr'] += ' -executable' if self.args['executable'] else ''
            
            # Set recursion
            self.formatted_args['recursion'] =  ' -maxdepth 1 ' if self.args['no_recursion'] else ''

        else:
            # Vector.name = php_find
            # Set first
            self.formatted_args['first'] = '1' if self.args['first'] else ''
            
            # Set type
            self.formatted_args['type']  = self.args['type'] if self.args['type'] else ''
            
            # Set attr
            self.formatted_args['attr'] = 'w' if self.args['writable'] else ''
            self.formatted_args['attr'] += 'r' if self.args['readable'] else ''
            self.formatted_args['attr'] += 'x' if self.args['executable'] else ''
            
            # Set recursion
            self.formatted_args['recursion'] = not self.args['no_recursion']
            
            
    def _stringify_result(self):
        
        # Listify output, to advantage other modules 
        self._output = self._result
        self._result = self._result.split('\n') if self._result else []
