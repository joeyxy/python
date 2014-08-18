<?php

//session_start();
//首先，建议上面这句话放在最最顶部，切< ?php前面决不允许出现任何空格以及换行!!，为了避免出现空格或换行，建议最顶部增加ob_start();写完整就是下面两行

ob_start();
session_start();

$session=$_SESSION['user_auth'];
echo "<meta http-equiv='Content-Type' content='text/html; charset=UTF-8' />";

if (is_file($_SERVER['DOCUMENT_ROOT'] . '/360safe/360webscan.php')) {
    require_once($_SERVER['DOCUMENT_ROOT'] . '/360safe/360webscan.php');
} // 注意文件路径
include_once('/html/top.php');
include('function.php');
//数据库链接文件
$host     = ''; //数据库服务器
$user     = ''; //数据库用户名
$password = ''; //数据库密码
$database = ''; //数据库名
$conn = @mysql_connect($host, $user, $password) or die('数据库连接失败！');
@mysql_select_db($database) or die('没有找到数据库！');
mysql_query("set names utf8");

