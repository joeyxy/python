<?php
ob_start();
session_start();
$serverName     = ''; //sqlserver
// 数据库服务器地址
$uid            = '';
// 数据库用户名
$pwd            = '';
// 数据库密码

$connectionInfo = array("UID"=>$uid, "PWD"=>$pwd, "Database"=>"new");

$conn = sqlsrv_connect( $serverName, $connectionInfo);
if (is_file($_SERVER['DOCUMENT_ROOT'] . '/360safe/360webscan.php')) {
    require_once($_SERVER['DOCUMENT_ROOT'] . '/360safe/360webscan.php');
} // 注意文件路径
if( $conn == false)

{

echo "连接失败！";

// die( print_r( sqlsrv_errors(), true));

}
$host     = ''; //数据库服务器
$user     = ''; //数据库用户名
$password = ''; //数据库密码
$database = ''; //数据库名
$conn1 = @mysql_connect($host, $user, $password) or die('数据库连接失败！');
@mysql_select_db($database) or die('没有找到数据库！');
mysql_query("set names utf8");
?>