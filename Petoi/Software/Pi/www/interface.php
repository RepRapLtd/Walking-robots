<HTML>

<HEAD>




<TITLE>RepRap Ltd Quadruped Robot</TITLE>

<link rel="stylesheet" href="styles.css">

</HEAD>

<BODY>
<?php include('header.php'); ?>

Aide-mémoire.
<br>
List of commands and arguments sent to the robot via a socket:
<br><br>
HOST, PORT = "localhost", 9999
<br>
socketserver.TCPServer((HOST, PORT), TCPHandler)
<br>
<br>
Commands. * means client side in javascript, otherwise PHP on the server:

<ul>
  <li>* ChangeServo servo option [angle]</li>
  <ul>
  <li>+1</li>
  <li>-1</li>
  <li>+10</li>
  <li>-10</li>
  <li>zero</li>
  <li>setAngle angle</li>
  <li>negateDirection</li>
  <li>saveCurrentAngleAsOffset</li>
  </ul>
  <li>GetLegNames</li>
  <li>GetLegDescription legName</li>
  <li>GetServoAngle servoNumber</li>
  <li>GetVoltages</li>
  <li>* MoveLegFast name x y</li>
  <li>* MoveLegStraight name x y v</li>
  <li>* Exit</li> 
</ul>
<br>
Example:
<pre>
<?php
 echo "<&ZeroWidthSpace;?&ZeroWidthSpace;php<br>";
 echo " \$output = shell_exec('python3 send-command-get-reply.py GetLegNames');<br> \$legNames = explode(' ',\$output);<br>?>";
?>
</pre>

</BODY>

</HTML>
