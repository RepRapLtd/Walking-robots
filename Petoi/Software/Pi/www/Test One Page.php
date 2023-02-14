<HTML>
<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
?>

<HEAD>

<TITLE>RepRap Ltd Quadruped Robot</TITLE>

<link rel="stylesheet" href="styles.css">

<script src="//ajax.googleapis.com/ajax/libs/jquery/2.0.0/jquery.min.js"></script>

<script>

$lastServo = 0;
$lastLeg = 0;
 
function changeServoAngle($delta)
{
  $call = 'send-command-get-reply.php?args=ChangeServo,' + $lastServo + ',' + $delta;
  $.get($call, function(data) 
  {
     $('#servo_a').empty().append(data);
  });
}

function getServoAngle()
{
  $call = 'send-command-get-reply.php?args=GetServoAngle,' + $lastServo;
  $.get($call, function(data) 
  {
     $('#servo_a').empty().append(data);
  });
}

function getLegData()
{

}


function setA($angle)
{
  $call = 'send-command-get-reply.php?args=ChangeServo,' + $lastServo + ',setAngle,' + $angle;
  $.get($call, function(data) 
  {
     $('#servo_a').empty().append(data);
  });
}

function setServo($s)
{
 $lastServo = $s;
 document.getElementById("servoNumber").textContent = $lastServo;
 getServoAngle();
}

function setLeg($l)
{
 $lastLeg = $l;
 document.getElementById("legNumber").textContent = $lastLeg;
 getLegData();
}


function AtStart($s, $l)
{
	$lastLeg = $l;
	setServo($s);
}

</script>


</HEAD>

<?php
 $reply = shell_exec("python3 send-command-get-reply.py GetActiveServos");
 $noServer = "";
 if($reply == "")
 {
  $noServer = "<br><br><H2>The robot server is not running. Start it, then refresh this page.</H2><br><br>";
 }
 $servos = explode(" ",$reply);
 
 $reply = shell_exec('python3 send-command-get-reply.py GetLegNames ');
 $legs = explode(" ",$reply);
 
 $loadFunction = "AtStart(" . $servos[0] . ",'" . $legs[0] . "');";

?>


<BODY onload = "<?php echo $loadFunction; ?>" >



<?php include('header.php'); ?>

<?php echo $noServer;?>


<H2>Servos</H2>


<table>
  
<tr align="left"><th> 
<p>Select Servo</p>

<?php
 foreach($servos as $servo)
 {
   $check = '';
   if($servo == $servos[0])
   {
   	$check = 'checked="checked" ';
   }
   if(ctype_print($servo))
   {
      echo '<input type="radio" id="'.$servo.'" name="Servo" value="'.$servo.'" '.$check.'onclick="setServo('.$servo.');"> <label for="'.$servo.'">'.$servo.'</label> <br>';
   }
 }
?>

</th>
<th>

<h2>Servo <span id="servoNumber">0</span></h2>

Angle: <span id="servo_a">0</span><sup>o</sup>
<br>
<br>

<button value="Home" onclick="setA(0);" > Home </button>
<button onclick="changeServoAngle('p1');"> +1 </button>
<button onclick="changeServoAngle('p10');"> +10 </button>
<button onclick="changeServoAngle('m1');"> -1 </button>
<button onclick="changeServoAngle('m10');"> -10 </button>
<br><br><br>
<button onclick="setA(document.getElementById('angle').value);">Set angle to</button> <input type="text" id="angle" size="4">

<br><br><br>

<button type="submit" value="save" > Save current angle as offset</button>
<br>
<br>

<button type="submit" value="-negate" > Negate Direction </button>

<br>
<br>
</th></tr>
 
</table>


<br>
<br>
<button type="submit" value="Home" > Zero Servos </button> <button type="submit" value="Home" > Save current position as zeros </button> 


<br><br><hr>
<H2>Legs</H2>



<table>
  <tr align="left">
   <th> 
<p>Select Leg</p>

<?php
 foreach($legs as $leg)
 {
   $check = '';
   if($leg == $legs[0])
   {
   	$check = 'checked="checked" ';
   }
   if(ctype_print($leg))
   {
      echo '<input type="radio" id="'.$leg.'" name="Leg" value="'.$leg.'" '.$check.'onclick="setLeg('.$leg.');"> <label for="'.$leg.'">'.$leg.'</label> <br>';
   }
 }
?>

</th>
  </tr>
 
</table>

<br><br><hr>

<H2>Camera</H2>

<img src="testpic.jpg" alt="robot camera image" width="500">

<table>
  <tr align="left">
   <th>Snap</th>
   <th>Save</th>
  </tr>
</table>

<table>

</table>


<table>
  <tr align="left"><th><a href="servos.php">Servos</a></th></tr>
  <tr align="left"><th><a href="legs.php">Legs</a></th></tr>
  <tr align="left"><th><a href="camera.php">Camera</a></th></tr>
  <tr align="left"><th><a href="accelerometer.php">Accelerometer</a></th></tr>
  <tr align="left"><th><a href="range.php">Range</a></th></tr>
  <tr align="left"><th><a href="voltages.php">Voltages</a></th></tr>
</table>

</BODY>

</HTML>
