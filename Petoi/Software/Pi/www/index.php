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

Sally Bowyer
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

/* Make the current servo postion its zero position */

function SaveCurrentAngleAsOffset()
{
  $call = 'send-command-get-reply.php?args=ChangeServo,' + $currentServo + ',saveCurrentAngleAsOffset';
  $.get($call, function(data) 
  {
     $('#servo_a').empty().append(data);
     getLegPosition(); // Leg may have moved
  });
}

/* Make the servo go in the oposite direction */

function NegateDirection()
{
  $call = 'send-command-get-reply.php?args=ChangeServo,' + $currentServo + ',gegateDirection';
  $.get($call, function(data) 
  {
     $('#servo_a').empty().append(data);
     getLegPosition(); // Leg may have moved
  });
}


/*ZeroServos */

function ZeroServos()
{
  $call = 'send-command-get-reply.php?args=ZeroServos'
  $.get($call, function(data) 
  {
     getLegPosition(); // Leg may have moved
     getServoAngle(); // Servo may have moved
  });
}

/*ZeroServos */

function ZeroServos()
{
  $call = 'send-command-get-reply.php?args=ZeroServos'
  $.get($call, function(data) 
  {
     getLegPosition(); // Leg may have moved
     getServoAngle(); // Servo may have moved
  });
}

/* SaveCurrentPositionAsZeros; */

