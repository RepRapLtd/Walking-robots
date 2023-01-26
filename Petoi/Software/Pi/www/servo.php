<HTML>

<HEAD>

<TITLE>RepRap Ltd Quadruped Robot</TITLE>

<link rel="stylesheet" href="styles.css">

</HEAD>

<BODY>

<?php include('header.php'); ?>

<h2> <?php 
$servo=$_GET["s"];
echo 'Servo ' . htmlspecialchars($servo) ;?>
</h2>

Angle: 0<sup>o</sup>

<br>

<table>
  <tr align="left"><th>+1</th></tr>
  <tr align="left"><th>-1</th></tr>
  <tr align="left"><th>+10</th></tr>
  <tr align="left"><th>-10</th></tr>
  <tr align="left"><th>Set angle</th></tr>
  <tr align="left"><th>Negate direction</th></tr> 
  <tr align="left"><th>Save current angle as offset</th></tr>   
</table>

<a href="servos.php">Back to servo selection</a>
<br>
<a href="index.php">Home</a>

</BODY>

</HTML>
