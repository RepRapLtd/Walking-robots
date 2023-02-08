
<html>
   <head>
      <script src="//ajax.googleapis.com/ajax/libs/jquery/2.0.0/jquery.min.js"></script>
      <script type="text/javascript">
      $call = 'pyechoarg.php';
     $(document).ready(function() {
        $('#plus_1').click(function() {
           //alert("success1");
           $.get($call, function(data) {
               $('#servo_a').empty().append(data);
               //alert("success2" + data);
           });
        });
    });
      </script>
   </head>
   <body>
      <button id="plus_1">+1</button>
      <br>
         Servo angle: <span id="servo_a">Some random test</span>
   </body>
</html>





<!--
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="content-type" content="text/html;charset=UTF-8">
    <title>Python-jQuery Example</title>
    <script src="http://code.jquery.com/jquery-2.0.3.js"></script>
    <script>
        $(function()
        {
            //$command = "pyechoarg.py abc"
            $.ajax({
                url: "pyechoarg.py abc",
                type: "post",
                datatype: "html",
                data: "here is data",
                success: function(response)
                {
                	alert(response);
                        $("#div").html(response);
                        console.log("There is a response"); 
                }
            });
        });

    </script>
</head>
<body>
    <div id="div">Default Stuff</div>
</body>
</html>


<!DOCTYPE html>
<html>
<script src="http://code.jquery.com/jquery-2.0.3.js"></script>
<body>
 
<h2>AJAX Hello World</h2>
 
<p id="demo">Update content using ajax.</p>
 
<button type="button" onclick="loadDocument()">Update Content</button>
 
<script>
function loadDocument() 
{
alert("hello!");

            $.ajax({
                url: "pyechoarg.py abc",
                type: "post",
                datatype: "html",
                data: "here is data",
                success: function(response)
                {
                	alert(response);
                        document.getElementById("demo").innerHTML = response;
                        console.log("There is a response"); 
                }
            });

  /*var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() 
  {
    if (this.readyState == 4 && this.status == 200) 
    {
      document.getElementById("demo").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", "test.txt", true);
  xhttp.send();*/
}
</script>
 
</body>
</html>

-->


