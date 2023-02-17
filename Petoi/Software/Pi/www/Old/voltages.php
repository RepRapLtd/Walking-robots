<HTML>

<HEAD>

<TITLE>RepRap Ltd Quadruped Robot</TITLE>

</HEAD>

<BODY>

<H1>RepRap Ltd Quadruped Robot</H1>

<HR>

<h2>Voltages</h2>

<?php 
 $output = shell_exec('python3 voltages.py');
 $output = str_replace("\n", "<br>", $output);
 echo $output; 
?>

<a href="index.php">Home</a>


</BODY>

</HTML>
