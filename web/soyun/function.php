<?php
//邀请码
mt_srand((double) microtime() * 1000000);
function gen_random_password($password_length = 30, $generated_password = "") //password_length 随机密码长度，默认10位   
{
    $valid_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    $chars_length     = strlen($valid_characters) - 1;
    for ($i = $password_length; $i--; ) {
        //$generated_password .= $valid_characters[mt_rand(0, $chars_length)];   
        
        $generated_password .= substr($valid_characters, (mt_rand() % (strlen($valid_characters))), 1);
    }
    return $generated_password;
}
//邀请码生成结束
//中文字符截断
    function session($name,$value='') {
        $prefix   =  C('SESSION_PREFIX');
        if(is_array($name)) { // session初始化 在session_start 之前调用
            if(isset($name['prefix'])) C('SESSION_PREFIX',$name['prefix']);
            if(isset($_REQUEST[C('VAR_SESSION_ID')])){
                session_id($_REQUEST[C('VAR_SESSION_ID')]);
            }elseif(isset($name['id'])) {
                session_id($name['id']);
            }
            ini_set('session.auto_start', 0);
            if(isset($name['name'])) session_name($name['name']);
            if(isset($name['path'])) session_save_path($name['path']);
            if(isset($name['domain'])) ini_set('session.cookie_domain', $name['domain']);
            if(isset($name['expire'])) ini_set('session.gc_maxlifetime', $name['expire']);
            if(isset($name['use_trans_sid'])) ini_set('session.use_trans_sid', $name['use_trans_sid']?1:0);
            if(isset($name['use_cookies'])) ini_set('session.use_cookies', $name['use_cookies']?1:0);
            if(isset($name['type'])) C('SESSION_TYPE',$name['type']);
            if(C('SESSION_TYPE')) { // 读取session驱动
                $class = 'Session'. ucwords(strtolower(C('SESSION_TYPE')));
                // 检查驱动类
                if(require_cache(EXTEND_PATH.'Driver/Session/'.$class.'.class.php')) {
                    $hander = new $class();
                    $hander->execute();
                }else {
                    // 类没有定义
                    throw_exception(L('_CLASS_NOT_EXIST_').': ' . $class);
                }
            }
            // 启动session
            if(C('SESSION_AUTO_START'))  session_start();
        }elseif('' === $value){ 
            if(0===strpos($name,'[')) { // session 操作
                if('[pause]'==$name){ // 暂停session
                    session_write_close();
                }elseif('[start]'==$name){ // 启动session
                    session_start();
                }elseif('[destroy]'==$name){ // 销毁session
                    $_SESSION =  array();
                    session_unset();
                    session_destroy();
                }elseif('[regenerate]'==$name){ // 重新生成id
                    session_regenerate_id();
                }
            }elseif(0===strpos($name,'?')){ // 检查session
                $name   =  substr($name,1);
                if($prefix) {
                    return isset($_SESSION[$prefix][$name]);
                }else{
                    return isset($_SESSION[$name]);
                }
            }elseif(is_null($name)){ // 清空session
                if($prefix) {
                    unset($_SESSION[$prefix]);
                }else{
                    $_SESSION = array();
                }
            }elseif($prefix){ // 获取session
                return $_SESSION[$prefix][$name];
            }else{
                return $_SESSION[$name];
            }
        }elseif(is_null($value)){ // 删除session
            if($prefix){
                unset($_SESSION[$prefix][$name]);
            }else{
                unset($_SESSION[$name]);
            }
        }else{ // 设置session
            if($prefix){
                if (!is_array($_SESSION[$prefix])) {
                    $_SESSION[$prefix] = array();
                }
                $_SESSION[$prefix][$name]   =  $value;
            }else{
                $_SESSION[$name]  =  $value;
            }
        }
    }
	function data_auth_sign( $data ) {
    if ( !is_array( $data ) ) {
        $data = (array)$data;
    }
    ksort( $data );
    $code = http_build_query( $data );
    $sign = sha1( $code );
    return $sign;
}
function mysubstr($str, $start, $len)
{
    $tmpstr = "";
    $strlen = $start + $len;
    for ($i = 0; $i < $strlen; $i++) {
        if (ord(substr($str, $i, 1)) > 0xa0) {
            $tmpstr .= substr($str, $i, 2);
            $i++;
        } else
            $tmpstr .= substr($str, $i, 1);
    }
    return $tmpstr;
}
//获取IP
function GetIP()
{
    if (getenv("HTTP_CLIENT_IP") && strcasecmp(getenv("HTTP_CLIENT_IP"), "unknown"))
        $ip = getenv("HTTP_CLIENT_IP");
    else if (getenv("HTTP_X_FORWARDED_FOR") && strcasecmp(getenv("HTTP_X_FORWARDED_FOR"), "unknown"))
        $ip = getenv("HTTP_X_FORWARDED_FOR");
    else if (getenv("REMOTE_ADDR") && strcasecmp(getenv("REMOTE_ADDR"), "unknown"))
        $ip = getenv("REMOTE_ADDR");
    else if (isset($_SERVER['REMOTE_ADDR']) && $_SERVER['REMOTE_ADDR'] && strcasecmp($_SERVER['REMOTE_ADDR'], "unknown"))
        $ip = $_SERVER['REMOTE_ADDR'];
    else
        $ip = "unknown";
 

        $oip = explode(".",$ip);
        for($i=0;$i<count($oip);$i++)
       {
              if($ip[$i]>255){
               return (0);
               }
        }
        if (ereg("^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$",$oip));
		{
		return $ip;
		}

	

}

