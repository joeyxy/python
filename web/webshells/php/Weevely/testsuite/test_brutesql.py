from baseclasses import SimpleTestCase
from tempfile import NamedTemporaryFile
import random, string
import sys, os
sys.path.append(os.path.abspath('..'))
import modules
from test import conf

class BruteSQL(SimpleTestCase):
    
    def _generate_wordlist(self, insert_word = ''):
        wordlist = [''.join(random.choice(string.ascii_lowercase) for x in range(random.randint(1,50))) for x in range(random.randint(1,50)) ]
        if insert_word:
            wordlist[random.randint(0,len(wordlist)-1)] = insert_word
        return wordlist
        
    
    def test_brutesql(self):

        for dbms in ['mysql', 'postgres']:

            if conf['test_only_dbms'] and conf['test_only_dbms'] != dbms:
                continue
    
            if dbms == 'mysql':
                user = conf['mysql_sql_user']
                pwd = conf['mysql_sql_pwd']
            else:
                user = conf['pg_sql_user']
                pwd = conf['pg_sql_pwd']
                                
            expected_match = [ user, pwd ]
            
            self.assertEqual(self._res(':bruteforce.sql %s -wordlist "%s" -dbms %s' % (user, str(self._generate_wordlist(pwd)), dbms)), expected_match)
            
            temp_path = NamedTemporaryFile(); 
            temp_path.write('\n'.join(self._generate_wordlist(pwd)))
            temp_path.flush() 
            
            self.assertEqual(self._res(':bruteforce.sql %s -wordfile "%s" -dbms %s' % (user, temp_path.name, dbms)), expected_match)
            self.assertRegexpMatches(self._warn(':bruteforce.sql %s -wordfile "%sunexistant" -dbms %s' % (user, temp_path.name, dbms)), modules.bruteforce.sql.WARN_NO_SUCH_FILE)
            self.assertRegexpMatches(self._warn(':bruteforce.sql %s' % (user)), modules.bruteforce.sql.WARN_NO_WORDLIST)
            
            self.assertEqual(self._res(':bruteforce.sql %s -chunksize 1 -wordlist "%s" -dbms %s' % (user, str(self._generate_wordlist(pwd)), dbms)), expected_match)
            self.assertEqual(self._res(':bruteforce.sql %s -chunksize 100000 -wordlist "%s" -dbms %s' % (user, str(self._generate_wordlist(pwd)), dbms)), expected_match)
            self.assertEqual(self._res(':bruteforce.sql %s -chunksize 0 -wordlist "%s" -dbms %s' % (user, str(self._generate_wordlist(pwd)),dbms)), expected_match)
            
            wordlist = self._generate_wordlist() + [ pwd ]
            self.assertEqual(self._res(':bruteforce.sql %s -wordlist "%s" -dbms %s -startline %i' % (user, str(wordlist), dbms, len(wordlist)-1)), expected_match)
            self.assertRegexpMatches(self._warn(':bruteforce.sql %s -wordlist "%s" -dbms %s -startline %i' % (user, str(wordlist), dbms, len(wordlist)+1)), modules.bruteforce.sql.WARN_STARTLINE)
            
            
            temp_path.close()

    def test_brutesqlusers(self):

        for dbms in ['mysql', 'postgres']:

            if conf['test_only_dbms'] and conf['test_only_dbms'] != dbms:
                continue
    
            if dbms == 'mysql':
                user = conf['mysql_sql_user']
                pwd = conf['mysql_sql_pwd']
            else:
                user = conf['pg_sql_user']
                pwd = conf['pg_sql_pwd']
    
            expected_match = { user : pwd }
            self.assertEqual(self._res(':bruteforce.sqlusers -wordlist "%s" -dbms %s' % ( str(self._generate_wordlist(pwd)), dbms)), expected_match)
            
            temp_path = NamedTemporaryFile(); 
            temp_path.write('\n'.join(self._generate_wordlist(pwd)))
            temp_path.flush() 
            
            self.assertEqual(self._res(':bruteforce.sqlusers -wordfile "%s" -dbms %s' % ( temp_path.name, dbms)), expected_match)
            self.assertRegexpMatches(self._warn(':bruteforce.sqlusers -wordfile "%sunexistant" -dbms %s' % ( temp_path.name, dbms)), modules.bruteforce.sql.WARN_NO_SUCH_FILE)
            self.assertRegexpMatches(self._warn(':bruteforce.sqlusers '), modules.bruteforce.sql.WARN_NO_WORDLIST)
            
            self.assertEqual(self._res(':bruteforce.sqlusers -chunksize 1 -wordlist "%s" -dbms %s' % ( str(self._generate_wordlist(pwd)), dbms)), expected_match)
            self.assertEqual(self._res(':bruteforce.sqlusers -chunksize 100000 -wordlist "%s" -dbms %s' % ( str(self._generate_wordlist(pwd)), dbms)), expected_match)
            self.assertEqual(self._res(':bruteforce.sqlusers -chunksize 0 -wordlist "%s" -dbms %s' % ( str(self._generate_wordlist(pwd)),dbms)), expected_match)
            
            wordlist = self._generate_wordlist() + [ pwd ]
            self.assertEqual(self._res(':bruteforce.sqlusers -wordlist "%s" -dbms %s -startline %i' % ( str(wordlist), dbms, len(wordlist)-1)), expected_match)
            self.assertRegexpMatches(self._warn(':bruteforce.sqlusers  -wordlist "%s" -dbms %s -startline %i' % ( str(wordlist), dbms, len(wordlist)+1)), modules.bruteforce.sql.WARN_STARTLINE)
            
            
            temp_path.close()
            
            