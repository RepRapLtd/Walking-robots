<HTML>

<HEAD>

<TITLE>RepRap Ltd Quadruped Robot</TITLE>

<link rel="stylesheet" href="styles.css">

</HEAD>

<BODY>

<?php include('header.php'); ?>
<a href="servos.php">Back to Servo Selection</a>
<h2> <?php 
$servo=$_GET["s"];
echo 'Servo ' . htmlspecialchars($servo) ;?>
</h2>

Angle: 0<sup>o</sup>
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


</BODY>

</HTML>
