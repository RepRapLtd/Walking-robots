<?php
function SendToRobot($commandLine)
{
	return shell_exec("python3 send-command-get-reply.py ".$commandLine);
}

$command = str_replace(","," ", $_GET["args"]);
echo SendToRobot($command);
?>

