// Get the button and container elements from HTML
const button = document.getElementById("theButton")
const data = document.getElementById("info")

// Create an array of cars to send to the server
const cars = [
 { "make":"Porsche", "model":"911S" },
 { "make":"Mercedes-Benz", "model":"220SE" },
 { "make":"Jaguar","model": "Mark VII" }
];

// Create an event listener on the button element
button.onclick= function(){
    alert("hello");

  // Get the reciever endpoint from Python using fetch
  fetch("http://127.0.0.1:5000/receiver", 
    {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
        'Accept': 'application/json'
      },
    // Strigify the payload into JSON
    body:JSON.stringify(cars)}).then(res=>{
        if(res.ok){
          return res.json()
        }else{
          alert("something is wrong")
        }
      }).then(jsonResponse=>{
        
        // Log the response data in the console
        console.log(jsonResponse)
      } 
      ).catch((err) => console.error(err));
      
     }
