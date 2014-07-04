<html>

<head>
<title>key down test</title>

<script>
function keyDown(){
   var keycode = event.keyCode;
   var realkey = String.fromCharCode(event.keyCode);
   alert('key:'+keycode+"char:"+realkey);
}
 document.onkeydown = keyDown;

</script>


</head>



</html>
