<HTML>

<HEAD>




<TITLE>RepRap Ltd Quadruped Robot</TITLE>

<link rel="stylesheet" href="styles.css">

</HEAD>

<BODY>
<?php include('header.php'); ?>

<H2>Servos</H2>
<table>
  <tr align="left"><th>Zero servos</th><th>blah blah blah</th></tr>
  <tr align="left"><th>Save current position as zeros</th><th>blah blah blah</th></tr>
  <tr align="left"><th><a href="servo.php?s=0">Servo 0</a></th><th rowspan="9">blah blah blah</th></tr>
  <tr align="left"><th><a href="servo.php?s=1">Servo 1</a></th></tr>
  <tr align="left"><th><a href="servo.php?s=6">Servo 6</a></th></tr> 
  <tr align="left"><th><a href="servo.php?s=7">Servo 7</a></th></tr>
  <tr align="left"><th><a href="servo.php?s=8">Servo 8</a></th></tr>
  <tr align="left"><th><a href="servo.php?s=9">Servo 9</a></th></tr>
  <tr align="left"><th><a href="servo.php?s=12">Servo 12</a></th></tr>
  <tr align="left"><th><a href="servo.php?s=14">Servo 14</a></th></tr>
  <tr align="left"><th><a href="servo.php?s=15">Servo 15</a></th></tr> 
 
</table>

<a

<h2> <?php 
$servo=$_GET["s"];
echo 'Servo ' . htmlspecialchars($servo) ;?>
</h2>

Angle: <?php 
 $output = shell_exec('python3 send-command-get-reply.py GetServoAngle '.$servo );

 echo $output; 
?>     <sup>o</sup>
<br>
<br>
<form id="myForm">
 
<button type="submit" value="Home" > Home </button>
<button type="submit" value="+1" > +1 </button>
<button type="submit" value="+10" > +10 </button>
<button type="submit" value="-1" > -1 </button>
<button type="submit" value="-10" > -10 </button>

<br>
<br> <label for="myName">Set angle:</label>
  <input id="myName" name="name" value="" />
<button type="submit" value="set" >Set </button>
<br>
<br>
<button type="submit" value="save" > Save current angle as offset</button>
<br>
<br>
<button type="submit" value="-negate" > Negate Direction </button>

</form>


<script>
   window.addEventListener("load", () => {
  function sendData() {

$button=$_POST['action'];

    const XHR = new XMLHttpRequest();

    // Bind the FormData object and the form element
    const FD = new FormData(form);

    // Define what happens on successful data submission
    XHR.addEventListener("load", (event) => {
      alert(event.target.responseText);
    });

    // Define what happens in case of error
    XHR.addEventListener("error", (event) => {
      alert('Oops! Something went wrong.');
    });

    // Set up our request
    XHR.open("POST", "http://192.168.68.192/receive.php?b=".$button);

    // The data sent is what the user provided in the form
    XHR.send(FD);
  }

  // Get the form element
  const form = document.getElementById("myForm");

  // Add 'submit' event handler
  form.addEventListener("submit", (event) => {
    event.preventDefault();

    sendData();
  });
});
  </script>
</a>


<H2>Legs</H2>

<?php 
 $output = shell_exec('python3 send-command-get-reply.py GetLegNames '.$servo );
 $tokens = explode(" ",$output);
?> 

<table>
  <tr align="left">
   <th><a href="leg.php?l=fl"><?php echo $tokens[0]; ?> </a></th>
   <th><a href="leg.php?l=fr"><?php echo $tokens[1]; ?></a></th>
  </tr>
  
  <tr align="left">
   <th><a href="leg.php?l=bl"><?php echo $tokens[2]; ?></a></th>
   <th><a href="leg.php?l=br"><?php echo $tokens[3]; ?></a></th>
  </tr>
 
</table>
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
