<?php

  error_reporting(0);
  $dir = "/tmp";
  $tmp_name = $_FILES['upload_file']['tmp_name'];
  $actual_name = $FILES['upload_file']['name'];
  $size = $_FILES['upload_file']['size'];
  $type = $_FILES['upload_file']['type'];
  move_uploaded_file($tmp_name,$dir.$actual_name);
  echo "<img src=\"".$dir.$actual_name."\">";
?>
