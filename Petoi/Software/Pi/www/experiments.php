<HTML>

<HEAD>

<TITLE>RepRap Ltd Quadruped Robot</TITLE>

<link rel="stylesheet" href="styles.css">

</HEAD>

<BODY>

<H1>RepRap Ltd Quadruped Robot</H1>



<HR>

<H2>Experiments</H2>

<form method="get" action="experiment-script.php">
<button type="submit">Do something!</button>
</form>


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
