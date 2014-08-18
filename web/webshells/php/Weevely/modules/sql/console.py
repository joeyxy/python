from core.module import Module
from core.moduleexception import ModuleException, ProbeException
from core.argparse import ArgumentParser, StoredNamespace
import re

WARN_NO_DATA = 'No data returned'
WARN_CHECK_CRED = 'check credentials and dbms availability'

class Console(Module):
    '''Run SQL console or execute single queries'''
    
    def _set_vectors(self):

        self.support_vectors.add_vector('mysql', 'shell.php', ["""if(mysql_connect("$host","$user","$pass")){$r=mysql_query("$query");if($r){while($c=mysql_fetch_row($r)){foreach($c as $key=>$value){echo $value."\x00";}echo "\n";}};mysql_close();}""" ])
        self.support_vectors.add_vector('mysql_fallback', 'shell.php', [ """$r=mysql_query("$query");if($r){while($c=mysql_fetch_row($r)){foreach($c as $key=>$value){echo $value."\x00";}echo "\n";}};mysql_close();"""]),
        self.support_vectors.add_vector('pg', 'shell.php', ["""if(pg_connect("host=$host user=$user password=$pass")){$r=pg_query("$query");if($r){while($c=pg_fetch_row($r)){foreach($c as $key=>$value){echo $value."\x00";}echo "\n";}};pg_close();}""" ]),
        self.support_vectors.add_vector('pg_fallback', 'shell.php', ["""$r=pg_query("$query");if($r){while($c=pg_fetch_row($r)){foreach($c as $key=>$value){echo $value."\x00";} echo "\n";}};pg_close();"""])

    def _set_args(self):
        self.argparser.add_argument('-user', help='SQL username')
        self.argparser.add_argument('-pass', help='SQL password')
        self.argparser.add_argument('-host', help='DBMS host or host:port', default='127.0.0.1')
        self.argparser.add_argument('-dbms', help='DBMS', choices = ['mysql', 'postgres'], default='mysql')
        self.argparser.add_argument('-query', help='Execute single query')

    def _init_stored_args(self):
        self.stored_args_namespace = StoredNamespace()
        self.stored_args_namespace['vector'] = ''
        self.stored_args_namespace['prompt'] = 'SQL> '
        


    def _prepare(self):

        self.args['vector'] = 'pg' if self.args['dbms'] == 'postgres' else 'mysql'
        if not self.args['user'] or not self.args['pass']:
            self.args['vector'] += '_fallback'
            
        

    def _probe(self):


        if not self.args['query']:
            
            self._check_credentials()
            
            while True:
                self._result = None
                self._output = ''
                
                query  = raw_input( self.stored_args_namespace['prompt'] ).strip()
                
                if not query:
                    continue
                if query == 'quit':
                    break
                
                self._result = self._query(query)
                
                if self._result == None:
                    self.mprint('%s %s' % (WARN_NO_DATA, WARN_CHECK_CRED))
                elif not self._result:
                    self.mprint(WARN_NO_DATA)
                else:   
                    self._stringify_result()
                    
                print self._output
                    
                
        else:
            self._result = self._query(self.args['query'])

            if self._result == None:
                self.mprint('%s, %s.' % (WARN_NO_DATA, WARN_CHECK_CRED))
                
    def _query(self, query):

        result = self.support_vectors.get(self.args['vector']).execute({ 'host' : self.args['host'], 'user' : self.args['user'], 'pass' : self.args['pass'], 'query' : query })
   
        if result:
            return [ line.split('\x00') for line in result[:-1].replace('\x00\n', '\n').split('\n') ]   


    def _check_credentials(self):

        get_current_user = 'SELECT USER;' if self.args['vector']== 'postgres' else 'SELECT USER();'
        
        user = self.support_vectors.get(self.args['dbms']).execute({ 'host' : self.args['host'], 'user' : self.args['user'], 'pass' : self.args['pass'], 'query' : get_current_user })
        
        if user:
            user = user[:-1]
            self.stored_args_namespace['vector'] = self.args['vector']
            self.stored_args_namespace['prompt'] = '%s SQL> ' % user
        else:
            raise ProbeException(self.name, "%s of %s " % (WARN_CHECK_CRED, self.args['host']) )
