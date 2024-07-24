<?php 
// use your login details
$servername = "192.168.35.54"; // IP Address of our actual server computer 
$db_name = "d11ms46_miniproject";  //e.g. D16AMS90_exam
$username = "Vedant"; //e.g. D16AMS90  
$password = "vedant@mini"; //e.g. NGR5YT6Y

// Create connection
$conn = new mysqli($servername, $username, $password);
// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

$sql1 = "USE ". $db_name . ";";
if ($conn->query($sql1) === TRUE) {
  #echo " ";
} else {
  echo "Error: " . $sql1 . "<br>" . $conn->error;
}


?>
