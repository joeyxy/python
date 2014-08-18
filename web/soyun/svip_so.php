<?php



require_once ('sgk.php');
include('function.php');
?>
<meta charset="utf-8">
<?php



$search =addslashes(trim($_GET['so']));
$search = iconv('utf-8','gbk//IGNORE',$search);
if (!empty($_GET['so']))
{
	$user = $_SESSION['username'];
	// $sql1 = 'update user set jb=jb-'1' where username='($user)'';//扣jb
	// mysql_query($sql1);
	 $sql = "select top 20 * from dbo.sgk where CONTAINS(*,'$search')  and 1=1";
	$query = sqlsrv_query($conn,$sql);
	//echo $sql;
	$num=sqlsrv_num_rows($query);
	//print_r ($rows);
	// if (sqlsrv_rows_affected($query) != 0)	{
	

	
		echo '<table>';
		echo '<td width=\'8%\'><div align=\'center\'>User</div></td>';
		echo '<td width=\'27%\'><div align=\'center\'>Pass</div></td>';
		echo '<td width=\'25%\'><div align=\'center\'>Email</div></td>';
		echo '<td width=\'10%\'><div align=\'center\'>Site</div></td>';
		echo '<td width=\'9%\'><div align=\'center\'>Salt</div></td>';
		echo '<td width=\'21%\'><div align=\'center\'>Other</div></td>';
		if ($_GET['auto']=="on"){
			while ($row = array_zhuan(sqlsrv_fetch_array($query))) {
			$name1=strip_tags($row['name1']);
			$pass=strip_tags($row['pass']);
			$email=strip_tags($row['email']);
			$site=strip_tags($row['site']);
			$salt=strip_tags($row['salt']);
			$other=strip_tags($row['other']);
			echo '<tr>';
			echo '<td width="8%" >'.$name1.'</td>';
			echo '<td width="27%">'.$pass.'</td>';
			echo '<td width="25%">'.$email.'</td>';
			echo '<td width="21%">'.$site.'</td>';
			echo '<td width="9%">'.$salt.'</td>';
			echo '<td width="10%">'.$other.'</td>';
			echo "</tr>";
			if ($name1<>$search){
			$sql = "select top 20 * from dbo.sgk where CONTAINS(name1,'$name1') and 1=1";
			$query = sqlsrv_query($conn,$sql);
			while ($row1 = array_zhuan(sqlsrv_fetch_array($query))) {
			$name1=strip_tags($row1['name1']);
			$pass=strip_tags($row1['pass']);
			$email=strip_tags($row1['email']);
			$site=strip_tags($row1['site']);
			$salt=strip_tags($row1['salt']);
			$other=strip_tags($row1['other']);

			echo '<tr>';
						echo '<td width="8%" >'.$name1.'</td>';
			echo '<td width="27%">'.$pass.'</td>';
			echo '<td width="25%">'.$email.'</td>';
			echo '<td width="21%">'.$site.'</td>';
			echo '<td width="9%">'.$salt.'</td>';
			echo '<td width="10%">'.$other.'</td>';
			echo '</tr>';
			}
			}
			if (email_main($email)<>$search and Null){
			$sql = "select top 20 * from dbo.sgk where CONTAINS(email,'$email')  and 1=1";
			$query = sqlsrv_query($conn,$sql);
			while ($row2 = array_zhuan(sqlsrv_fetch_array($query))) {
			$name1=strip_tags($row2['name1']);
			$pass=strip_tags($row2['pass']);
			$email=strip_tags($row2['email']);
			$site=strip_tags($row2['site']);
			$salt=strip_tags($row2['salt']);
			$other=strip_tags($row2['other']);
			echo '<tr>';
						echo '<td width="8%" >'.$name1.'</td>';
			echo '<td width="27%">'.$pass.'</td>';
			echo '<td width="25%">'.$email.'</td>';
			echo '<td width="21%">'.$site.'</td>';
			echo '<td width="9%">'.$salt.'</td>';
			echo '<td width="10%">'.$other.'</td>';
			echo '</tr>';
			}
			}

			//print_r ($row);
		}
				 echo "</div></td>";
		 
		 echo "</table>";	
		 		echo '
<script>
   window.onload = function(){
      
      var strTemp = document.body.innerHTML.replace(/'.$search.'/g ,"<font color=red>'.$search.'</font>");
      document.body.innerHTML = strTemp;
   }
</script>
';
}
// }
else
{
				while ($row = array_zhuan(sqlsrv_fetch_array($query))) {
			$name1=strip_tags($row['name1']);
			$pass=strip_tags($row['pass']);
			$email=strip_tags($row['email']);
			$site=strip_tags($row['site']);
			$salt=strip_tags($row['salt']);
			$other=strip_tags($row['other']);
			echo '<tr>';
			echo '<td width="8%" >'.$name1.'</td>';
			echo '<td width="27%">'.$pass.'</td>';
			echo '<td width="25%">'.$email.'</td>';
			echo '<td width="21%">'.$site.'</td>';
			echo '<td width="9%">'.$salt.'</td>';
			echo '<td width="10%">'.$other.'</td>';
			echo "</tr>";
		}
				 echo "</div></td>";
		 
// if ($_GET['vip'] == 'open'){


// $sql="select * from main where username='".$_SESSION['username']."'";
// $a=mysql_query($sql,$conn1);
// if (mysql_affected_rows() <> 0)
// {
	$sql = "select top 20 * from text.dbo.text where CONTAINS(*,'".addslashes($_GET['so'])."')";
	$query = sqlsrv_query($conn,$sql);
	

if (sqlsrv_rows_affected($query) != 0)	{
	echo '<div class="container">';
	
	echo "此结果来自内部社工库";
	while ($row = array_zhuan(sqlsrv_fetch_array($query))) {
		$results=$row[2];
		
		if (!ctype_space($results)){

		echo ("<li>From:[".$row[1]."]<br></li>");
		
		echo ("<li>Text:<br>".htmlspecialchars($row[2])."</li><br>");
	
	}

	}	
	$sql = "select top 20 * from disk.dbo.Text where CONTAINS(*,'".addslashes($_GET['so'])."')";
	$query= sqlsrv_query($conn,$sql);
	while ($row = array_zhuan(sqlsrv_fetch_array($query))) {
		$results=$row[2];
		
		if (!ctype_space($results)){

		echo ("<li>From:[".$row[1]."]<br></li>");
		echo ("<li>Text:<br>".htmlspecialchars($row[2])."</li><br>");
	
	}

	}
echo "</div>";
}
// }
		 		echo '
<script>
   window.onload = function(){
      
      var strTemp = document.body.innerHTML.replace(/'.$search.'/g ,"<font color=red>'.$search.'</font>");
      document.body.innerHTML = strTemp;
   }
</script>
';
}
}
sqlsrv_close($conn);



?>