//中文字符截断结束
//这里不建议使用? >结尾了！因为你的? >后面可能存在空格或换行！！！

function array_zhuan($array) //Array数组gbk转utf8
{
    $serial_str = iconv('gbk', 'utf-8', serialize($array));
    $serial_str = preg_replace('!s:(\d+):"(.*?)";!se', "'s:'.strlen('$2').':\"$2\";'", $serial_str);
    $serial_str = str_replace("\r", "", $serial_str);
    return unserialize($serial_str);
}

function get($url)
{
    $rand = rand(1, 255);
    $ip   = $rand . "." . $rand . "." . $rand . "." . $rand;
    $url  = $url;
    $ch   = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_REFERER, $url); //构造来路
    curl_setopt($ch, CURLOPT_USERAGENT, "Baiduspider+(+http://www.baidu.com/search/spider.htm)");
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
        "Client_Ip: " . $ip . "",
        "Real_ip: " . $ip . "",
        "X_FORWARD_FOR:" . $ip . "",
        "X-forwarded-for: " . $ip . "",
        "PROXY_USER: " . $ip . ""
    ));
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    $data = curl_exec($ch);
    curl_close($ch);
    return $data;
}

/*
 * post 方式模拟请求指定地址
 * @param  string url	请求的指定地址
 * @param  array  params 请求所带的
 * #patam  string cookie cookie存放地址
 * @return string curl_exec()获取的信息
 * @author andy
 **/
function post($url, $params, $cookie)
{
    $ip   = "220.181.24.100";
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_HEADER, 0);
    // 对认证证书来源的检查，0表示阻止对证书的合法性的检查。
    curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
    // 从证书中检查SSL加密算法是否存在
    curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, 1);
    //模拟用户使用的浏览器，在HTTP请求中包含一个”user-agent”头的字符串。
    curl_setopt($curl, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36");
    //发送一个常规的POST请求，类型为：application/x-www-form-urlencoded，就像表单提交的一样。
    curl_setopt($curl, CURLOPT_POST, 1);
    // 将 curl_exec()获取的信息以文件流的形式返回，而不是直接输出。
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
    // 使用自动跳转
    curl_setopt($curl, CURLOPT_FOLLOWLOCATION, 1);
    curl_setopt($curl, CURLOPT_REFERER, $url); //构造来路
    curl_setopt($curl, CURLOPT_AUTOREFERER, 1);
    curl_setopt($curl, CURLOPT_TIMEOUT, 10);
    curl_setopt($curl, CURLOPT_HTTPHEADER, array(
        "Client_Ip: " . $ip . "",
        "Real_ip: " . $ip . "",
        "X_FORWARD_FOR:" . $ip . "",
        "X-forwarded-for: " . $ip . "",
        "PROXY_USER: " . $ip . ""
    ));
    curl_setopt($curl, CURLOPT_COOKIEJAR, $cookie);
    // 全部数据使用HTTP协议中的"POST"操作来发送。要发送文件，
    // 在文件名前面加上@前缀并使用完整路径。这个参数可以通过urlencoded后的字符串
    // 类似'para1=val1?2=val2&...'或使用一个以字段名为键值，字段数据为值的数组
    // 如果value是一个数组，Content-Type头将会被设置成multipart/form-data。
    curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($params));
    $result = curl_exec($curl);
    curl_close($curl);
    return $result;
}

