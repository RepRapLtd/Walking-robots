<?php
function SendToRobot($commandLine)
{
	return shell_exec("python3 send-command-get-reply.py ".$commandLine);
	//return shell_exec("./pyechoarg.py ccc");
}

$op = SendToRobot("GetLastServo");
echo $op;
?>

