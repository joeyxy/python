

from moduleexception import ModuleException, ProbeException, ProbeSucceed, InitException
from core.argparse import ArgumentParser, StoredNamespace, _StoreTrueAction, _StoreFalseAction, _callable
from types import ListType, StringTypes, DictType
from core.prettytable import PrettyTable
from core.vector import VectorsDict
from os import linesep
import copy


class ModuleBase:

    def __init__(self, modhandler):
        

        self.modhandler = modhandler

        self.name = '.'.join(self.__module__.split('.')[-2:])

        self._init_vectors()
        self._init_args()
        self._init_stored_args()
        
        self._set_vectors()
        self._set_args()
        
        self._init_session_args()
        
        self._init_module()
        
    def _init_vectors(self):
        """This method initialize VectorsDict objects self.vectors and 
        self.support_vectors.
        """
        self.vectors = VectorsDict(self.modhandler)
        self.support_vectors = VectorsDict(self.modhandler)

    def _init_args(self):
        """This method initialize ArgumentParser objects self.argparser.
        """
    
        self.argparser = ArgumentParser(prog=':%s' % self.name, description = self.__doc__, add_help=False)
        
        
    def run(self, arglist = []):
        """Main method called every module execution. It calls:
        
        . Check and set arguments (method _check_args(), do not inherit)
        . Optionally prepares the environment or formats the passed arguments to simplify vector run 
           (method _prepare(), inherition is optional)
        . Runs vectors and saves results  (method _probe(), inherition is mandatory)
        . Optionally verifies probe execution (method _verify(), inherition is optional)
        . Stringify self._result (method stringify_result(), inherition is optional)
        
        """
        
        self._result = ''
        self._output = ''

        try:
            self._check_args(arglist)
            self._prepare()
            self._probe()
            self._verify()
        except ProbeException as e:
            self.mprint('[!] Error: %s' % (e.error), 2, e.module) 
        except ProbeSucceed as e:
            self._stringify_result()
        except InitException, e:
            raise
        except ModuleException, e:
            module = self.name
            if e.module:
                module = e.module
            self.mprint('[!] Error: %s' % (e.error), 2, module) 
        else:
            self._stringify_result()
            
        
        return self._result, self._output

    def mprint(self, msg, msg_class = 3, module_name = None):
        """This method prints formatted warning messages.
        """
        
        if not self.modhandler.verbosity or msg_class <= self.modhandler.verbosity[-1]:
            if module_name == None:
                module_str = '[%s] ' % self.name
            elif module_name == '':
                module_str = ''
            else:
                module_str = '[%s] ' % module_name
                
            print module_str + str(msg)
        
            self.modhandler._last_warns += str(msg) + linesep
            
    def _init_stored_args(self):
        self.stored_args_namespace = StoredNamespace()
        
    def _init_session_args(self):
        
        # Get arguments from session, casting it if needed
        session_args = self.modhandler.sessions.get_session().get(self.name,{})
        self.stored_args_namespace.update(session_args)

    
    def _check_args(self, submitted_args):
        """This method parse and merge new arguments with stored arguments (assigned with :set)
        """
        namespace = copy.copy(self.stored_args_namespace)
        namespace.stored = False
        
        parsed_namespace = self.argparser.parse_args(submitted_args, namespace)
        self.args = vars(parsed_namespace)
        

    def _stringify_result(self):
        """This method try an automatic transformation from self._result object to self._output
        string. Variables self._result and self._output always contains last run results.
        """
        
        
        # Empty outputs. False is probably a good output value 
        if self._result != False and not self._result:
            self._output = ''
        # List outputs.
        elif isinstance(self._result, ListType):
            
            if len(self._result) > 0:
                
                columns_num = 1
                if isinstance(self._result[0], ListType):
                    columns_num = len(self._result[0])
                
                table = PrettyTable(['']*(columns_num))
                table.align = 'l'
                table.header = False
                
                for row in self._result:
                    if isinstance(row, ListType):
                        table.add_row(row)
                    else:
                        table.add_row([ row ])
            
                self._output = table.get_string()
                
        # Dict outputs are display as tables
        elif isinstance(self._result, DictType) and self._result:

            # Populate the rows
            randomitem = next(self._result.itervalues())
            if isinstance(randomitem, ListType):
                table = PrettyTable(['']*(len(randomitem)+1))
                table.align = 'l'
                table.header = False
                
                for field in self._result:
                    table.add_row([field] + self._result[field])
                
            else:
                table = PrettyTable(['']*2)
                table.align = 'l'
                table.header = False
                
                for field in self._result:
                    table.add_row([field, str(self._result[field])])
                

            self._output = table.get_string()
        # Else, try to stringify
        else:
            self._output = str(self._result)
        
        
    def store_args(self, submitted_args):
        
        # With no arguments, reset stored variables 
        if not submitted_args:
            self._init_stored_args()
            
        # Else, store them
        else:
            self.stored_args_namespace = self.argparser.parse_args(submitted_args, self.stored_args_namespace)
        
        
    def format_help(self, help = True, stored_args=True,  name = True, descr=True, usage=True, padding = 0):
        
        help_output = ''

        if help:
            help_output += '%s\n' % self.argparser.format_help()
        else:
            
            if name:
                help_output += '[%s]' % self.name
                
            if descr:
                if name: help_output += ' '
                help_output += '%s\n' %self.argparser.description
            
            if usage:
                help_output += '%s\n' % self.argparser.format_usage() 
    
        stored_args_help = self.format_stored_args()
        if stored_args and stored_args_help:
            help_output += 'stored arguments: %s\n' % stored_args_help.replace('\n', '\n' + ' '*(18))
            
        help_output = ' '*padding + help_output.replace('\n', '\n' + ' '*(padding)).rstrip(' ') 
            
        return help_output
        
                
    def format_stored_args(self):
    
        stringified_stored_args = ''
        
        for index, argument in enumerate(action.dest for action in self.argparser._actions if action.dest != 'help' ):
            value = self.stored_args_namespace[argument] if (argument in self.stored_args_namespace and self.stored_args_namespace[argument] != None) else ''
            stringified_stored_args += '%s=\'%s\' ' % (argument, value)
            
            if index+1 % 4 == 0:
                stringified_stored_args += '\n'
            
        return stringified_stored_args
        
    