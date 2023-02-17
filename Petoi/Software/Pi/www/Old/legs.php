<HTML>

<HEAD>

<TITLE>RepRap Ltd Quadruped Robot</TITLE>

<link rel="stylesheet" href="styles.css">

</HEAD>

<BODY>

<?php include('header.php'); ?>

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





</BODY>

</HTML>