function SaveCurrentPositionAsZeros()
{
  $call = 'send-command-get-reply.php?args=SaveCurrentPositionAsZeros'
  $.get($call, function(data) 
  {
     getLegPosition(); // Leg may have moved
     getServoAngle(); // Servo may have moved
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
	GetVoltages();
	GetAccelerometer();
	GetRange();
	setUpCanvas();
}

/* Refresh Accelerometer */

function RefreshAccelerometer()
{
  $call = 'send-command-get-reply.php?args=RefreshAccelerometer'
  $.get($call, function(data) 
  {
     $('#Accelerometer').empty().append(data);
    
  });
}



/* Get Voltages */

function GetVoltages()
{
  $call = 'send-command-get-reply.php?args=GetVoltages'
  $.get($call, function(data) 
  {
   data = data.replace(/\n/g,"<br>");
   $('#voltageData').empty().append(data);
    
  });
}

/* Get Range */

function GetRange()
{
  $call = 'send-command-get-reply.php?args=GetRange'
  $.get($call, function(data) 
  {
   $('#rangeData').empty().append(data);
    
  });
}

/* Get Leg row pattern */

function GetRowValues()
{
  $call = 'send-command-get-reply.php?args=GetRowValues,' + $currentLeg
  $.get($call, function(data) 
  {
   $('#LegRowData').empty().append($currentLeg + " row pattern: " + data);
    
  });
}

/* Get Accelerometer */

function GetAccelerometer()
{
  $call = 'send-command-get-reply.php?args=GetAccelerometer'
  $.get($call, function(data) 
  {
   $('#accelerometerData').empty().append(data);
    
  });
}

/*******************************************************************************************/

// Leg row design


    function addVertex(x, y) {
        // Add a default speed value for each vertex, you can adjust the default value as needed
        vertices.push({x, y, speed: ''}); // Initialize speed as an empty string or a default value
        draw();
        updateTable();
    }
    
    function undoVertex() {
        vertices.pop();
        draw();
        updateTable();
    }

   // Adjust the saveVertices function to include speed
    function saveVertices() {
        // Now vertices include speed, which you can process or save
        console.log('Saving polygon with vertices and speeds:', vertices);
        // Call your JS function here with vertices
    }

    function drawGridLines() {
        ctx.beginPath();
        ctx.strokeStyle = '#e0e0e0';
        // Draw vertical lines
        for (let x = 0; x <= gridWidth; x += 10) {
            ctx.moveTo(offsetX + x * cellSize, offsetY);
            ctx.lineTo(offsetX + x * cellSize, canvasHeight);
        }
        // Draw horizontal lines
        for (let y = 0; y <= gridHeight; y += 10) {
            ctx.moveTo(offsetX, offsetY + y * cellSize);
            ctx.lineTo(offsetX + gridWidth * cellSize, offsetY + y * cellSize);
        }
        ctx.stroke();
    }

    function drawAxisNumbers() {
        ctx.fillStyle = 'black';
        // Draw X-axis numbers along the bottom
        for (let x = 0; x <= gridWidth; x += 10) {
            ctx.fillText(x, offsetX + x * cellSize - 3, canvas.height - 5); // Adjust for the bottom
        }
        // Draw Y-axis numbers (right-handed system)
        for (let y = 0; y <= gridHeight; y += 10) {
            ctx.fillText(gridHeight - y, 5, offsetY + y * cellSize + 3);
        }
    }

    function drawLines() {
        ctx.strokeStyle = 'black';
        if (vertices.length > 0) {
            ctx.beginPath();
            ctx.moveTo(offsetX + vertices[0].x * cellSize, offsetY + (gridHeight - vertices[0].y) * cellSize);
            vertices.forEach(vertex => {
                ctx.lineTo(offsetX + vertex.x * cellSize, offsetY + (gridHeight - vertex.y) * cellSize);
            });
            ctx.stroke();
        }
    }

    function drawVertices() {
        vertices.forEach(vertex => {
            ctx.fillRect(offsetX + vertex.x * cellSize - 2, offsetY + (gridHeight - vertex.y) * cellSize - 2, 4, 4);
        });
    }
    
    function canvasClick(event) {
    	rect = canvas.getBoundingClientRect();
    	x = event.clientX - rect.left - offsetX;
    	// Adjust the Y-coordinate calculation to round to the nearest grid line
    	y = event.clientY - rect.top - offsetY;
    	gridX = Math.floor(x / cellSize);
    	// Update to round to the nearest grid line for Y
    	gridY = gridHeight - Math.round(y / cellSize);
    	if (gridX >= 0 && gridX < gridWidth && gridY >= 0 && gridY <= gridHeight) {
        	addVertex(gridX, gridY);
    		}
    }
    	
    function undoPoint()
    {
        undoVertex();
        updateTable();
    }
    
    function setUpCanvas()
    {
        window.canvas = document.getElementById('canvas');
    	window.ctx = canvas.getContext('2d');
    	window.vertices = [];
    	window.cellSize = 20;
    	window.gridWidth = 50;
    	window.gridHeight = 40;
    	window.offsetX = 30; // Space for Y-axis numbers
    	window.offsetY = 30; // Additional space for X-axis numbers at the bottom
    	window.canvasHeight = canvas.height - offsetY; // Adjust for bottom X-axis numbers 
    	canvas.addEventListener('click', canvasClick);
        document.getElementById('undo').addEventListener('click', undoPoint);
        document.getElementById('save').addEventListener('click', saveVertices);
        draw();  
    }

    function draw() 
    {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawGridLines();
        drawAxisNumbers();
        drawLines();
        drawVertices();
    }
       
  

 function updateTable() {
        const tableBody = document.getElementById('verticesTable').getElementsByTagName('tbody')[0];
        // Clear existing table rows
        while (tableBody.firstChild) {
            tableBody.removeChild(tableBody.firstChild);
        }
        // Add new rows for each vertex with a speed input
        vertices.forEach((vertex, index) => {
            let row = tableBody.insertRow();
            let cell1 = row.insertCell(0);
            let cell2 = row.insertCell(1);
            let cell3 = row.insertCell(2);
            let cell4 = row.insertCell(3); // Cell for speed input
            cell1.textContent = index + 1;
            cell2.textContent = vertex.x;
            cell3.textContent = vertex.y;
            // Add an input field for speed
            cell4.innerHTML = `<input type="number" value="${vertex.speed}" onchange="updateSpeed(this.value, ${index})">`;
        });
    }
    
        // Function to update speed value in the vertices array
    function updateSpeed(value, index) {
        if (index >= 0 && index < vertices.length) {
            vertices[index].speed = value;
        }
    }
    
    window.updateSpeed = updateSpeed;
    

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

<button onclick="SaveCurrentAngleAsOffset();" > Save current angle as offset </button> 
<br>
<br>
<button onclick="negateDirection();" > Negate Direction </button> 
<br>
<br>
</th></tr>
 
</table>


<br>
<br>
<button onclick="ZeroServos();" > Zero Servos </button> <button onclick="SaveCurrentPositionAsZeros();" > Save current position as zeros </button>
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

<canvas id="canvas" width="1020" height="820"></canvas>
<button id="undo">Undo</button>
<table id="verticesTable">
    <thead>
        <tr>
            <th>Point #</th>
            <th>X</th>
            <th>Y</th>
        </tr>
    </thead>
    <tbody>
    </tbody>
</table>
<button id="save">Save</button>



<br><br><hr>

<H2>Camera</H2>


<center>
<?php include 'camera_ip.php'; ?>
<img src="http://<?= $camera_ip; ?>:8000/stream.mjpg" width="640" height="480">
</center>

<table>
  <tr align="left">
   <th>Snap</th>
   <th>Save</th>
  </tr>
</table>

<table>

</table>

<hr>

<br>
<button value="Get Voltages" onclick="GetVoltages();" > Get Voltages </button><br>
Voltages: <br><span id="voltageData"></span>

<hr>

<br>
<button value="Get Accelerometer" onclick="GetAccelerometer();" > Get Accelerometer </button><br>
Accelerometer: <br><span id="accelerometerData"></span>


<hr>

<br>
<button value="Get Range" onclick="GetRange();" > Get Range </button><br>
Range: <br><span id="rangeData"></span>



</BODY>

</HTML>
