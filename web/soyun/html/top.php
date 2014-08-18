 <?php
ob_start();
session_start();
 ?>
<link type="text/css" rel="stylesheet" href="/css/footer.css">
<link rel="stylesheet" href="/html/bootstrap.min.css">
<script type="text/javascript" src="http://cdn.bootcss.com/jquery/1.10.2/jquery.min.js"></script>
<script type="text/javascript" src="/js/Bootstrap.min.js"></script>
<div class="navbar navbar-fixed-top">
  <div class="navbar-inner">
    <div class="container">
 
      <!-- .btn-navbar is used as the toggle for collapsed navbar content -->
      <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </a>
 
      <!-- Be sure to leave the brand out there if you want it shown -->
      <a class="brand" href="index.php">SoYun</a>
 
      <!-- Everything you want hidden at 940px or less, place within here -->
      <div class="nav-collapse collapse">
 <ul class="nav">
<li ><a href="index.php">主页</a></li>
<li ><a href="http://bbs.soyun.org">社区</a></li>
</ul> 
<ul class="nav pull-right">
<?php
if ($_SESSION['username']=="")
{
echo '
<li><a href="http://bbs.soyun.org/index.php?m=u&c=login">登陆</a></li>
<li><a href="http://bbs.soyun.org/index.php?m=u&c=register">注册</a></li>
';
}
else
{
echo '                    <li class="dropdown" id="fat-menu">
                      <a data-toggle="dropdown" class="dropdown-toggle" role="button" id="drop3" href="#">Info<b class="caret"></b></a>
                      <ul aria-labelledby="drop3" role="menu" class="dropdown-menu">
                        <li role="presentation"><a href="http://bbs.soyun.org/index.php?m=profile" tabindex="-1" role="menuitem">'.$_SESSION['username'].'</a></li>
                        <li class="divider" role="presentation"></li>
                        <li role="presentation"><a href="loginout.php" tabindex="-1" role="menuitem">退出登录</a></li>
                      </ul>
                    </li>';
}
?>
</ul>
     </div>
 
    </div>
  </div>
</div>


