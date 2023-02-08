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
	return shell_exec("nohup python3 send-command-get-reply.py ".$commandLine." 2>&1 &");
}

$lastServo = SendToRobot("GetLastServo");
echo "lastServo: ".$lastServo."<br>";
if($lastServo === "")
{
       echo "Server not running. Start the server then refresh this page.";
}
?>

<form action="experiment.php" method="post">
    <input type="submit" name="plus1" value="+1" />
    <input type="submit" name="plus10" value="+10" />
    <input type="submit" name="exit" value="stop server" />
</form>

<?php

$output = "";

    
if($_SERVER['REQUEST_METHOD'] == "POST")
{
        if(isset($_POST['plus1']))
        {
		$output = SendToRobot("ChangeServo ".$lastServo." +1");
        } elseif(isset($_POST['plus10']))
    	{
        	$output = SendToRobot("ChangeServo ".$lastServo." +10");
    	} elseif(isset($_POST['exit']))
    	{
        	$output = SendToRobot("Exit");
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

