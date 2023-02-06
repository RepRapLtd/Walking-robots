<HTML>

<HEAD>

<TITLE>RepRap Ltd Quadruped Robot</TITLE>

<link rel="stylesheet" href="styles.css">

</HEAD>



<BODY>

<H1>RepRap Ltd Quadruped Robot</H1>

<HR>

<H2>Experiments</H2>

<?php
function SendToRobot($commandLine)
{
	return shell_exec('python3 send-command-get-reply.py '.$commandLine);
}
?>



<form action="experiment.php" method="post">
    <input type="submit" name="plus1" value="+1" />
    <input type="submit" name="plus10" value="+10" />
</form>

<?php
    $output = "";
    
    if($_SERVER['REQUEST_METHOD'] == "POST")
    {
        if(isset($_POST['plus1']))
        {
        	SendToRobot("ChangeServo 0 +1");
        	$output = SendToRobot("GetServoAngle 0");
        } elseif(isset($_POST['plus10']))
    	{
        	SendToRobot("ChangeServo 0 +10");
        	$output = SendToRobot("GetServoAngle 0");
    	}
    }
    
    echo "Servo angle: ".$output;
?>


<br>

Range is: <?php $output = shell_exec('python3 range.py'); echo $output; ?>
<br>
Last scan:
<br>
..............<br>
.............<br>
...........<br>
..........<br>
<br>
Take single reading
<br>
Scan
<br>

<a href="index.php">Home</a>



</BODY>

</HTML>