function md5online($md5){//MD5online调用
	  
	  
	  $ip="8.35.201.51";
	  
$ch = curl_init();
$post_data = array (  
     "md5" => $md5,
	 "search" => "0",
	 "action" => "decrypt",
	 "a" => "54217635"
); 
$url =  "http://www.md5online.org/md5-decrypt.html";
curl_setopt($ch, CURLOPT_URL,$url);
curl_setopt($ch, CURLOPT_POST, 1);  
curl_setopt($ch, CURLOPT_POSTFIELDS,http_build_query($post_data));
curl_setopt($ch, CURLOPT_REFERER, "http://www.md5online.org/md5-decrypt.html");   //构造来路
curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36");
curl_setopt($ch, CURLOPT_HTTPHEADER,array("Client_Ip: ".$ip."", "Real_ip: ".$ip."", "X_FORWARD_FOR:".$ip."", "X-forwarded-for: ".$ip."", "PROXY_USER: ".$ip.""));
curl_setopt($ch, CURLOPT_TIMEOUT, 10);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
$hash = curl_exec($ch);
curl_close($ch);
  preg_match_all('/<b>(.*)<\/b>/',$hash,$hashdata);

  
$hashdata=trim($hashdata);

  
 if (empty($hashdata)){
              return false;
			  exit;
 }
 if (strstr($hashdata, "No result found in our database")) {
             return false;

exit;
 }
 if (strstr($hashdata, "502 Bad Gateway")) {
             return false;
			 exit;
    }
		 if (strstr($hashdata, "504 Gateway Time")) {
             return false;
			 exit;
    }

  preg_match_all('/<b>(.*)<\/b>/',$hash,$hashdata);
   if (empty($hashdata)){
              return false;
			  exit;
 }
	   $hashdata=$hashdata[0] ;
	   $hashdata=$hashdata[0];
		return $hashdata;
          //    return false;
	
	  }
	  
	    function somd5($txt)//SOMD5
    {
			$key = 'S@!@O!M@@!D!!@!@5C@@!O!M';
		$md5=$txt;
        $chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.";
        $ikey ="-x6g6ZWm2G9g_vr0Bo.pOq3kRIxsZ6rm";
        $nh1 = rand(0,64);
        $nh2 = rand(0,64);
        $nh3 = rand(0,64);
        $ch1 = $chars{$nh1};
        $ch2 = $chars{$nh2};
        $ch3 = $chars{$nh3};
        $nhnum = $nh1 + $nh2 + $nh3;
        $knum = 0;$i = 0;
        while(isset($key{$i})) $knum +=ord($key{$i++});
        $mdKey = substr(md5(md5(md5($key.$ch1).$ch2.$ikey).$ch3),$nhnum%8,$knum%8 + 16);
        $txt = base64_encode($txt);
        $txt = str_replace(array('+','/','='),array('-','_','.'),$txt);
        $tmp = '';
        $j=0;$k = 0;
        $tlen = strlen($txt);
        $klen = strlen($mdKey);
        for ($i=0; $i<$tlen; $i++) {
            $k = $k == $klen ? 0 : $k;
            $j = ($nhnum+strpos($chars,$txt{$i})+ord($mdKey{$k++}))%64;
            $tmp .= $chars{$j};
        }
        $tmplen = strlen($tmp);
        $tmp = substr_replace($tmp,$ch3,$nh2 % ++$tmplen,0);
        $tmp = substr_replace($tmp,$ch2,$nh1 % ++$tmplen,0);
        $tmp = substr_replace($tmp,$ch1,$knum % ++$tmplen,0);

		$ch = curl_init();
		$post_data = array ( 
		"isajax" => "PpFP6THspF7eo4TGJ3nCnF1",
		"md5" => $md5
		); 
$url =  "http://aiisoo.com/somd5-index-md5.html";
curl_setopt($ch, CURLOPT_URL,$url);
curl_setopt($ch, CURLOPT_POST, 1);  
curl_setopt($ch, CURLOPT_POSTFIELDS,http_build_query($post_data));
curl_setopt($ch, CURLOPT_REFERER, "http://aiisoo.com/index.php");   //鏋勯€犳潵璺?
curl_setopt($ch, CURLOPT_TIMEOUT, 10);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false); 
curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0");
$body = curl_exec($ch);
curl_close($ch);
preg_match_all('{<h1.*>(.*)</h1>}',$body,$array);
//$array=strip_tags($array);
$array=$array[1];
$array=$array[0];
return strip_tags($array);
		}
		
	
