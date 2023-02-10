<HTML>

<HEAD>

<TITLE>RepRap Ltd Quadruped Robot</TITLE>

<link rel="stylesheet" href="styles.css">

<script src="//ajax.googleapis.com/ajax/libs/jquery/2.0.0/jquery.min.js"></script>

<script>

$lastServo = 0;
$servoAngle = 0;
  
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
     $servoAngle = data;
     $('#servo_a').empty().append(data);
  });
}


function setA()
{
  $angle = document.getElementById("angle").value;
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

</script>


</HEAD>

<BODY>
<?php include('header.php'); ?>

<H1>Servos</H1>


<table>
  
<tr align="left"><th> 
<p>Select Servo</p>
<input type="radio" id="0" name="Servo" value="0" checked="checked" onclick="setServo(0);"> 
<label for="0">0</label> <br>
<input type="radio" id="1" name="Servo" value="1" onclick="setServo(1);">
<label for="1">1</label><br>
<input type="radio" id="6" name="Servo" value="6" onclick="setServo(6);">
<label for="6">6</label><br>
<input type="radio" id="7" name="Servo" value="7" onclick="setServo(7);">
<label for="7">7</label><br>  
<input type="radio" id="8" name="Servo" value="8" onclick="setServo(8);">
<label for="8">8</label><br>
<input type="radio" id="9" name="Servo" value="9" onclick="setServo(9);">
<label for="9">9</label><br>
<input type="radio" id="12" name="Servo" value="12" onclick="setServo(12);">
<label for="12">12</label><br>
<input type="radio" id="14" name="Servo" value="14" onclick="setServo(14);">
<label for="14">14</label><br>
<input type="radio" id="15" name="Servo" value="15" onclick="setServo(15);">
<label for="15">15</label><br>

</th><th rowspan="1">

<h2>Servo <span id="servoNumber">0</span></h2>

Angle: <span id="servo_a">0</span><sup>o</sup>
<br>
<br>

<button value="Home" > Home </button>
<button onclick="changeServoAngle('p1');"> +1 </button>
<button onclick="changeServoAngle('p10');"> +10 </button>
<button onclick="changeServoAngle('m1');"> -1 </button>
<button onclick="changeServoAngle('m10');"> -10 </button>
<br><br><br>
<button onclick="setA()">Set angle to </button><input type="text" id="angle" size="4">

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
<button type="submit" value="Home" > Zero Servos </button> <button type="submit" value="Home" > Save current position as zeros </button> <!-- Need to set what the buttons do as currently same as "Home" Button below -->






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
