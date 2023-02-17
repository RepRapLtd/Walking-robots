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

/*

Quadruped Robot Web-page-based Control

Version 1

Sall Bowyer
Adrian Bowyer

RepRap Ltd

https://reprapltd.com

17 February 2023

Licence: GPL

*/

/* Javascript globals - we need to remember which servo and leg we're talking to and the leg's foot's position. */


$currentServo = 0;
$currentLeg = "front-left";
$legX = 0;
$legY = 0;


/*

This first Javascript function shows the general form of a function that talks to the robot. There are a
number of these for different robot commands and activities.

Communications follow this route (how they are achieved is in [...]):

	index.php (this file sends a command or request)
	  |
	  [jquery send-command-get-reply.php?args=a1,a2,a3]
	  |
	  V
	send-command-get-reply.php
	  |
	  [shell_exec send-command-get-reply.py a1 a2 a3...]
	  |
	  V
	send-command-get-reply.py
	  |
	  [send command line args to the socket]
	  |
	  V
	petoi-server.py (socket text makes the robot do something and return data)
	  |
	  [send the return data text to the socket]
	  |
	  V
	send-command-get-reply.py
	  |
	  [print("the text from the socket")]
	  |
	  V
	send-command-get-reply.php
	  |
	  [echo the result of the Python print(); ]
	  |
	  V
	index.php (this file receives the thing from the echo...;)

This seems slightly convoluted, but it allows the petoi-server.py to be running all the time
controlling the robot. The PHP file send-command-get-reply.php is just a small wrapper for the 
equally small Python program send-command-get-reply.py, which handles the socket communications
with the robot (petoi-server.py).
  
These control functions have zero or more arguments that bring data in from the web page
buttons and text boxes. They all construct a text string $call which looks like this:

  send-command-get-reply.php?args=a1,a2,a3....
  
This is an ordinary web HTTP address with arguments. The first argument (a1) tells the robot what to do
and the following ones give it data to do that with, like positions, angles, speeds and so on.

The next line:

  $.get($call, function(data)
  
executes $call (that is send-command-get-reply.php) on the robot web server and gets any text back
in data. The subsequent lines then deal with that data. 

This particular function changes the servo $currentServo by angle $delta degrees. So, for example, in this function the line

  $('#servo_a').empty().append(data);
  
finds the part of the web page that says this:

  <span id="servo_a">0</span>
  
and replaces the 0 with the new angle returned from the robot in data. The next line

  getLegPosition();
  
asks the robot where the leg $currentLeg is and updates its position on the web page. This is in case moving the servo also happened to move the leg $currentLeg (which it may not have, of course).
But updating the leg position on the web page is never going to do any harm. */
 
function changeServoAngle($delta)
{
  $call = 'send-command-get-reply.php?args=ChangeServo,' + $currentServo + ',changeBy,' + $delta;
  $.get($call, function(data) 
  {
     $('#servo_a').empty().append(data);
     getLegPosition(); // Leg may have moved
  });
}

/* The getServoAngle() function gets the angle that $currentServo is at and updates the web page angle text.*/

function getServoAngle()
{
  $call = 'send-command-get-reply.php?args=GetServoAngle,' + $currentServo;
  $.get($call, function(data) 
  {
     $('#servo_a').empty().append(data);
  });
}

/* The moveLegStraight($x, $y, $v) funtion moves the foot of $currentLeg to the point ($x, $y) mm at speed $v mm/s. The robot will reply with the point the foot has ended up at, which is then used to update the web page. Moving a leg may also have changed the the angle of $currentServo, so that is updated as well.

Note that the foot cannot move to any point ($x, $y) - the leg is only so long... If a move can't be made the robot will do nothing and the leg's position won't change.
*/

function moveLegStraight($x, $y, $v)
{
  $call = 'send-command-get-reply.php?args=MoveLegStraight,' + $currentLeg + "," + $x + "," + $y + "," + $v;
  $.get($call, function(data) 
  {
     $pos = data.split(" ");
     $legX = $pos[0];
     $legY = $pos[1];
     $('#legX').empty().append($legX);
     $('#legY').empty().append($legY);
     getServoAngle(); // Servo may have moved
  });
}

/* The changeLegPos($dx, $dy) is like the moveLegStraight($x, $y, $v) function, but it moves the leg as fast as it will go to the target point and doesn't bother about going in a straight line. */

function changeLegPos($dx, $dy)
{
  $x = parseFloat($legX) + parseFloat($dx);
  $y = parseFloat($legY) + parseFloat($dy);
  $call = 'send-command-get-reply.php?args=MoveLegFast,' + $currentLeg + "," + $x + "," + $y;
  $.get($call, function(data) 
  {
     $pos = data.split(" ");
     $legX = $pos[0];
     $legY = $pos[1];
     $('#legX').empty().append($legX);
     $('#legY').empty().append($legY);
     getServoAngle(); // Servo may have moved
  });
}

/* getLegPosition() gets the (x, y) position of $currentLeg and updates the web page with it. */

function getLegPosition()
{
  $call = 'send-command-get-reply.php?args=GetLegPosition,' + $currentLeg;
  $.get($call, function(data) 
  {
     $pos = data.split(" ");
     $legX = $pos[0];
     $legY = $pos[1];
     $('#legX').empty().append($legX);
     $('#legY').empty().append($legY);
  });
}

/* setServoAngle($angle) moves $currentServo to a specified angle, as opposed to changing it by + or - an angle. */
/* ***TODO Constrain Angle */

function setServoAngle($angle)
{
  $call = 'send-command-get-reply.php?args=ChangeServo,' + $currentServo + ',setAngle,' + $angle;
  $.get($call, function(data) 
  {
     $('#servo_a').empty().append(data);
  });
}

