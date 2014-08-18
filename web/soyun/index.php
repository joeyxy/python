<?php


include('sgk.php');
include('function.php');
?>
<script>
    function buy(){
        if (confirm("是否购买内部数据(1金币)！")) {
            return true;
        }else{
            return false;
        }
    }

</script>
<?php

if (empty($_GET["keyword"])){
    echo '
    <!DOCTYPE html>
    <html>
    <head>
	
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>Soyun-谁泄露了你的信息？</title>
        <meta name="description" content="搜云,社工库在线查询，全国最大最全的信息泄露查询平台！">
		<meta name="keywords" content="社工库在线查询,社工库论坛,社工库查询"/>
        <meta name="viewport" content="width=device-width">

        <link href="/css/css.css" rel="stylesheet" type="text/css">
        
        <style>
            body {
                padding-top: 60px;
                padding-bottom: 40px;
            }
        </style>
        <link rel="stylesheet" href="/css/bootstrap-responsive.min.css">
        <link rel="stylesheet" href="/css/font-awesome.css">
        <link rel="stylesheet" href="/css/launch.css">

    </head>
    <body>
        ';
        include_once('/html/top.php');
        echo '
        <div class="container">
            <header class="launch-head">
                <h1>SoYun</h1>
                <h2>你的信息可能被某个网站泄露!</h2> 
            </header>

            <section id="signup-sect"> 
                <p>来看看，谁背叛了你的信息？</p> 
                <p>QQ群:248980196</p>
                <div class="flex-container">
                    <form class="fancy-form" >
                        <div class="controls controls-row hide-me">

                          <input  id="input-email" class="span5" type="text" name="keyword" placeholder="关键字">
                          <button id="submit-email" class="span2 btn btn-fancy" type="submit">查询</button>
                      </div>                        
                      <div id="resp" class="center-child"></div> <!-- Response message -->
                      <div class="row">
                          <div class="col-lg-6">
                            <div class="input-group">
                              <span class="input-group-addon">
                                <input type="checkbox" name="auto">智能模式
                            </span>

                            <!--<input type="text" class="form-control" name="email" placeholder="Your Email">-->
                        </div><!-- /input-group -->
                    </div><!-- /.col-lg-6 -->
                </form>
                <div class="well" id="error"></div> <!-- Error message -->

            </div>
        </section>

        <section id="info" class="row">
            <div class="span4">
                <h3>数据从哪来？</h3>
                <p>所有的数据来自互联网的收集，与本站无关！</p>
            </div>
            <div class="span4">
                <h3>网站储存了数据？</h3>
                <p>不一定，一些数据仅仅是泄露的账号或者邮箱，但偶尔会出现密码，如果您查询到了您的账号，请尽快修改密码！</p>
            </div>
            <div class="span4">
                <h3>为什么查询到的密码错误?</h3>
                <p>本站不敢保证所有的信息正确，有些可能是用户的历史密码！</p>
            </div>
        </section>

        <footer id="pagefooter">
            <p class="pull-right">Email:admin@soyun.org<br>©2014 soyun 所有</p>

        </footer>
    </div> <!-- /container -->
    <script type="text/javascript" src="http://tajs.qq.com/stats?sId=34818869" charset="UTF-8"></script>
</body>
</html>';
}
else
{
    echo '
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>Soyun-谁泄露了你的信息？</title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width">

        <link href="/css/css.css" rel="stylesheet" type="text/css">
        
        <style>
            body {
                padding-top: 60px;
                padding-bottom: 40px;
            }
        </style>
        <link rel="stylesheet" href="/css/bootstrap-responsive.min.css">
        <link rel="stylesheet" href="/css/font-awesome.css">
        <link rel="stylesheet" href="/css/launch.css">

    </head>
    <body>
        ';
        include_once('/html/top.php');
        echo '
        <div class="container">
            <header class="launch-head">
                <h1>SoYun</h1>
            </header>
            ';
            echo '
            <section id="signup-sect"> 
                <div class="flex-container">
                    <form class="fancy-form" >
                        <div class="controls controls-row hide-me">

                          <input  id="input-email" class="span5" type="text" name="keyword" placeholder="关键字">
                          <button id="submit-email" class="span2 btn btn-fancy" type="submit">查询</button>
                      </div>                        

                  </form>

              </section>
          </div> <!-- /container -->';
          echo ' <div class="container">';
          // if (!empty($_SESSION['username']))
          // {
           $search=addslashes($_GET['keyword']);
        $ip=getip();
		 $time = date('Y-m-d H:i:s', time());
        // echo $ip;
        $a="INSERT INTO bbs.`log`(`user`,`ip`,`msg`,`time`) VALUES ('$use','$ip','Search,IP:" . $search . "','$time')";
        // echo $a;
        mysql_query($a,$conn1);
		// echo $a;
           // $sql="select * from main where username='".$session['username']."'";
           // $a=mysql_query($sql,$conn1);
           // if (mysql_affected_rows() <> 0)
           // {
            // $vip='open';
        // }
        // elseif ($_GET['buy']=='yes') {
            // if($session['credit'] >= 1) {
                // $sql="update `talk_user` set credit=credit-1 where username='".$session['username']."'";
                // mysql_query($sql);
                // if (mysql_affected_rows() <> 0){
                    // $_SESSION['credit']=$_SESSION['credit']-1;
                    // $sql="select `credit` from `talk_user` where username='".$session['username']."' and credit > 0";
                    // mysql_query($sql);
                    // if (mysql_affected_rows() <> 0)
                    // {
                        // $vip='open';
                    // }
                    // else{
                        // echo "没有足够的积分！";
                    // }
                // }
            // }
        // }
        // elseif ($session['credit'] >= 1) {
            // echo "此结果内部社工库已经获取，是否购买<a href='http://www.soyun.org/?keyword=".$search."&buy=yes'>Buy</a>";
    // # code...
        // }
        echo '<div class="hero-unit">';

        $url="http://www.soyun.org/svip_so.php?so=".$search."&vip=".$vip ;  
        $cu = curl_init();
        curl_setopt($cu, CURLOPT_URL, $url);
        curl_setopt($cu, CURLOPT_RETURNTRANSFER, 1);
       echo  curl_exec($cu);
        curl_close($cu);
		// $body=file_get_contents($url);
		// echo $body;
        echo '</div></div>
        <script type="text/javascript" src="http://tajs.qq.com/stats?sId=34818869" charset="UTF-8"></script>
    </body>
    </html>';
// }
// else{
    // echo "<script>alert('请登陆账号！')</script>";
// }
}