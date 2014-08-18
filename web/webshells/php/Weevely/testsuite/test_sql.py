from baseclasses import SimpleTestCase
from test import conf
from tempfile import NamedTemporaryFile
import random, string
import sys, os
sys.path.append(os.path.abspath('..'))
import modules
from unittest import skipIf

class MySql(SimpleTestCase):
    
    @skipIf(conf['test_only_dbms'] == 'postgres', "Skipping mysql tests")
    def test_query(self):

        
        user = conf['mysql_sql_user']
        pwd = conf['mysql_sql_pwd']
        
        self.assertEqual(self._res(':sql.console -user %s -pass %s -query "SELECT USER();"' % ( user, pwd ) ), [['%s@localhost' % user ]])

        self.assertEqual(self._res(':sql.console -user %s -pass %s -query "SELECT USER();"' % ( user, pwd ) ), [['%s@localhost' % user ]])
        

        self._res(':sql.console -user %s -pass %s -query "create database asd;"' % ( user, pwd ))
        
        databases = self._res(':sql.console -user %s -pass %s -query "show databases;" ' % ( user, pwd ))          
        self.assertTrue(['asd'] in databases and ['information_schema'] in databases )
      
        self._res(':sql.console -user %s -pass %s -query "drop database asd;" ' % ( user, pwd ))
                      

    @skipIf(conf['test_only_dbms'] == 'postgres' or not conf['mysql_sql_default_user'], "Skipping mysql tests")
    def test_query_fallback_user(self):
        
        default_user = conf['mysql_sql_default_user']
        user = conf['mysql_sql_user']
        pwd = conf['mysql_sql_pwd']
        
        self.assertEqual(self._res(':sql.console -query "SELECT USER();"'), [['%s@localhost' % default_user ]])
        self.assertEqual(self._res(':sql.console -host notreachable -query "SELECT USER();"' ), [['%s@localhost' % default_user ]])
       
        

    @skipIf(conf['test_only_dbms'] == 'postgres', "Skipping mysql tests")
    def test_dump(self):

        user = conf['mysql_sql_user']
        pwd = conf['mysql_sql_pwd']
        
        
        # Standard test
        self.assertRegexpMatches(self._res(':sql.dump -user %s -pass %s information_schema' % ( user, pwd ) ), "-- Dumping data for table `COLUMNS`")
        self.assertRegexpMatches(self._warn(':sql.dump -user %s -pass wrongpass information_schema' % ( user ) ), modules.sql.dump.WARN_DUMP_INCOMPLETE)
             
        # table
        self.assertRegexpMatches(self._res(':sql.dump -user %s -pass %s information_schema -table TABLES' % ( user, pwd ) ), "-- Dumping data for table `TABLES`")
         
  
        self.assertRegexpMatches(self._res(':sql.dump -user %s -pass %s information_schema -vector mysqlphpdump -table TABLES' % ( user, pwd ) ), "-- Dumping data for table `TABLES`")
        self.assertRegexpMatches(self._warn(':sql.dump -user %s -pass wrongpass information_schema  -vector mysqlphpdump -table TABLES' % ( user ) ), modules.sql.dump.WARN_DUMP_INCOMPLETE)

        # lpath
        self.assertRegexpMatches(self._warn(':sql.dump -user %s -pass %s information_schema -table TABLES -ldump /wrongpath' % ( user, pwd ) ), modules.sql.dump.WARN_DUMP_ERR_SAVING)

        # host
        self.assertRegexpMatches(self._warn(':sql.dump -user %s -pass %s information_schema -table TABLES -host wronghost' % ( user, pwd ) ), modules.sql.dump.WARN_DUMP_INCOMPLETE)



    @skipIf(conf['test_only_dbms'] == 'postgres', "Skipping mysql tests")
    @skipIf(not conf['shell_sh'], "Skipping shell.sh dependent tests")
    def test_dump(self):

        user = conf['mysql_sql_user']
        pwd = conf['mysql_sql_pwd']

        # vectors
        self.assertRegexpMatches(self._res(':sql.dump -user %s -pass %s information_schema -vector mysqldump -table TABLES' % ( user, pwd ) ), "-- Dumping data for table `TABLES`")
        self.assertRegexpMatches(self._warn(':sql.dump -user %s -pass wrongpass information_schema  -vector mysqldump -table TABLES' % ( user ) ), modules.sql.dump.WARN_DUMP_INCOMPLETE)
                   

class PGSql(SimpleTestCase):
    
    
    @skipIf(conf['test_only_dbms'] == 'mysql', "Skipping postgres tests")
    def test_query(self):
            
        user = conf['pg_sql_user']
        pwd = conf['pg_sql_pwd']

        self.assertEqual(self._res(':sql.console -user %s -pass %s -query "SELECT USER;" -dbms postgres' % ( user, pwd ) ), [[ user ]])
        self.assertRegexpMatches(self._warn(':sql.console -user %s -pass wrongpass -query "SELECT USER();" -dbms postgres' % ( user) ), modules.sql.console.WARN_CHECK_CRED)
    
        self.assertRegexpMatches(self._warn(':sql.console -user %s -pass %s -host notreachable -query "SELECT USER;" -dbms postgres' % ( user, pwd ) ), modules.sql.console.WARN_CHECK_CRED)
        
        self._res(':sql.console -user %s -pass %s -query "create database asd;" -dbms postgres' % ( user, pwd ))
        
        databases = self._res(':sql.console -user %s -pass %s -query "SELECT datname FROM pg_database;" -dbms postgres' % ( user, pwd ))          
        self.assertTrue(['asd'] in databases and ['postgres'] in databases )
      
        self._res(':sql.console -user %s -pass %s -query "drop database asd;" -dbms postgres' % ( user, pwd ))
                  
                  
                      