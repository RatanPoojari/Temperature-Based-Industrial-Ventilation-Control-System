<?php
require_once 'login.php';
$sql2 = "select * from sensor getLastRecord ORDER BY datetime DESC LIMIT 1;";




$result = $conn->query($sql2);
if ($result->num_rows > 0) {
$row = $result->fetch_assoc();
$DateTime=$row["datetime"];
$temperature=$row["temperature"];
$humidity=$row["humidity"];
}




$conn->close();






$Bdata = array();
$bar_label = array("Temperature", "Humidity");
$bar_colors = array("#FC420B", "#2DFAB0 ");
$bar_val = array($temperature,$humidity);


$point = array("Bcolor" => $bar_colors,"Bval" => $bar_val,"Blabel" => $bar_label);
array_push($Bdata,$point);

$myJSON = json_encode($Bdata);

echo $myJSON;









?>