function jiami_main($input)//超级加密函数MAIN
    {
    	$key="!@#<SD)SCBUkawkhdjawhd(!K!)SSK!@9";
        $input = str_replace("n", "", $input);
        $input = str_replace("t", "", $input);
        $input = str_replace("r", "", $input);
        $key = substr(md5($key), 0, 24);
        $td = mcrypt_module_open('tripledes', '', 'ecb', '');
        $iv = mcrypt_create_iv(mcrypt_enc_get_iv_size($td), MCRYPT_RAND);
        mcrypt_generic_init($td, $key, $iv);
        $encrypted_data = mcrypt_generic($td, $input);
        mcrypt_generic_deinit($td);
        mcrypt_module_close($td);
        return trim(md5(sha1(md5(chop(base64_encode($encrypted_data))))));
    }
    	function jiami($txt) //超级加密函数
    	{
    		$jiami=jiami_main(md5($txt));
    		return $jiami;
    	}
    	
    	
    	/**
* 获取 IP  地理位置
* 淘宝IP接口
* @Return: array
*/
function getCity($ip)
{
$url="http://ip.taobao.com/service/getIpInfo.php?ip=".$ip;
$ip=json_decode(file_get_contents($url));
if((string)$ip->code=='1'){
return false;
}
$data = (array)$ip->data;
return $data;
}
function email_main($email){
$b=explode("@",$email);
$b=$b[0];
return $b;
}
function mail_send($search,$rulues,$email){
require("class.phpmailer.php"); //下载的文件必须放在该文件所在目录
$mail = new PHPMailer(); //建立邮件发送类
$address ="617925118@qq.com";
$mail->IsSMTP(); // 使用SMTP方式发送
$mail->Host = "smtp.exmail.qq.com"; // 您的企业邮局域名
$mail->SMTPAuth = true; // 启用SMTP验证功能
$mail->Username = "system@sojb.pw"; // 邮局用户名(请填写完整的email地址)
$mail->Password = "jUA9vUX72nuH"; // 邮局密码
$mail->Port=25;
$mail->From = "system@sojb.pw"; //邮件发送者email地址
$mail->FromName = "SoYun";
$mail->AddAddress("$email", "a");//收件人地址，可以替换成任何想要接收邮件的email信箱,格式是AddAddress("收件人email","收件人姓名")
//$mail->AddReplyTo("", "");

//$mail->AddAttachment("/var/tmp/file.tar.gz"); // 添加附件
$mail->IsHTML(true); // set email format to HTML //是否使用HTML格式

$mail->Subject = "search result,about ".$search.""; //邮件标题
$mail->Body = "This is your the query result to the SoYun, key word:".$search."<br><br>".$rulues."";
//$mail->AltBody = "This is the body in plain text for non-HTML mail clients"; //附加信息，可以省略

if(!$mail->Send())
{
echo "Error. <p>";
echo "error: " . $mail->ErrorInfo;
exit;
}
echo "<script>alert('We have the query results sent to your email!');</script>";
}

function search_auto_md5($md5){
$str=strlen($md5);
if ($str == 16) {
$yes=somd5($md5);
if ($yes==""){
return $md5;
}
else{
return $yes."{<font color='red'>MD5自动解密完成</font>}";
 }
 }
else if ($str==32){
 $yes=somd5($md5);
 if ($yes==""){
return $md5;
}
else{
 return $yes."{<font color='green'>MD5自动解密完成</font>}";
 }
 }
 
else if ($str != 32){
 return $md5;
 }

 
}
function encrypt($data, $key)
{
	$key	=	md5($key);
    $x		=	0;
    $len	=	strlen($data);
    $l		=	strlen($key);
    for ($i = 0; $i < $len; $i++)
    {
        if ($x == $l) 
        {
        	$x = 0;
        }
        $char .= $key{$x};
        $x++;
    }
    for ($i = 0; $i < $len; $i++)
    {
        $str .= chr(ord($data{$i}) + (ord($char{$i})) % 256);
    }
    return base64_encode($str);
}

?>