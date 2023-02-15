<html>
<head>
      
<script src="//ajax.googleapis.com/ajax/libs/jquery/2.0.0/jquery.min.js"></script>

<script>
  
function p1()
{
  $call = 'send-command-get-reply.php?args=ChangeServo,0,p1';
  $.get($call, function(data) 
  {
     $('#servo_a').empty().append(data);
  });
} 

function p10()
{
  $call = 'send-command-get-reply.php?args=ChangeServo,0,p10';
  $.get($call, function(data) 
  {
     $('#servo_a').empty().append(data);
  });
} 

function setA()
{
  $angle = document.getElementById("angle").value;
  $call = 'send-command-get-reply.php?args=ChangeServo,0,setAngle,' + $angle;
  $.get($call, function(data) 
  {
     $('#servo_a').empty().append(data);
  });
} 

</script>

</head>

<body>

<button onclick="p1()">+1</button>
<br>
<button onclick="p10()">+10</button>
<br>
<button onclick="setA()">Set angle to </button><input type="text" id="angle" size="4">
<br>
Servo angle: <span id="servo_a">Boo!</span>
   
</body>
</html>