/* chooseServo($s) changes the currently selected servo $currentServo. It does not talk to the robot.*/

function chooseServo($s)
{
 $currentServo = $s;
 document.getElementById("servoNumber").textContent = $currentServo;
 getServoAngle();
}

/* chooseLeg($l) changes the currently selected leg $currentLeg. It does not talk to the robot. */

function chooseLeg($l)
{
 $currentLeg = $l;
 document.getElementById("legName").textContent = $currentLeg;
 getLegPosition();
}

/* AtStart($s, $l) runs once when this page is first loaded from the server to set the initial servo and leg.
It doesn't talk to the robot. */

function AtStart($s, $l)
{
	chooseServo($s);
	chooseLeg($l);
}

</script>


</HEAD>

<?php

/* On the robot server as this page is loading ask the robot for its list of active servos.
This also checks if the robot server is running (you get a reply) or not (you get nothing - "").
It records a message if the server isn't running for later display. */
 
 $reply = shell_exec("python3 send-command-get-reply.py GetActiveServos");
 $noServer = "";
 if($reply == $noServer)
 {
  $noServer = "<br><br><H2>The robot server is not running. Start it, then refresh this page.</H2><br><br>";
 }
 $servos = explode(" ",$reply);
 
/* Now ask the robot for the names of its legs. */
 
 $reply = shell_exec("python3 send-command-get-reply.py GetLegNames");
 $legs = explode(" ",$reply);
 
/* $loadFunction will be used by the HTML <BODY onload... to call the
Javascript function for page load above. Set the servo and leg to the first ones.
*/ 
 
 $loadFunction = "AtStart(" . $servos[0] . ",'" . $legs[0] . "');";

?>


<BODY onload = "<?php echo $loadFunction; ?>" >



<?php include('header.php'); ?>



<?php

/* This displayes the message that was recorded on whether the server is running or not. */

echo $noServer;

?>


<H2>Servos</H2>


<table>
  
<tr align="left"><th> 
<p>Select Servo</p>

<?php

/* Make the list of servo radio buttons from the list sent by the robot above. We know that the first one should be the one checked initially. The ctype_print function makes sure each name is a printable one - sometimes there is a bit of rubbish text on the end of the list. */

 foreach($servos as $servo)
 {
   $check = '';
   if($servo == $servos[0])
   {
   	$check = 'checked="checked" ';
   }
   if(ctype_print($servo))
   {
      echo '<input type="radio" id="'.$servo.'" name="Servo" value="'.$servo.'" '.$check.'onclick="chooseServo('.$servo.');"> <label for="'.$servo.'">'.$servo.'</label> <br>';
   }
 }
?>

</th>
<th>
<br>
<h3>Servo: <span id="servoNumber">0</span></h3>

Angle: <span id="servo_a">0</span><sup>o</sup>
<br>
<br>

<button value="Home" onclick="setServoAngle(0);" > Home </button>
<button onclick="changeServoAngle(-10);"> -10 </button>
<button onclick="changeServoAngle(-1);"> -1 </button>
<button onclick="changeServoAngle(1);"> +1 </button>
<button onclick="changeServoAngle(10);"> +10 </button>
<br><br><br>
<button onclick="setServoAngle(document.getElementById('angle').value);">Set angle to</button> <input type="text" id="angle" size="4">

<br><br><br>

<!-- ***TODO all these. -->

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

/* Make the list of leg radio buttons from the list sent by the robot above. We know that the first one should be the one checked initially. The ctype_print function makes sure each name is a printable one - sometimes there is a bit of rubbish text on the end of the list. */

 foreach($legs as $leg)
 {
   $check = '';
   if($leg == $legs[0])
   {
   	$check = 'checked="checked" ';
   }
   if(ctype_print($leg))
   {
      echo '<input type="radio" id="'.$leg.'" name="Leg" value="'.$leg.'" '.$check.'onclick="chooseLeg(\''.$leg.'\');"> <label for="'.$leg.'">'.$leg.'</label> <br>';
   }
 }
?>

</th>
<th>
<br>
<h3>Leg: <span id="legName">leg</span></h3>

Position: x = <span id="legX">0</span>, y = <span id="legY">0</span> mm
<br>
<br>

<button value="Home" onclick="changeLegPos(-$legX, -$legY);" > Home </button><br><br>
x: 
<button onclick="changeLegPos(-5, 0);"> -5 </button>
<button onclick="changeLegPos(-1, 0);"> -1 </button>
<button onclick="changeLegPos(1, 0);"> +1 </button>
<button onclick="changeLegPos(5, 0);"> +5 </button>


<br>
y: 
<button onclick="changeLegPos(0, -5);"> -5 </button>
<button onclick="changeLegPos(0, -1);"> -1 </button>
<button onclick="changeLegPos(0, 1);"> +1 </button>
<button onclick="changeLegPos(0, 5);"> +5 </button>


<br><br><br>
<button onclick="moveLegStraight(document.getElementById('xPos').value, document.getElementById('yPos').value, document.getElementById('velocity').value);">Move to</button> x: <input type="text" id="xPos" size="3"> y: <input type="text" id="yPos" size="3"> v: <input type="text" id="velocity" size="3">

<br><br><br>

<br>
<br>
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
  <tr align="left"><th><a href="accelerometer.php">Accelerometer</a></th></tr>
  <tr align="left"><th><a href="range.php">Range</a></th></tr>
  <tr align="left"><th><a href="voltages.php">Voltages</a></th></tr>
</table>

</BODY>

</HTML>
